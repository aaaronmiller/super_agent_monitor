"""
MCP Interface for Delobotomize RAG Server
Provides Model Context Protocol tools for agents to query RAG
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
from rag_pipeline import OptimalRAG


class MCPRAGInterface:
    """
    MCP server that exposes RAG querying capabilities to Claude Code agents.
    """

    def __init__(self, rag_instance: Optional[OptimalRAG]):
        self.rag = rag_instance
        self.server_info = {
            "name": "delobotomize-rag",
            "version": "5.0.0",
            "protocolVersion": "2024-11-05",
        }

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Return available MCP tools"""
        return [
            {
                "name": "rag_query",
                "description": "Query the RAG index for relevant code context and findings",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Natural language query about code issues or patterns",
                        },
                        "run_id": {
                            "type": "string",
                            "description": "Optional run ID to scope the search",
                        },
                        "top_k": {
                            "type": "integer",
                            "default": 10,
                            "description": "Number of results to return",
                        },
                        "query_type": {
                            "type": "string",
                            "enum": ["keyword_heavy", "semantic", "hybrid"],
                            "default": "hybrid",
                            "description": "Type of query for routing optimization",
                        },
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "rag_index_status",
                "description": "Get indexing status for a run",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "run_id": {
                            "type": "string",
                            "description": "Run ID to check indexing status for",
                        }
                    },
                    "required": ["run_id"],
                },
            },
        ]

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP tool calls"""

        if tool_name == "rag_query":
            return await self._handle_rag_query(arguments)
        elif tool_name == "rag_index_status":
            return await self._handle_index_status(arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    async def _handle_rag_query(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle rag_query tool calls"""
        query = args.get("query", "")
        run_id = args.get("run_id")
        top_k = args.get("top_k", 10)
        query_type = args.get("query_type", "hybrid")

        if not query:
            return {"error": "Query parameter is required", "results": []}

        try:
            # Perform RAG query
            if not self.rag:
                return {"error": "RAG system not initialized", "results": []}

            results = self.rag.query(query, top_k=top_k)

            # Format results for MCP
            formatted_results = []
            for result in results:
                formatted_results.append(
                    {
                        "chunk_id": result.get("chunk_id"),
                        "content": result.get("text", result.get("content", "")),
                        "score": result.get("score", result.get("rerank_score", 0)),
                        "source": result.get("source", "unknown"),
                        "metadata": {
                            "file": result.get("file"),
                            "line": result.get("line"),
                            "function": result.get("function"),
                            "type": result.get("type"),
                        },
                    }
                )

            return {
                "results": formatted_results,
                "query_time_ms": 0,  # Would track actual timing
                "total_results": len(formatted_results),
            }

        except Exception as e:
            return {"error": f"RAG query failed: {str(e)}", "results": []}

    async def _handle_index_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle rag_index_status tool calls"""
        run_id = args.get("run_id", "")

        if not run_id:
            return {"error": "run_id parameter is required"}

        try:
            # Check if index exists for this run
            # This is a simplified implementation
            index_exists = self._check_index_exists(run_id)

            return {
                "run_id": run_id,
                "index_phase": "findings_only" if index_exists else "none",
                "chunks_indexed": 0,  # Would track actual count
                "last_updated": None,  # Would track actual timestamp
            }

        except Exception as e:
            return {"error": f"Index status check failed: {str(e)}"}

    def _check_index_exists(self, run_id: str) -> bool:
        """Check if RAG index exists for the given run"""
        # Simplified check - would implement proper index detection
        return False

    def create_mcp_response(self, tool_call_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Create properly formatted MCP response"""
        return {"jsonrpc": "2.0", "id": tool_call_id, "result": result}

    def create_mcp_error(self, tool_call_id: str, error: str) -> Dict[str, Any]:
        """Create properly formatted MCP error response"""
        return {"jsonrpc": "2.0", "id": tool_call_id, "error": {"code": -32603, "message": error}}


class MCPRAGServer:
    """
    MCP server implementation that handles JSON-RPC communication
    """

    def __init__(self, rag_instance: Optional[OptimalRAG], port: int = 4001):
        self.rag_interface = MCPRAGInterface(rag_instance)
        self.port = port

    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP messages"""

        # Validate JSON-RPC format
        if message.get("jsonrpc") != "2.0":
            return self._error_response(None, "Invalid JSON-RPC version")

        message_id = message.get("id")
        method = message.get("method")
        params = message.get("params", {})

        try:
            if method == "initialize":
                return await self._handle_initialize(message_id)
            elif method == "tools/list":
                return await self._handle_tools_list(message_id)
            elif method == "tools/call":
                return await self._handle_tools_call(message_id, params)
            else:
                return self._error_response(message_id, f"Unknown method: {method}")

        except Exception as e:
            return self._error_response(message_id, f"Internal error: {str(e)}")

    async def _handle_initialize(self, message_id: Any) -> Dict[str, Any]:
        """Handle MCP initialization"""
        return {
            "jsonrpc": "2.0",
            "id": message_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": self.rag_interface.server_info,
            },
        }

    async def _handle_tools_list(self, message_id: Any) -> Dict[str, Any]:
        """Handle tools/list request"""
        tools = self.rag_interface.get_available_tools()
        return {"jsonrpc": "2.0", "id": message_id, "result": {"tools": tools}}

    async def _handle_tools_call(self, message_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if not tool_name:
            return self._error_response(message_id, "Tool name is required")

        try:
            result = await self.rag_interface.handle_tool_call(tool_name, arguments)
            return self.rag_interface.create_mcp_response(message_id, result)
        except Exception as e:
            return self.rag_interface.create_mcp_error(message_id, str(e))

    def _error_response(self, message_id: Any, error: str) -> Dict[str, Any]:
        """Create error response"""
        return {"jsonrpc": "2.0", "id": message_id, "error": {"code": -32603, "message": error}}

    async def start_server(self):
        """Start the MCP server (simplified implementation)"""
        print(f"Starting MCP RAG server on port {self.port}")

        # In a real implementation, this would use a proper async server
        # For now, just demonstrate the interface
        print("MCP RAG server initialized")
        print("Available tools:")
        for tool in self.rag_interface.get_available_tools():
            print(f"  - {tool['name']}: {tool['description']}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Delobotomize MCP RAG Server")
    parser.add_argument(
        "--index-path", default="/app/rag-index", help="Path to RAG index directory"
    )
    parser.add_argument("--port", type=int, default=4001, help="Port to run MCP server on")

    args = parser.parse_args()

    # Initialize RAG (would handle missing dependencies gracefully)
    try:
        from rag_pipeline import OptimalRAG

        rag = OptimalRAG(args.index_path)
    except ImportError as e:
        print(f"Warning: RAG dependencies not available: {e}")
        print("Server will start but queries will fail")
        rag = None

    # Start MCP server
    server = MCPRAGServer(rag, args.port)

    # Run server (simplified)
    asyncio.run(server.start_server())

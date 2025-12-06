import http from 'http';
import net from 'net';
import { URL } from 'url';
import { EventEmitter } from 'events';

export class ProxyService extends EventEmitter {
    private server: http.Server;
    private port: number = 0;
    private activeSessions: Map<string, number> = new Map(); // sessionId -> lastActivityTimestamp

    constructor() {
        super();
        this.server = http.createServer((req, res) => {
            // Handle HTTP requests (less common for API calls which are usually HTTPS)
            this.handleRequest(req, res);
        });

        this.server.on('connect', (req, clientSocket, head) => {
            // Handle HTTPS CONNECT
            this.handleConnect(req, clientSocket, head);
        });
    }

    public async start(): Promise<number> {
        return new Promise((resolve, reject) => {
            this.server.listen(0, () => {
                const address = this.server.address();
                if (typeof address === 'object' && address) {
                    this.port = address.port;
                    console.log(`[ProxyService] Started on port ${this.port}`);
                    resolve(this.port);
                } else {
                    reject(new Error('Failed to get proxy port'));
                }
            });
        });
    }

    public getPort(): number {
        return this.port;
    }

    public registerSession(sessionId: string) {
        this.activeSessions.set(sessionId, Date.now());
    }

    public getLastActivity(sessionId: string): number {
        return this.activeSessions.get(sessionId) || 0;
    }

    private handleRequest(req: http.IncomingMessage, res: http.ServerResponse) {
        // Basic HTTP forwarding (not used much for Anthropic API)
        // But useful for logging
        this.emitActivity(req);

        const url = new URL(req.url || '');
        const options = {
            hostname: url.hostname,
            port: url.port || 80,
            path: url.pathname + url.search,
            method: req.method,
            headers: req.headers,
        };

        const proxyReq = http.request(options, (proxyRes) => {
            res.writeHead(proxyRes.statusCode || 500, proxyRes.headers);
            proxyRes.pipe(res, { end: true });
        });

        req.pipe(proxyReq, { end: true });

        proxyReq.on('error', (err) => {
            console.error('[ProxyService] Request error:', err);
            res.end();
        });
    }

    private handleConnect(req: http.IncomingMessage, clientSocket: any, head: Buffer) {
        this.emitActivity(req);

        const { port, hostname } = new URL(`http://${req.url}`);

        const serverSocket = net.connect(Number(port) || 443, hostname, () => {
            clientSocket.write('HTTP/1.1 200 Connection Established\r\n' +
                'Proxy-agent: SuperAgentMonitor-Proxy\r\n' +
                '\r\n');
            serverSocket.write(head);
            serverSocket.pipe(clientSocket);
            clientSocket.pipe(serverSocket);
        });

        serverSocket.on('error', (err) => {
            console.error('[ProxyService] Socket error:', err);
            clientSocket.end();
        });

        clientSocket.on('error', (err: any) => {
            console.error('[ProxyService] Client socket error:', err);
            serverSocket.end();
        });

        // Monitor data flow for ongoing activity
        clientSocket.on('data', () => this.emitActivity(req));
        serverSocket.on('data', () => this.emitActivity(req));
    }

    private emitActivity(req: http.IncomingMessage) {
        // In a real implementation, we'd map the source port/IP to a session ID.
        // Since we are running locally and spawning processes, we might need to 
        // assign a unique proxy port per session OR use an auth header to identify the session.
        // For this MVP, we'll assume single active session or just update a global "system activity".
        // TO IMPROVE: SessionLauncher should pass a unique header or we use distinct ports.

        // Hack for MVP: We assume the most recently registered session is the active one 
        // or we just update all active sessions (since we are a monitor for one user).
        const now = Date.now();
        for (const sessionId of this.activeSessions.keys()) {
            this.activeSessions.set(sessionId, now);
        }

        this.emit('activity');
    }
}

export const proxyService = new ProxyService();

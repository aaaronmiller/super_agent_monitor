import axios from 'axios'

const LM_STUDIO_URL = process.env.LM_STUDIO_URL || 'http://localhost:1234/v1'

export interface LocalModel {
    id: string
    object: string
    owned_by: string
    created?: number
}

export interface LocalModelStatus {
    available: boolean
    baseUrl: string
    models: LocalModel[]
    error?: string
}

export interface ChatMessage {
    role: 'system' | 'user' | 'assistant'
    content: string
}

export interface ChatCompletionRequest {
    model: string
    messages: ChatMessage[]
    temperature?: number
    max_tokens?: number
    stream?: boolean
}

export interface ChatCompletionResponse {
    id: string
    object: string
    created: number
    model: string
    choices: {
        index: number
        message: ChatMessage
        finish_reason: string
    }[]
    usage: {
        prompt_tokens: number
        completion_tokens: number
        total_tokens: number
    }
}

class LocalModelService {
    private baseUrl: string

    constructor() {
        this.baseUrl = LM_STUDIO_URL
    }

    /**
     * Check if LM Studio is running and available
     */
    async getStatus(): Promise<LocalModelStatus> {
        try {
            const models = await this.listModels()
            return {
                available: true,
                baseUrl: this.baseUrl,
                models
            }
        } catch (error) {
            return {
                available: false,
                baseUrl: this.baseUrl,
                models: [],
                error: (error as Error).message
            }
        }
    }

    /**
     * List available models from LM Studio
     */
    async listModels(): Promise<LocalModel[]> {
        const response = await axios.get(`${this.baseUrl}/models`, {
            timeout: 5000
        })
        return response.data.data || []
    }

    /**
     * Send a chat completion request to LM Studio
     */
    async chat(request: ChatCompletionRequest): Promise<ChatCompletionResponse> {
        const response = await axios.post(`${this.baseUrl}/chat/completions`, request, {
            timeout: 300000 // 5 minute timeout for long generations
        })
        return response.data
    }

    /**
     * Get recommended model configurations for council patterns
     */
    getRecommendedConfigs() {
        return {
            'vibethinker-1.5b': {
                id: 'vibethinker-1.5b',
                name: 'VibeThinker 1.5B',
                description: 'Math specialist - 80.3 AIME24, extremely efficient',
                temperature: 0.7,
                max_tokens: 131000,
                bestFor: ['math', 'code', 'reasoning']
            },
            'dr-tulu-8b': {
                id: 'dr-tulu-8b',
                name: 'Dr. Tulu 8B',
                description: 'Research specialist - long-form deep research with tool use',
                temperature: 0.7,
                max_tokens: 128000,
                bestFor: ['research', 'search', 'analysis']
            },
            'qwen3-32b': {
                id: 'qwen3-32b-instruct',
                name: 'Qwen3 32B Instruct',
                description: 'Strong general reasoning, 131k output',
                temperature: 0.7,
                max_tokens: 131000,
                bestFor: ['general', 'coding', 'reasoning']
            },
            'deepseek-r1-14b': {
                id: 'deepseek-r1-14b',
                name: 'DeepSeek R1 14B',
                description: 'Transparent reasoning traces, 128k output',
                temperature: 0.7,
                max_tokens: 128000,
                bestFor: ['reasoning', 'transparency', 'debugging']
            }
        }
    }

    /**
     * Get speculative decoding configurations
     */
    getSpeculativeConfigs() {
        return {
            'qwen3-32b-spec': {
                target: 'qwen3-32b-instruct-mlx-4bit',
                draft: 'qwen3-0.5b-instruct-mlx-4bit',
                expectedSpeedup: '2.4x',
                ramUsage: '~20.5GB'
            },
            'deepseek-spec': {
                target: 'deepseek-r1-14b-mlx-4bit',
                draft: 'qwen3-0.5b-instruct-mlx-4bit',
                qualifier: 'qwen3-1.7b-instruct-mlx-4bit',
                expectedSpeedup: '2.8-3.5x (pyramid)',
                ramUsage: '~11GB'
            }
        }
    }
}

export const localModelService = new LocalModelService()

import axios from 'axios'

export interface EmbeddingResponse {
  embedding: number[]
  tokens: number
  model: string
}

/**
 * Service for generating text embeddings using OpenAI API
 */
export class EmbeddingService {
  private apiKey: string
  private model: string
  private baseURL: string
  private cache: Map<string, number[]> = new Map()
  private maxCacheSize: number = 1000

  constructor(config?: {
    apiKey?: string
    model?: string
    baseURL?: string
  }) {
    this.apiKey = config?.apiKey || process.env.OPENAI_API_KEY || ''
    this.model = config?.model || 'text-embedding-3-small'
    this.baseURL = config?.baseURL || 'https://api.openai.com/v1'

    if (!this.apiKey) {
      console.warn('⚠️  No OpenAI API key configured. Embedding service will not work.')
    }
  }

  /**
   * Generate embedding for a single text
   */
  async embed(text: string): Promise<EmbeddingResponse> {
    if (!this.apiKey) {
      throw new Error('OpenAI API key not configured')
    }

    // Check cache
    const cacheKey = this.getCacheKey(text)
    if (this.cache.has(cacheKey)) {
      return {
        embedding: this.cache.get(cacheKey)!,
        tokens: 0, // Cache hit, no tokens used
        model: this.model
      }
    }

    // Truncate text if too long (max 8191 tokens for text-embedding-3-small)
    const truncatedText = this.truncateText(text, 8000)

    try {
      const response = await axios.post(
        `${this.baseURL}/embeddings`,
        {
          input: truncatedText,
          model: this.model,
          encoding_format: 'float'
        },
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          }
        }
      )

      const embedding = response.data.data[0].embedding
      const tokens = response.data.usage.total_tokens

      // Cache the result
      this.addToCache(cacheKey, embedding)

      return {
        embedding,
        tokens,
        model: this.model
      }
    } catch (error: any) {
      console.error('Embedding API error:', error.response?.data || error.message)
      throw new Error(`Failed to generate embedding: ${error.message}`)
    }
  }

  /**
   * Generate embeddings for multiple texts (batched)
   */
  async embedBatch(texts: string[]): Promise<EmbeddingResponse[]> {
    if (!this.apiKey) {
      throw new Error('OpenAI API key not configured')
    }

    if (texts.length === 0) {
      return []
    }

    // Check cache for all texts
    const results: EmbeddingResponse[] = []
    const uncachedTexts: string[] = []
    const uncachedIndices: number[] = []

    texts.forEach((text, idx) => {
      const cacheKey = this.getCacheKey(text)
      if (this.cache.has(cacheKey)) {
        results[idx] = {
          embedding: this.cache.get(cacheKey)!,
          tokens: 0,
          model: this.model
        }
      } else {
        uncachedTexts.push(this.truncateText(text, 8000))
        uncachedIndices.push(idx)
      }
    })

    // If all cached, return early
    if (uncachedTexts.length === 0) {
      return results
    }

    try {
      const response = await axios.post(
        `${this.baseURL}/embeddings`,
        {
          input: uncachedTexts,
          model: this.model,
          encoding_format: 'float'
        },
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          }
        }
      )

      const embeddings = response.data.data
      const totalTokens = response.data.usage.total_tokens
      const tokensPerText = Math.ceil(totalTokens / uncachedTexts.length)

      // Fill in results for uncached texts
      uncachedIndices.forEach((idx, i) => {
        const embedding = embeddings[i].embedding
        results[idx] = {
          embedding,
          tokens: tokensPerText,
          model: this.model
        }

        // Cache the result
        const cacheKey = this.getCacheKey(texts[idx])
        this.addToCache(cacheKey, embedding)
      })

      return results
    } catch (error: any) {
      console.error('Batch embedding API error:', error.response?.data || error.message)
      throw new Error(`Failed to generate embeddings: ${error.message}`)
    }
  }

  /**
   * Calculate cosine similarity between two embeddings
   */
  cosineSimilarity(a: number[], b: number[]): number {
    if (a.length !== b.length) {
      throw new Error('Embeddings must have same dimensions')
    }

    let dotProduct = 0
    let normA = 0
    let normB = 0

    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i]
      normA += a[i] * a[i]
      normB += b[i] * b[i]
    }

    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB))
  }

  /**
   * Generate cache key for text
   */
  private getCacheKey(text: string): string {
    // Simple hash function for cache keys
    let hash = 0
    for (let i = 0; i < text.length; i++) {
      const char = text.charCodeAt(i)
      hash = ((hash << 5) - hash) + char
      hash = hash & hash // Convert to 32bit integer
    }
    return `${this.model}:${hash}`
  }

  /**
   * Add embedding to cache with LRU eviction
   */
  private addToCache(key: string, embedding: number[]): void {
    // Simple LRU: remove oldest if cache is full
    if (this.cache.size >= this.maxCacheSize) {
      const firstKey = this.cache.keys().next().value
      if (firstKey) {
        this.cache.delete(firstKey)
      }
    }

    this.cache.set(key, embedding)
  }

  /**
   * Truncate text to approximate token limit
   * Rough estimate: 1 token ≈ 4 characters
   */
  private truncateText(text: string, maxTokens: number): string {
    const maxChars = maxTokens * 4
    if (text.length <= maxChars) {
      return text
    }

    return text.slice(0, maxChars) + '...'
  }

  /**
   * Clear the embedding cache
   */
  clearCache(): void {
    this.cache.clear()
  }

  /**
   * Get cache statistics
   */
  getCacheStats(): { size: number; maxSize: number; hitRate?: number } {
    return {
      size: this.cache.size,
      maxSize: this.maxCacheSize
    }
  }
}

// Singleton instance
export const embeddingService = new EmbeddingService()

import { Router } from 'express'
import { componentRegistry } from '../services/ComponentRegistry'

export const componentsRouter = Router()

/**
 * GET /api/components
 * List all components
 */
componentsRouter.get('/', async (req, res) => {
  try {
    const { category, tag, search } = req.query

    let components = componentRegistry.getAll()

    // Filter by category
    if (category && typeof category === 'string') {
      components = componentRegistry.getByCategory(category as any)
    }

    // Filter by tag
    if (tag && typeof tag === 'string') {
      components = componentRegistry.searchByTag(tag)
    }

    // Search by keyword
    if (search && typeof search === 'string') {
      components = componentRegistry.search(search)
    }

    res.json({
      components: components.map(c => ({
        id: c.id,
        name: c.name,
        displayName: c.displayName,
        description: c.description,
        category: c.category,
        tags: c.tags,
        version: c.version,
        model: c.model,
        pattern: c.pattern
      })),
      total: components.length,
      lastScan: componentRegistry.getLastScanTime()
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'SCAN_ERROR', message: error.message } })
  }
})

/**
 * GET /api/components/stats
 * Get component statistics
 */
componentsRouter.get('/stats', async (req, res) => {
  try {
    const stats = componentRegistry.getStats()
    res.json(stats)
  } catch (error: any) {
    res.status(500).json({ error: { code: 'STATS_ERROR', message: error.message } })
  }
})

/**
 * GET /api/components/:id
 * Get component details by ID
 */
componentsRouter.get('/:id', async (req, res) => {
  try {
    const component = componentRegistry.getById(req.params.id)

    if (!component) {
      return res.status(404).json({
        error: { code: 'NOT_FOUND', message: 'Component not found' }
      })
    }

    res.json({ component })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'FETCH_ERROR', message: error.message } })
  }
})

/**
 * GET /api/components/:id/compatible
 * Get components compatible with the given component
 */
componentsRouter.get('/:id/compatible', async (req, res) => {
  try {
    const compatible = componentRegistry.getCompatible(req.params.id)

    res.json({
      components: compatible.map(c => ({
        id: c.id,
        name: c.name,
        displayName: c.displayName,
        description: c.description,
        category: c.category,
        tags: c.tags
      })),
      total: compatible.length
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'COMPATIBLE_ERROR', message: error.message } })
  }
})

/**
 * POST /api/components/recommendations
 * Get recommended components based on selected components
 * Body: { selectedComponents: string[] }
 */
componentsRouter.post('/recommendations', async (req, res) => {
  try {
    const { selectedComponents } = req.body

    if (!Array.isArray(selectedComponents)) {
      return res.status(400).json({
        error: { code: 'INVALID_INPUT', message: 'selectedComponents must be an array' }
      })
    }

    const recommendations = componentRegistry.getRecommendations(selectedComponents)

    res.json({
      recommendations: recommendations.map(c => ({
        id: c.id,
        name: c.name,
        displayName: c.displayName,
        description: c.description,
        category: c.category,
        tags: c.tags,
        reason: this.getRecommendationReason(c, selectedComponents)
      })),
      total: recommendations.length
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'RECOMMENDATION_ERROR', message: error.message } })
  }
})

/**
 * POST /api/components/scan
 * Trigger component registry scan
 */
componentsRouter.post('/scan', async (req, res) => {
  try {
    await componentRegistry.scan()

    res.json({
      success: true,
      stats: componentRegistry.getStats()
    })
  } catch (error: any) {
    res.status(500).json({ error: { code: 'SCAN_ERROR', message: error.message } })
  }
})

/**
 * Helper to generate recommendation reason
 */
function getRecommendationReason(component: any, selectedComponents: string[]): string {
  const selected = selectedComponents
    .map(id => componentRegistry.getById(id))
    .filter(Boolean)

  // Check if it's a dependency
  for (const s of selected) {
    if (s?.dependencies?.includes(component.name)) {
      return `Required dependency of ${s.displayName || s.name}`
    }
  }

  // Check for shared tags
  const sharedTags = component.tags?.filter((tag: string) =>
    selected.some(s => s?.tags?.includes(tag))
  )

  if (sharedTags?.length) {
    return `Related (tags: ${sharedTags.slice(0, 3).join(', ')})`
  }

  return 'Commonly used together'
}

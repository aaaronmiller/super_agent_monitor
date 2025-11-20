import fs from 'fs/promises'
import path from 'path'
import matter from 'gray-matter'

export interface ComponentMetadata {
  name: string
  displayName?: string
  description?: string
  category: 'agent' | 'skill' | 'hook' | 'script' | 'orchestrator'
  tags?: string[]
  dependencies?: string[]
  incompatibilities?: string[]
  model?: string
  tools?: string[]
  version?: string
  pattern?: string
}

export interface Component extends ComponentMetadata {
  id: string
  filePath: string
  content: string
  language?: 'markdown' | 'python' | 'shell' | 'yaml'
}

export class ComponentRegistry {
  private components: Map<string, Component> = new Map()
  private componentsDir: string
  private lastScanTime: Date | null = null

  constructor(componentsDir: string = path.join(process.cwd(), 'components')) {
    this.componentsDir = componentsDir
  }

  /**
   * Scan components directory and index all components
   */
  async scan(): Promise<void> {
    console.log(`🔍 Scanning components in ${this.componentsDir}...`)
    this.components.clear()

    const categories = ['agents', 'skills', 'hooks', 'scripts', 'orchestrators']

    for (const category of categories) {
      const categoryPath = path.join(this.componentsDir, category)

      try {
        const exists = await fs.access(categoryPath).then(() => true).catch(() => false)
        if (!exists) {
          console.warn(`⚠️  Category directory not found: ${category}`)
          continue
        }

        await this.scanCategory(categoryPath, category as any)
      } catch (error) {
        console.error(`Error scanning ${category}:`, error)
      }
    }

    this.lastScanTime = new Date()
    console.log(`✅ Scanned ${this.components.size} components`)
  }

  /**
   * Scan a category directory (agents, skills, etc.)
   */
  private async scanCategory(categoryPath: string, category: Component['category']): Promise<void> {
    const entries = await fs.readdir(categoryPath, { withFileTypes: true })

    for (const entry of entries) {
      const fullPath = path.join(categoryPath, entry.name)

      if (entry.isDirectory()) {
        // For skills (which have SKILL.md inside a directory)
        if (category === 'skill') {
          const skillFilePath = path.join(fullPath, 'SKILL.md')
          const exists = await fs.access(skillFilePath).then(() => true).catch(() => false)
          if (exists) {
            await this.indexComponent(skillFilePath, category, entry.name)
          }
        }
      } else if (entry.isFile()) {
        await this.indexComponent(fullPath, category)
      }
    }
  }

  /**
   * Index a single component file
   */
  private async indexComponent(
    filePath: string,
    category: Component['category'],
    skillName?: string
  ): Promise<void> {
    try {
      const content = await fs.readFile(filePath, 'utf-8')
      const ext = path.extname(filePath)
      const basename = path.basename(filePath, ext)

      let metadata: ComponentMetadata
      let language: Component['language']

      // Parse based on file type
      if (ext === '.md') {
        // Markdown with YAML frontmatter
        const parsed = matter(content)
        metadata = parsed.data as ComponentMetadata
        language = 'markdown'
      } else if (ext === '.py') {
        // Python script - extract metadata from docstring
        metadata = this.parsePythonMetadata(content, basename)
        language = 'python'
      } else if (ext === '.sh') {
        // Shell script - extract metadata from comments
        metadata = this.parseShellMetadata(content, basename)
        language = 'shell'
      } else if (ext === '.yaml' || ext === '.yml') {
        // YAML workflow template
        metadata = this.parseYamlMetadata(content)
        language = 'yaml'
      } else {
        // Unknown file type
        console.warn(`⚠️  Unknown file type: ${filePath}`)
        return
      }

      // Generate component ID
      const id = this.generateId(metadata.name || skillName || basename, category)

      const component: Component = {
        id,
        filePath,
        content,
        language,
        category,
        ...metadata
      }

      this.components.set(id, component)
      console.log(`  ✓ Indexed: ${id}`)

    } catch (error) {
      console.error(`Error indexing ${filePath}:`, error)
    }
  }

  /**
   * Parse metadata from Python script docstring
   */
  private parsePythonMetadata(content: string, filename: string): ComponentMetadata {
    // Extract docstring
    const docstringMatch = content.match(/^"""([\s\S]*?)"""/)
    const docstring = docstringMatch ? docstringMatch[1].trim() : ''

    // Extract title and description
    const lines = docstring.split('\n')
    const title = lines[0] || filename
    const description = lines.slice(1).join(' ').trim() || `${filename} script`

    return {
      name: filename.replace(/-/g, '_'),
      displayName: title,
      description,
      category: 'script',
      tags: []
    }
  }

  /**
   * Parse metadata from shell script comments
   */
  private parseShellMetadata(content: string, filename: string): ComponentMetadata {
    // Extract header comments
    const lines = content.split('\n').filter(line => line.startsWith('#'))
    const title = lines[0]?.replace(/^#\s*/, '') || filename
    const description = lines[1]?.replace(/^#\s*/, '') || `${filename} hook`

    return {
      name: filename.replace(/-/g, '_'),
      displayName: title,
      description,
      category: 'hook',
      tags: []
    }
  }

  /**
   * Parse metadata from YAML workflow
   */
  private parseYamlMetadata(content: string): ComponentMetadata {
    // This would use a YAML parser in production
    // For now, extract basic info with regex
    const nameMatch = content.match(/^name:\s*(.+)$/m)
    const descMatch = content.match(/^description:\s*(.+)$/m)

    return {
      name: nameMatch?.[1]?.trim() || 'unknown',
      description: descMatch?.[1]?.trim() || '',
      category: 'orchestrator',
      tags: []
    }
  }

  /**
   * Generate unique component ID
   */
  private generateId(name: string, category: string): string {
    return `${category}:${name.toLowerCase().replace(/[^a-z0-9-_]/g, '-')}`
  }

  /**
   * Get all components
   */
  getAll(): Component[] {
    return Array.from(this.components.values())
  }

  /**
   * Get components by category
   */
  getByCategory(category: Component['category']): Component[] {
    return this.getAll().filter(c => c.category === category)
  }

  /**
   * Get component by ID
   */
  getById(id: string): Component | undefined {
    return this.components.get(id)
  }

  /**
   * Search components by tag
   */
  searchByTag(tag: string): Component[] {
    return this.getAll().filter(c => c.tags?.includes(tag))
  }

  /**
   * Search components by keyword (name, description, tags)
   */
  search(keyword: string): Component[] {
    const lowerKeyword = keyword.toLowerCase()
    return this.getAll().filter(c => {
      return (
        c.name?.toLowerCase().includes(lowerKeyword) ||
        c.displayName?.toLowerCase().includes(lowerKeyword) ||
        c.description?.toLowerCase().includes(lowerKeyword) ||
        c.tags?.some(tag => tag.toLowerCase().includes(lowerKeyword))
      )
    })
  }

  /**
   * Get components compatible with a given component
   */
  getCompatible(componentId: string): Component[] {
    const component = this.getById(componentId)
    if (!component) return []

    return this.getAll().filter(c => {
      // Don't include self
      if (c.id === componentId) return false

      // Check incompatibilities
      if (component.incompatibilities?.includes(c.name)) return false
      if (c.incompatibilities?.includes(component.name)) return false

      return true
    })
  }

  /**
   * Get recommended components based on dependencies and common pairings
   */
  getRecommendations(selectedComponents: string[]): Component[] {
    const recommendations = new Map<string, number>() // component ID -> score

    for (const selectedId of selectedComponents) {
      const selected = this.getById(selectedId)
      if (!selected) continue

      // Recommend dependencies
      selected.dependencies?.forEach(depName => {
        const dep = this.getAll().find(c => c.name === depName)
        if (dep) {
          recommendations.set(dep.id, (recommendations.get(dep.id) || 0) + 10)
        }
      })

      // Recommend components with similar tags
      selected.tags?.forEach(tag => {
        this.searchByTag(tag).forEach(c => {
          if (!selectedComponents.includes(c.id)) {
            recommendations.set(c.id, (recommendations.get(c.id) || 0) + 1)
          }
        })
      })
    }

    // Sort by score and return top recommendations
    return Array.from(recommendations.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([id]) => this.getById(id)!)
      .filter(Boolean)
  }

  /**
   * Get last scan time
   */
  getLastScanTime(): Date | null {
    return this.lastScanTime
  }

  /**
   * Get component statistics
   */
  getStats() {
    const all = this.getAll()
    return {
      total: all.length,
      byCategory: {
        agents: this.getByCategory('agent').length,
        skills: this.getByCategory('skill').length,
        hooks: this.getByCategory('hook').length,
        scripts: this.getByCategory('script').length,
        orchestrators: this.getByCategory('orchestrator').length
      },
      lastScan: this.lastScanTime?.toISOString()
    }
  }
}

// Singleton instance
export const componentRegistry = new ComponentRegistry()

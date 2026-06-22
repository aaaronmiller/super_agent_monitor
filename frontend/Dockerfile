# Frontend Dockerfile for Svelte 5 + Ice-ninja Stack

FROM oven/bun:1-alpine AS base

# Stage 1: Dependencies
FROM base AS deps
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

# Stage 2: Build
FROM deps AS builder
WORKDIR /app
COPY . .
RUN bun run build

# Stage 3: Runtime
FROM base AS runtime
WORKDIR /app

# Copy built assets
COPY --from=builder /app/build ./build
COPY package.json ./

# Install only production dependencies
RUN bun install --frozen-lockfile --production

# Expose port (SvelteKit preview default)
EXPOSE 4173

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:4173/ || exit 1

# Run with bun
CMD ["bun", "run", "preview", "--host", "0.0.0.0", "--port", "4173"]

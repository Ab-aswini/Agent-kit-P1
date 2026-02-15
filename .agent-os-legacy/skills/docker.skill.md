# Docker Skill

> Loaded by: DevOps Division agents | Version: 1.0

## Dockerfile Pattern
```dockerfile
# Multi-stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-alpine AS runtime
WORKDIR /app
RUN addgroup -g 1001 appgroup && adduser -u 1001 -G appgroup -s /bin/sh -D appuser
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -q --spider http://localhost:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

## Anti-Patterns
- Do NOT run containers as root
- Do NOT include dev dependencies in production images
- Do NOT hardcode secrets (use env vars or secrets management)
- Do NOT use `latest` tag in production
- Do NOT skip health checks

## Checklist
- [ ] Multi-stage build used
- [ ] Non-root user configured
- [ ] Health check defined
- [ ] .dockerignore is comprehensive
- [ ] No secrets in image; image size is optimized


# Pet Project: ToDo API (Flask + PostgreSQL + Docker)

## Quickstart

1. Install Docker and Docker Compose.
2. Copy `.env.sample` to `.env`:
   ```bash
   cp .env.sample .env
   ```
3. Start services:
   ```bash
   make up   # or: docker compose up -d --build
   ```
4. Test API:
   ```bash
   curl http://localhost:5000/health
   curl -X POST -H "Content-Type: application/json" -d '{"title":"Learn DevOps"}' http://localhost:5000/tasks
   curl http://localhost:5000/tasks
   ```

## Structure

```
backend/           # Flask API
db/init.sql        # DB schema (auto-applied on first start)
docker-compose.yml # Local dev stack
k8s/               # Kubernetes manifests (optional)
```

## Next steps (roadmap)
- Add tests in `backend/tests`
- Add CI/CD (GitLab/Jenkins)
- Container hardening & Gunicorn
- Kubernetes deployment
- Monitoring (Prometheus + Grafana)
- Centralized logging

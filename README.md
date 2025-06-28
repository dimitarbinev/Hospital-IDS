---

## 🐳 Running with Docker

This project provides Dockerfiles and a `docker-compose.yml` for easy setup of all core components:

- **Backend**: FastAPI app (Python 3.11)
- **Frontend**: Next.js dashboard (Node.js 22.13.1)
- **Database**: MongoDB

### 📦 Requirements & Versions
- **Backend**: Python 3.11 (from `python:3.11-slim`)
- **Frontend**: Node.js 22.13.1 (from `node:22.13.1-slim`)
- **Database**: MongoDB (latest)

### ⚙️ Build & Run
1. **Clone the repository** and ensure Docker & Docker Compose are installed.
2. **Build and start all services**:
   ```bash
   docker compose up --build
   ```
   This will build the backend and frontend images and start MongoDB.

### 🔑 Environment Variables
- No required environment variables are set by default.
- If you need to add secrets or config, uncomment and use the `env_file` lines in the `docker-compose.yml` for each service.

### 🔌 Ports
- **Backend (FastAPI)**: `8000` (internal, not published to host by default)
- **Frontend (Next.js)**: `3000` (internal, not published to host by default)
- **MongoDB**: `27017` (published to host for development)

> **Note:**
> - To access the frontend or backend from your host, add `ports:` mappings to the relevant service in `docker-compose.yml`, e.g.:
>   ```yaml
>   ports:
>     - "3000:3000"
>   ```
> - For production, remove or secure the MongoDB port mapping.
> - MongoDB data is not persisted by default. Uncomment the `volumes:` section in `docker-compose.yml` to enable data persistence.

### 🛠 Special Configuration
- The backend and frontend run as non-root users for security.
- Node and Python dependencies are installed and cached for faster builds.
- Healthcheck is enabled for MongoDB.

---

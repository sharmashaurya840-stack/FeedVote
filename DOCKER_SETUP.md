# Docker Setup Guide for FeedVote

**Last Updated:** March 30, 2026

This guide provides comprehensive instructions for setting up FeedVote using Docker on Windows systems. For quick setup, see [QUICKSTART.md](QUICKSTART.md).

---

## Prerequisites

### System Requirements for Windows

1. **Install Docker Desktop for Windows**
   - Download: https://www.docker.com/products/docker-desktop
   - Supported: Windows 10 Pro/Enterprise/Education or Windows 11
   - Requirements:
     - 4GB RAM (8GB recommended)
     - 2 CPU cores minimum
     - Virtualization enabled in BIOS
     - WSL 2 (Windows Subsystem for Linux 2) enabled

2. **Verify Installation**
   ```powershell
   docker --version
   docker-compose --version
   ```

---

## ⚡ Quick Start (2 Steps)

```powershell
# 1. Build images
docker-compose build

# 2. Start services
docker-compose up -d

# Access at http://localhost:8501
```

For detailed non-Docker setup, see [QUICKSTART.md](QUICKSTART.md).

---

## Deployment Options

### Option 1: Development (SQLite) - Default

Uses `docker-compose.yml`:

```powershell
docker-compose build
docker-compose up -d
```

**Database:** SQLite (backend/feedvote.db)  
**Best for:** Local development, learning, testing

**Access:**
- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### Option 2: Production (MySQL)

Uses `docker-compose.prod.yml`:

```powershell
docker-compose -f docker-compose.prod.yml up -d
```

**Database:** MySQL 8.0  
**Best for:** Production deployment, multi-user environments

**Features:**
- MySQL 8.0 with persistent storage
- Health checks for all services
- Proper service dependencies
- Environment-based security configuration

---

## Database Configuration

| Aspect | Development (SQLite) | Production (MySQL) |
|--------|----------------------|-------------------|
| Type | SQLite 3 | MySQL 8.0 |
| Location | `backend/feedvote.db` | Docker volume `mysql_data` |
| Persistence | File-based | Docker managed |
| Setup | Zero config | Requires configuration |
| Best For | Development | Enterprise |
| Data Survives | Yes (unless deleted) | Yes (unless volume deleted) |

---

## Common Commands Reference

| Task | Command |
|------|---------|
| Build images | `docker-compose build` |
| Start (background) | `docker-compose up -d` |
| Start (visible logs) | `docker-compose up` |
| View logs | `docker-compose logs -f` |
| Stop services | `docker-compose stop` |
| Remove containers | `docker-compose down` |
| Remove data | `docker-compose down -v` |
| View containers | `docker-compose ps` |
| Rebuild without cache | `docker-compose build --no-cache` |
| Run tests in container | `docker-compose exec backend python -m pytest` |

---

## Environment Variables

Create `.env` file from `.env.example` or configure via docker-compose.

**Development defaults:**
```
DATABASE_URL=sqlite:///./feedvote.db
BACKEND_URL=http://backend:8000
```

**Production example:**
```
DATABASE_URL=mysql+pymysql://root:password@db:3306/feedvote
BACKEND_URL=http://backend:8000
```

---

## Data Persistence

### Development (SQLite)
- **Host location:** `c:\Users\srbro\Dropbox\PC\Downloads\FeedVote-main\backend\feedvote.db`
- **Survives:** Container restarts ✓, `docker-compose stop` ✓
- **Deleted by:** Manual file deletion or `docker-compose down -v`

### Production (MySQL)
- **Host location:** Docker volume managed by Docker
- **Survives:** Container restarts ✓, `docker-compose stop` ✓  
- **Deleted by:** `docker-compose down -v`

---

## Service Health Checks

**Backend (FastAPI):**
- Checks `/health` endpoint
- Waits for API to be responsive before marking healthy

**Frontend (Streamlit):**
- Self-starting
- Depends on backend health check

Frontend starts only after backend reports healthy.

---

## 🆘 Troubleshooting

### Docker Not Found / Command Not Recognized
```
Error: "docker: command not found"
```
**Solution:**
1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
2. Restart PowerShell/Terminal after installation
3. Run: `docker --version` to verify

---

### Port Already in Use
```
Error: "Bind for 0.0.0.0:8000 failed"
```
**Solution:**
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000
netstat -ano | findstr :8501

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

---

### Database Connection Errors

**SQLite issues:**
```powershell
# Option 1: Delete database and restart
rm backend/feedvote.db
docker-compose up -d

# Option 2: Full rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

**MySQL issues:**
```powershell
# View logs for MySQL
docker-compose logs -f db

# Verify MySQL is healthy
docker-compose ps

# Rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

### Container Won't Start
```powershell
# View detailed error logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Full rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

---

### View Container Logs

```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# View only recent logs
docker-compose logs --tail=50 backend

# Save logs to file
docker-compose logs > logs.txt
```

---

## File Structure

```
FeedVote/
├── docker-compose.yml              # Development (SQLite)
├── docker-compose.prod.yml         # Production (MySQL)
├── .env.example                    # Environment template
├── backend/
│   ├── Dockerfile                  # Backend container definition
│   ├── requirements.txt            # Python dependencies
│   ├── app/
│   │   ├── main.py                # FastAPI application
│   │   ├── database.py            # Database configuration
│   │   ├── models.py              # SQLAlchemy models
│   │   ├── schemas.py             # Pydantic schemas
│   │   ├── crud.py                # Database operations
│   │   └── routes/                # API endpoints
│   ├── feedvote.db                # SQLite database (development)
│   └── tests/                     # Test files
├── frontend/
│   ├── Dockerfile                  # Frontend container definition
│   ├── requirements.txt            # Python dependencies
│   └── app.py                      # Streamlit application
└── README.md                        # Project documentation
```

---

## Production Deployment Tips

1. **Use `.env` file with secure credentials**
   ```powershell
   cp .env.example .env
   # Edit .env with production values
   ```

2. **Use `docker-compose.prod.yml`**
   ```powershell
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Set up reverse proxy (Nginx recommended)**
   - Route `yourdomain.com` → `localhost:8501` (frontend)
   - Route `yourdomain.com/api` → `localhost:8000` (backend)

4. **Database backups**
   ```powershell
   # MySQL backup
   docker-compose exec db mysqldump -u root -p feedvote > backup.sql
   ```

---

## Next Steps

1. Run `docker-compose build`
2. Run `docker-compose up -d`
3. Access http://localhost:8501
4. See **PROJECT_STATUS.md** for verification details
5. See **README.md** for API documentation

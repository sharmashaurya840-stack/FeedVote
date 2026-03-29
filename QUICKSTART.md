# FeedVote - Quick Start Guide

**Last Updated:** March 30, 2026  
**Status:** ✅ Production Ready

---

## ⚡ Get Running in 5 Minutes

### Option 1: Run Without Docker (Fastest)

**Prerequisites:** Python 3.10+

```powershell
# Terminal 1: Backend setup
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```powershell
# Terminal 2: Frontend setup
cd frontend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

**Browser will open automatically:**
- Frontend: http://localhost:8501
- Backend API docs: http://localhost:8000/docs

---

### Option 2: Run With Docker

**Prerequisites:** Docker Desktop installed

```powershell
# Build and start
docker-compose build
docker-compose up -d

# Access at:
# Frontend: http://localhost:8501
# Backend API docs: http://localhost:8000/docs

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🎯 Access Points

| Component | URL | Purpose |
|-----------|-----|---------|
| Frontend | http://localhost:8501 | Web interface for users |
| Backend API | http://localhost:8000 | REST API server |
| API Documentation | http://localhost:8000/docs | Interactive Swagger UI |
| Database | backend/feedvote.db | SQLite (auto-created) |

---

## ✨ Core Features to Test

1. **Register:** Create a new user via the sidebar
2. **Submit Idea:** Go to "Submit Feedback" page
3. **Vote:** Browse ideas and vote up/down
4. **Leaderboard:** View trending ideas in "Top Voted"

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `taskkill /PID <PID> /F` or use different port |
| Python not found | Install Python 3.10+ from python.org |
| Frontend can't connect | Ensure backend runs on port 8000 first |
| Database errors | Delete `backend/feedvote.db` and restart |
| Docker not found | Install Docker Desktop from docker.com |

---

## 📚 Full Documentation

- **README.md** — Complete overview, architecture, and API reference
- **DOCKER_SETUP.md** — Detailed Docker configuration and troubleshooting
- **PROJECT_STATUS.md** — Current status, verification results, and deployment options

---

**Pick Option 1 or 2 above and start in 5 minutes!**

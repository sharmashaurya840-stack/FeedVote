# 🗳️ FeedVote

## 🎯 Problem Statement

FeedVote is a lightweight feedback and voting application for small teams and classroom projects. It simplifies idea submission, voting, and prioritization while demonstrating a complete DevOps workflow with containerization and automated CI/CD.

## 🏗️ System Architecture

The application uses a Streamlit frontend to collect and display feedback. The frontend sends requests to a FastAPI backend, which stores data in a SQLite database. Docker is used for containerization, GitHub Actions manages CI/CD, and Docker Hub is used for deployment.

```
FeedVote/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── crud.py
│   │   └── routes/
│   │       ├── users.py
│   │       ├── feedback.py
│   │       └── vote.py
│   │
│   ├── tests/
│   │   ├── test_feedback.py
│   │   └── test_vote.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── README.md
└── LICENSE
```

## 🚀 CI/CD Pipeline Explanation

### ✅ Backend & Frontend Tests

The pipeline runs backend and frontend tests to validate API endpoints, database operations, and user interaction flows.

### 🔒 Security Scanning

Security scanning checks code and dependencies for vulnerabilities and exposed secrets using tools such as Bandit, Safety, and Trufflehog.

### 🐳 Docker Build & Validation

Docker build validates the backend and frontend container images and ensures the application can start successfully in the container environment.

### 🔗 Integration Testing

Integration testing uses Docker Compose to run backend, frontend, and database services together, verifying the full workflow end to end.

### 📦 Deployment

The final stage pushes the validated Docker image to Docker Hub so the application is available for deployment.

## 🌿 Git Workflow Used

The project follows a feature branch workflow. Developers create a feature branch, push changes, and open a pull request. The pull request triggers automated testing. Once tests pass, the branch is merged into main and deployment proceeds.

## 🛠️ Tools Used

| Tool | Purpose |
| --- | --- |
| ⚡ FastAPI | Backend API framework |
| 🎨 Streamlit | Frontend user interface |
| 🐳 Docker | Containerization runtime |
| 🎼 Docker Compose | Local service orchestration |
| 🤖 GitHub Actions | CI/CD automation |
| 📦 Docker Hub | Container image registry |
| 💾 SQLite | Lightweight relational database |

## 📸 Screenshots

### 🔹 Pipeline Success
![Pipeline Success](images/pipeline_success.png)

### 🔹 Deployment Output
![Deployment Output](images/deployment.png)

### 🔹 Application Running
![App Screenshot](images/frontend_running.png)

### 🔹 Deploy to Docker hub Job Success
![CI/CD Screenshot](images/deploy_job_success.png)

## ⚠️ Challenges Faced

* 1. CI/CD Configuration and Test Failures  

While setting up the CI/CD pipeline, tests occasionally failed due to configuration issues and environment mismatches.  
To debug these issues, we analyzed GitHub Actions logs, where each job and step provides detailed execution output. By identifying the exact failing step, we were able to fix dependency and configuration issues.

* 2. Git Push Rejection and Branch Sync Issues  
We encountered multiple "non-fast-forward" errors while pushing changes due to mismatches between local and remote branches. This helped us understand proper Git practices such as pulling latest changes, using pull requests, and maintaining a clean workflow without relying on unnecessary force pushes.

* 3. Source Code Management and Collaboration Control  
Initially, collaborators had direct access to the repository, which could lead to uncontrolled changes.  
To solve this, we defined a proper workflow and ruleset:

- All contributors work on separate feature branches  
- Changes are pushed to remote branches  
- Pull Requests are created for integration  
- Code is reviewed before merging into the main branch  
- Direct commits to main branch are restricted  

This improved overall source code management, ensured controlled collaboration, and enforced a structured development lifecycle.

* 4. Database File Tracked by Git (Security & Tracking Issue)  
Initially, when the project was pushed for the first time, the database file was also uploaded to GitHub. This created a serious security risk, as sensitive data and credentials could be exposed from the codebase.  

Additionally, tracking the database caused unnecessary issues:
- Every small data change was being tracked by Git  
- This resulted in unnecessary commits  
- It reduced repository cleanliness and increased noise  

To solve this, we used .gitignore to exclude the database file from version control.  
This ensured:
- Sensitive data remains secure  
- Git only tracks relevant source code  
- Avoids unnecessary commit history pollution

* 5. Docker Build Challenges  
While working with Docker, multiple issues were faced during image building due to missing dependencies and incorrect configurations.  
Initially, some dependencies were not properly installed and configurations were not up to date, which caused build failures.  

We resolved these issues by:
- Updating dependencies  
- Fixing Dockerfile configurations  
- Debugging using build logs step-by-step  

This improved our understanding of Docker image building and container behavior.

* 6. Local Deployment and CI/CD-Based Deployment Flow  
For learning and development purposes, the project is currently deployed locally using Docker.  

Additionally, we implemented a deployment job in the CI/CD pipeline:
- Deployment is triggered only after code is merged into the main branch  
- The pipeline first runs testing jobs  
- After successful validation, the deployment job builds Docker images  
- These images are then pushed to Docker Hub automatically  

This creates a semi-automated deployment workflow where:
- Code is tested before deployment  
- Images are consistently built and stored  
- The project becomes ready for future cloud deployment  

This approach serves as a foundational step towards full cloud deployment in the future.

# CI/CD Workflow Explanation for FeedVote

## Overview

This document explains the CI/CD workflow used by the FeedVote project. It is written for beginners and teachers, with simple language and clear steps.

CI/CD stands for Continuous Integration and Continuous Delivery. In this project, it means:

- Every time code is pushed to the `main` branch or a pull request is opened, the pipeline runs.
- The pipeline checks the code, builds the app, validates Docker, and runs tests.
- If anything fails, the pipeline stops and reports the problem.

## Why CI/CD is important

In real-world projects, CI/CD helps teams deliver better code faster. It:

- catches bugs early,
- makes sure the app still works after changes,
- avoids broken deployments,
- gives developers quick feedback,
- and helps keep code quality high.

For FeedVote, CI/CD ensures the backend, frontend, security, Docker builds, and integration tests are all verified automatically.

## High-level pipeline flow

1. Developer pushes code to `main`, or opens a pull request against `main`.
2. GitHub Actions starts the pipeline.
3. `backend-test` runs backend tests.
4. `frontend-test` checks frontend dependencies.
5. `security-scan` reviews code and dependencies for security issues.
6. `docker-build` builds Docker images and validates compose files.
7. `integration-test` starts the app with Docker Compose and checks it.
8. `status` summarizes whether everything passed.

If a step fails, later steps may stop running, and the pipeline reports the failure.

---

## Detailed workflow: job by job

### 1. backend-test

This job checks the backend code in the `backend/` folder.

#### What this job does

- checks out the source code
- sets up Python 3.10
- caches pip packages
- installs backend dependencies
- runs unit tests with `pytest`
- uploads test coverage reports
- runs `flake8` lint checks
- runs `pylint` analysis

#### Why each step is used

- `Checkout code`: downloads the project files so the pipeline can run on them.
- `Set up Python 3.10`: installs the Python version the backend uses.
- `Cache pip dependencies`: saves package downloads so future runs are faster.
- `Install dependencies`: installs the backend requirements.
- `Run tests with pytest`: confirms backend functions behave correctly.
- `Upload coverage reports`: stores test coverage data for later review.
- `Lint with flake8`: checks Python code for syntax and style issues.
- `Analyze with pylint`: performs deeper code analysis.

#### Step-by-step commands

- `python -m pip install --upgrade pip`
  - `python -m pip`: run pip through Python.
  - `install --upgrade pip`: updates pip itself.

- `pip install --upgrade packaging`
  - installs or updates the `packaging` package.

- `pip install -r requirements.txt`
  - installs all packages listed in `backend/requirements.txt`.

- `pytest tests/ -v --tb=short --cov=app --cov-report=xml --cov-report=html --cov-report=term`
  - `pytest tests/`: run tests in the `tests` folder.
  - `-v`: verbose output.
  - `--tb=short`: shorter failure traces.
  - `--cov=app`: measure coverage for the `app` package.
  - `--cov-report=xml`: write XML coverage file.
  - `--cov-report=html`: write HTML coverage report.
  - `--cov-report=term`: show coverage in the terminal.

- `pip install flake8`
  - installs the `flake8` linter.

- `flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics`
  - `app/`: check code in backend app folder.
  - `--count`: show number of issues.
  - `--select=E9,F63,F7,F82`: select only very serious errors.
  - `--show-source`: show the source code causing the problem.
  - `--statistics`: show a summary.

- `flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics`
  - `--exit-zero`: do not fail on warnings.
  - `--max-complexity=10`: warn for overly complex functions.
  - `--max-line-length=127`: allow lines up to 127 characters.

- `pip install pylint`
  - installs the `pylint` code analyzer.

- `pylint app/ --exit-zero --max-line-length=127 || true`
  - runs pylint on `app/`.
  - `--exit-zero`: always return success code so the job does not fail from pylint issues.
  - `|| true`: in Bash, ensures the command returns success even if pylint finds issues.

---

### 2. frontend-test

This job checks the frontend code in the `frontend/` folder.

#### What this job does

- checks out the source code
- sets up Python 3.10
- caches frontend pip packages
- installs frontend dependencies
- validates the Streamlit app environment

#### Why each step is used

- `Checkout code`: gets the frontend source files.
- `Set up Python 3.10`: uses the same Python version as the frontend.
- `Cache pip dependencies`: saves downloads from `pip`.
- `Install dependencies`: installs packages needed by the frontend.
- `Validate Streamlit app`: confirms Streamlit can import and run.

#### Step-by-step commands

- `python -m pip install --upgrade pip`
  - updates pip before installation.

- `pip install -r requirements.txt`
  - installs packages from `frontend/requirements.txt`.

- `streamlit config show`
  - prints Streamlit configuration to verify it is installed properly.

- `python -c "import streamlit; print('✓ Streamlit import successful')"`
  - runs a short Python command.
  - imports Streamlit and prints success.
  - if Streamlit cannot import, this step fails.

---

### 3. security-scan

This job inspects code and dependencies for security issues.

#### What this job does

- checks out the repository code
- sets up Python 3.10
- caches pip dependencies for security tools
- scans backend and frontend code with Bandit
- checks Python dependencies with Safety
- looks for hardcoded secrets with TruffleHog

#### Why each step is used

- `Bandit`: finds common Python security mistakes in code.
- `Safety`: scans installed packages for known vulnerabilities.
- `TruffleHog`: searches for leaked secrets or passwords in the repository.

#### Step-by-step commands

- `pip install bandit`
  - installs the Bandit security scanner.

- `bandit -r backend/app/ frontend/ -f screen -ll || true`
  - `-r backend/app/ frontend/`: scan these folders recursively.
  - `-f screen`: format output for the screen.
  - `-ll`: show low-level output.
  - `|| true`: do not fail the job if issues are found.

- `pip install safety`
  - installs the Safety vulnerability checker.

- `safety check --json || true`
  - checks installed dependencies for known insecure versions.
  - `--json`: prints results as JSON.
  - `|| true`: do not fail the job if vulnerabilities are found.

- `uses: trufflesecurity/trufflehog@main`
  - uses a GitHub Action to run TruffleHog.
  - checks the repository for secrets.

- `extra_args: --debug`
  - adds debug output for TruffleHog.

Note: In this workflow, security tools are allowed to report findings without failing the entire pipeline, because they are currently configured with `continue-on-error: true` or `|| true`.

---

### 4. docker-build

This job builds Docker images and validates Docker Compose files.

#### What this job does

- waits until `backend-test` and `frontend-test` finish successfully
- checks out the code again
- installs `docker-compose`
- builds the backend Docker image
- builds the frontend Docker image
- validates `docker-compose.yml`
- validates `docker-compose.prod.yml`
- prints Docker image sizes

#### Why each step is used

- `needs: [backend-test, frontend-test]`: ensures tests pass before building images.
- `docker build`: creates Docker images for backend and frontend.
- `docker-compose config`: checks that compose files are valid.
- checking image sizes: provides visibility into image weight.

#### Step-by-step commands

- `sudo apt-get update`
  - updates package lists on the Ubuntu machine.

- `sudo apt-get install -y docker-compose`
  - installs Docker Compose required to validate compose files.

- `docker build --tag ${{ env.BACKEND_IMAGE }}:latest --tag ${{ env.BACKEND_IMAGE }}:${{ github.sha }} --file backend/Dockerfile ./backend`
  - `docker build`: build a Docker image.
  - `--tag ...:latest`: tag the image as `feedvote-backend:latest`.
  - `--tag ...:${{ github.sha }}`: also tag the image with the current commit SHA.
  - `--file backend/Dockerfile`: use the backend Dockerfile.
  - `./backend`: build context is the backend folder.

- `docker build --tag ${{ env.FRONTEND_IMAGE }}:latest --tag ${{ env.FRONTEND_IMAGE }}:${{ github.sha }} --file frontend/Dockerfile ./frontend`
  - same process for the frontend image.

- `docker-compose config > /dev/null`
  - validates `docker-compose.yml` syntax.
  - `> /dev/null`: hides normal output.

- `docker-compose -f docker-compose.prod.yml config > /dev/null`
  - validates the production compose file.

- `docker images ${{ env.BACKEND_IMAGE }} --format "table {{.Repository}}\t{{.Size}}"`
  - lists the built backend image and size.

- `docker images ${{ env.FRONTEND_IMAGE }} --format "table {{.Repository}}\t{{.Size}}"`
  - lists the built frontend image and size.

---

### 5. integration-test

This job runs the app in Docker Compose and checks that it starts and responds correctly.

#### What this job does

- waits until `docker-build` finishes successfully
- checks out the code
- installs `docker-compose`
- builds test Docker images
- starts services in detached mode
- waits for the backend service to become healthy
- checks several API endpoints
- stops and removes services
- saves service logs as an artifact

#### Why each step is used

- `needs: docker-build`: ensures Docker images are available first.
- `docker-compose up -d`: starts the app in the background.
- `curl -f http://localhost:8000/...`: tests that the app responds at expected URLs.
- cleanup steps: stop containers and free resources.
- upload logs: save output for debugging if something fails.

#### Step-by-step commands

- `docker build -t feedvote-backend:test ./backend`
  - builds a backend image for testing.
  - `-t ...:test`: tag it with `:test`.

- `docker build -t feedvote-frontend:test ./frontend`
  - builds a frontend image for testing.

- `docker-compose up -d`
  - starts containers in detached mode.
  - `-d`: run containers in the background.

- `sleep 10`
  - waits 10 seconds for services to start.

- the backend health check loop:
  - tries `curl -f http://localhost:8000/health`
  - repeats up to 30 times
  - waits 2 seconds after each failed attempt
  - if the backend never responds, prints logs and fails.

- `curl -f http://localhost:8000/ || exit 1`
  - checks the root endpoint.
  - `-f`: fail if the HTTP response code is not successful.
  - `|| exit 1`: stop if the request fails.

- `curl -f http://localhost:8000/health || exit 1`
  - checks the health endpoint.

- `curl -f http://localhost:8000/docs || exit 1`
  - checks the documentation endpoint.

- `docker-compose down -v`
  - stops the containers.
  - removes volumes.

- `docker-compose logs > service-logs.txt || true`
  - saves logs to a file.
  - `|| true`: do not fail if log collection has issues.

- upload service logs as artifact
  - stores `service-logs.txt` so developers can download it.

---

### 6. status

This final job summarizes the pipeline.

#### What this job does

- waits for all previous jobs to finish
- checks each required job result
- fails if any required job failed
- prints a success message when everything passes

#### Why this step is used

- makes it easy to see whether the whole pipeline succeeded
- enforces that backend, frontend, Docker, and integration all passed
- provides a final pass/fail result for the run

#### Step-by-step commands

- `if [ "${{ needs.backend-test.result }}" != "success" ]; then ... fi`
  - checks whether `backend-test` passed.
  - if it did not pass, prints an error and exits with failure.

- the same pattern repeats for:
  - `frontend-test`
  - `docker-build`
  - `integration-test`

- `echo "✅ Pipeline completed successfully"`
  - prints success when everything was good.

- `echo "Commit: ${{ github.sha }}"`
  - shows the commit hash for this run.

- `echo "Branch: ${{ github.ref }}"`
  - shows the Git branch.

> Note: `security-scan` is not required by `status` here. It runs independently, but it still provides useful security information.

---

## What happens if a step fails

- If `backend-test` fails, the jobs that depend on it are blocked.
- If `frontend-test` fails, `docker-build` will still start only after `backend-test` and `frontend-test` succeed.
- If `docker-build` fails, `integration-test` cannot run.
- If `integration-test` fails, the final `status` job reports failure.
- The pipeline stops early for dependent jobs, saving time and making the failure easier to find.

In GitHub Actions, a failed step usually means:

- the job is marked as failed,
- later jobs depending on that job do not run,
- the developer gets a notification or sees the failure in the pull request.

## How to explain this in class

- Start with the overall goal: verify code automatically on every change.
- Explain the difference between tests, security checks, builds, and deployment validation.
- Show the pipeline order: test backend, test frontend, scan security, build Docker, run integration tests, then report status.
- Emphasize that CI/CD gives confidence before code is merged.

## Summary

This project uses a GitHub Actions pipeline to:

- verify backend code with Python tests,
- validate the frontend Streamlit app,
- scan for security issues,
- build Docker images,
- run the app in Docker Compose,
- and finally report success or failure.

The pipeline helps keep FeedVote stable, secure, and easy to maintain.

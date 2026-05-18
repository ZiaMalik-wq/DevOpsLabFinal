# DevOps Final Lab Exam - Viva Preparation Guide

This document summarizes exactly what we implemented for your Final Exam and the technical reasons behind our decisions. Use this to prepare for your Viva!

---

## 🏗️ What We Applied Today

### 1. Containerization & Docker Compose (Section A)
- **What we did:** We moved away from the cloud-based Supabase database and fully containerized the application. We created separate `Dockerfile`s for the frontend and backend, and used the official `postgres:15-alpine` image for the database.
- **Orchestration:** We created a `docker-compose.yml` to orchestrate all three containers so they can communicate over a shared internal Docker network (`app-network`).
- **Data Persistence:** We used a named Docker Volume (`db_data`) so that if the database container shuts down, your data isn't lost.

### 2. CI/CD Automation with GitHub Actions (Section B)
- **What we did:** We built a fully automated Continuous Integration and Continuous Deployment (CI/CD) pipeline in `.github/workflows/ci-cd.yml`.
- **How it works:** Every time you run `git push`, a GitHub server spins up, checks out your code, builds the new Docker images, pushes them to your Docker Hub account, and automatically deploys the updated code to your Azure Kubernetes cluster.
- **Security:** We used GitHub Secrets (`AZURE_CREDENTIALS`, `DOCKER_USERNAME`, etc.) so that sensitive passwords are not exposed in the codebase.

### 3. Kubernetes on Azure AKS (Section C)
- **What we did:** We deployed the application to a production Azure Kubernetes Service (AKS) cluster using `aks-deployment.yaml`.
- **The Reverse Proxy Solution (Crucial Concept):** Azure Student accounts have a strict quota limit (usually only 1 Public IP allowed). Because of this, we could not give both the frontend and the backend a Public IP. 
- **How we fixed it:** We configured Nginx inside the frontend container to act as a **Reverse Proxy**. The frontend took the 1 allowed Public IP (using a `LoadBalancer` service), while the backend was kept completely internal and secure (using a `ClusterIP` service). When a user sends a request to `/api`, Nginx silently forwards that request to the internal backend.
- **Bonus:** This architecture entirely eliminated **CORS (Cross-Origin Resource Sharing)** errors because the browser thinks the frontend and backend are hosted on the exact same domain!

### 4. Automated Testing with Selenium (Section D)
- **What we did:** We wrote an automated Python testing script (`test_app.py`) using the Selenium WebDriver.
- **How it works:** It launches a "headless" (invisible) Google Chrome browser, opens your application, and automatically verifies that the React page renders, the API connects successfully, and buttons are clickable.

---

## 🗣️ Potential Viva Questions & Answers

**Q1: Why did you use an Nginx Reverse Proxy instead of just giving the backend a Public IP?**
> **Answer:** "Because I am using an Azure Student subscription, which enforces a strict quota limit on Public IP addresses. To bypass this, I used Nginx in my frontend container to act as a reverse proxy. It routes all `/api` traffic internally to the backend. This is actually a highly professional DevOps architecture because it keeps the backend secure from the public internet and natively solves CORS issues."

**Q2: What is the difference between `LoadBalancer` and `ClusterIP` in your Kubernetes deployment?**
> **Answer:** "`LoadBalancer` provisions an external Public IP address from Azure so the application can be accessed from the internet (which I used for my frontend). `ClusterIP` only exposes the service internally within the Kubernetes cluster, which is what I used for my database and backend for security."

**Q3: How does your GitHub Actions CI/CD Pipeline authenticate with Azure?**
> **Answer:** "I created an Azure Service Principal with 'Contributor' role access to my Resource Group. I stored its JSON credentials securely in GitHub Secrets, which the pipeline uses to authenticate via the `azure/login` action before running `kubectl apply`."

**Q4: If your database container crashes or restarts, do you lose your data?**
> **Answer:** "No. In the `docker-compose.yml`, I mapped the PostgreSQL data directory to a named Docker Volume (`db_data`). Volumes are stored on the host machine, so the data persists entirely independently of the container lifecycle."

**Q5: What does the Selenium test script actually test?**
> **Answer:** "It tests the core user flows. It spins up a headless Chrome instance, waits for the React DOM to render to ensure the frontend works, checks the page source to guarantee no API network errors occurred (validating frontend-to-backend connectivity), and simulates finding and clicking a button."

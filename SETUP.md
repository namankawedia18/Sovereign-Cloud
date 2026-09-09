# Sovereign Cloud Storage System - Setup Guide

## Prerequisites

Install the following software before running the project:

### 1. Git

Download and install Git:

https://git-scm.com/downloads

Verify installation:

```bash
git --version
```

### 2. Docker Desktop

Download and install Docker Desktop:

https://www.docker.com/products/docker-desktop/

After installation:

* Start Docker Desktop
* Wait until Docker Engine is running

Verify installation:

```bash
docker --version
docker compose version
```

---

## Step 1: Clone the Repository

Open a terminal and run:

```bash
git clone <repository-url>
```

Move into the project folder:

```bash
cd CC-Project
```

---

## Step 2: Create Environment File

Create a file named:

```text
.env
```

Add the following content:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=sovereign_cloud

SECRET_KEY=sovereign_cloud_project_2026
```

**Important:**

* `DB_HOST` must be `db` when using Docker Compose.
* Do not use `localhost`.

---

## Step 3: Build Docker Containers

Run:

```bash
docker compose build
```

This may take a few minutes the first time.

---

## Step 4: Start the Application

Run:

```bash
docker compose up
```

Or run in background:

```bash
docker compose up -d
```

Docker will start:

1. PostgreSQL Database Container
2. Flask Application Container

---

## Step 5: Verify Containers

Check running containers:

```bash
docker ps
```

Expected containers:

```text
sovereign-app
sovereign-db
```

---

## Step 6: Access the Application

Open a browser and visit:

```text
http://localhost:5000
```

---

## Step 7: Create Database Tables

If this is the first time running the project:

```bash
docker compose exec web flask db upgrade
```

---

## Step 8: Seed Default Policies

Run:

```bash
docker compose exec web python seed_policies.py
```

This creates the default data-classification policies.

---

## Step 9: Create an Admin User

Register normally through the application.

Then enter PostgreSQL:

```bash
docker compose exec db psql -U postgres -d sovereign_cloud
```

Promote the user to admin:

```sql
UPDATE users
SET role='ADMIN'
WHERE username='YOUR_USERNAME';
```

Verify:

```sql
SELECT username, role FROM users;
```

Exit:

```sql
\q
```

Logout and login again.

---

## Useful Commands

### View Logs

```bash
docker compose logs -f
```

### View Application Logs

```bash
docker compose logs -f web
```

### View Database Logs

```bash
docker compose logs -f db
```

### Stop Containers

```bash
docker compose down
```

### Restart Containers

```bash
docker compose restart
```

### Rebuild After Code Changes

```bash
docker compose down
docker compose up --build
```

---

## Project Features

* User Authentication
* Role Based Access Control (RBAC)
* Policy-Based File Storage
* Region-Based Storage
* File Encryption
* File Decryption on Download
* Audit Logging
* PostgreSQL Database
* Dockerized Deployment

---

## Troubleshooting

### Database Connection Error

Ensure Docker Desktop is running:

```bash
docker ps
```

Verify database container:

```bash
docker compose ps
```

---

### Changes Not Reflecting

Rebuild containers:

```bash
docker compose down
docker compose up --build
```

---

### Port 5000 Already In Use

Stop the process using port 5000 or modify:

```yaml
ports:
  - "5001:5000"
```

Then access:

```text
http://localhost:5001
```

---

## Team Workflow

Pull latest changes:

```bash
git pull origin main
```

After pulling:

```bash
docker compose up --build
```

This ensures everyone runs the latest version of the project.

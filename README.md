# Sovereign Cloud

Sovereign Cloud is a Flask-based prototype for secure file storage with policy-based governance, role-based access control, and audit logging. The project is designed to demonstrate how sensitive data can be stored and managed under regional and classification-based controls.

## Features

- User authentication and registration
- Role-based access control (admin vs user)
- Policy-based file storage rules
- Region-aware file storage
- Encryption for protected file classifications
- User-specific file visibility and download access
- Audit logging for uploads and downloads
- Local development mode using SQLite by default

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or newer
- pip
- Git

## Clone the Repository

```bash
git clone <repository-url>
cd <project-folder>
```

## Create a Virtual Environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Configuration

The project works with SQLite by default, so no extra setup is required for local development.

If you want to use PostgreSQL locally instead, create a `.env` file in the project root with values like:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sovereign_cloud
SECRET_KEY=your_secret_key
```

If no database environment variables are set, the app will automatically use:

```text
sqlite:///local_dev.db
```

## Run the Application

Start the Flask app:

```bash
python app.py
```

Then open the app in your browser:

```text
http://127.0.0.1:5000
```

## Seed Default Policies

Before testing uploads, initialize the default data-classification policies:

```bash
python seed_policies.py
```

## Default Admin Login

A default admin account is available for testing:

- Email: `admin@sovereign.local`
- Password: `admin123`

## Sample User Login

You can also create a normal user via the registration page, or use the example user created during testing:

- Username: `sanjay`
- Email: `sanjay@example.com`
- Password: `pass123`

## Typical Workflow

1. Register or log in as a user.
2. Go to the Upload page.
3. Choose a file and classification.
4. The file is stored according to the policy for that classification.
5. View files in the My Files section.
6. Download only files owned by the logged-in user.
7. Log in as admin to manage policies and review activity.

## Useful Commands

### Run the app

```bash
python app.py
```

### Recreate database tables

```bash
flask db upgrade
```

### Seed policies

```bash
python seed_policies.py
```

## Project Structure

```text
app.py
config.py
controllers/
models/
services/
templates/
static/
seed_policies.py
requirements.txt
```

## Notes

- This is a local Flask development setup, not a Docker deployment setup.
- If you are running the app for the first time, the database will be created automatically.
- For demonstration purposes, policy seeding is required before file upload works correctly.

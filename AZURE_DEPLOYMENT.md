# Azure Deployment Guide

This project is now structured for Microsoft Azure cloud hosting.

## Azure services recommended

1. Azure App Service
   - Host the Flask app
   - Set environment variables in App Service Configuration > Application settings
   - Use a Linux or Windows runtime depending on your preference

2. Azure Database for PostgreSQL Flexible Server
   - Store the user, file metadata, and audit logs
   - Use a managed PostgreSQL instance instead of a local Docker database

3. Azure Blob Storage
   - Store uploaded files securely in the cloud
   - The project automatically uses Azure Blob Storage when `AZURE_STORAGE_USE_AZURE=true`

4. Azure Key Vault (recommended)
   - Store secrets like database passwords, storage keys, and app secrets
   - Best practice for production environments

## Required environment variables

Set these in Azure App Service:

```env
DATABASE_URL=postgresql://<user>:<password>@<server>.postgres.database.azure.com:5432/sovereign_cloud
SECRET_KEY=<strong-random-key>
AZURE_STORAGE_USE_AZURE=true
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=<account>;AccountKey=<key>;EndpointSuffix=core.windows.net
AZURE_STORAGE_CONTAINER_NAME=sovereign-cloud-files
PORT=8000
FLASK_DEBUG=false
```

## Azure setup steps

### 1. Create Azure resources

- Resource Group
- App Service Plan
- Web App
- Azure Database for PostgreSQL Flexible Server
- Azure Storage account with Blob Storage enabled

### 2. Configure the database

- Create a PostgreSQL database named `sovereign_cloud`
- Update the connection string in App Service settings
- Run the database migrations:

```bash
flask db upgrade
```

### 3. Configure Blob Storage

- Create a container named `sovereign-cloud-files`
- Grant access via connection string or account name + key
- Ensure the app environment variables are correctly set

### 4. Deploy the app

From the project root:

```bash
git init
git add .
git commit -m "Azure-ready deployment"
```

Then configure GitHub deployment or use Azure CLI / Visual Studio deployment to push the app to the App Service.

## Production best practices

- Use Azure Key Vault for secrets
- Enable HTTPS only
- Configure application logging in Azure Monitor
- Use Azure private networking or firewall rules for database access
- Keep uploaded files encrypted at rest with Azure Storage encryption
- Enable role-based access and audit controls

## Project cloud architecture

```text
User Browser
    -> Azure App Service (Flask app)
        -> Azure Database for PostgreSQL
        -> Azure Blob Storage
        -> Azure Key Vault (secrets)
```

This architecture moves the project from a local deployment model to a real cloud-native deployment pattern.

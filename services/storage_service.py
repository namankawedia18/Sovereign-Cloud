import os
from io import BytesIO

try:
    from azure.storage.blob import BlobServiceClient
except ImportError:  # pragma: no cover
    BlobServiceClient = None


def _azure_enabled():
    return (
        os.getenv("AZURE_STORAGE_USE_AZURE", "false").strip().lower() == "true"
        or bool(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
        or (
            os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
            and os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
        )
    )


def _blob_container_client():
    if not _azure_enabled() or BlobServiceClient is None:
        return None

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if connection_string:
        client = BlobServiceClient.from_connection_string(connection_string)
    else:
        account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
        client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=account_key,
        )

    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "sovereign-cloud-files")
    return client.get_container_client(container_name)


def _normalize_blob_name(storage_path):
    return storage_path.replace("\\", "/").lstrip("./")


def save_file(uploaded_file, storage_path):
    """Save a file to local disk or Azure Blob Storage depending on configuration."""
    if _azure_enabled():
        container_client = _blob_container_client()
        if container_client is None:
            raise RuntimeError("Azure Blob Storage is enabled but the SDK is not installed.")

        if hasattr(uploaded_file, "read"):
            data = uploaded_file.read()
        elif isinstance(uploaded_file, (bytes, bytearray)):
            data = bytes(uploaded_file)
        else:
            data = uploaded_file

        blob_name = _normalize_blob_name(storage_path)
        container_client.upload_blob(name=blob_name, data=data, overwrite=True)
        return blob_name

    directory = os.path.dirname(storage_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    if hasattr(uploaded_file, "save"):
        uploaded_file.save(storage_path)
    else:
        with open(storage_path, "wb") as file_handle:
            if hasattr(uploaded_file, "read"):
                file_handle.write(uploaded_file.read())
            else:
                file_handle.write(uploaded_file)

    return storage_path


def read_file_bytes(storage_path):
    if _azure_enabled():
        container_client = _blob_container_client()
        if container_client is None:
            raise RuntimeError("Azure Blob Storage is enabled but the SDK is not installed.")

        blob_name = _normalize_blob_name(storage_path)
        blob = container_client.get_blob_client(blob_name)
        if not blob.exists():
            raise FileNotFoundError(blob_name)
        return blob.download_blob().readall()

    with open(storage_path, "rb") as file_handle:
        return file_handle.read()


def file_exists(storage_path):
    if _azure_enabled():
        container_client = _blob_container_client()
        if container_client is None:
            return False

        blob_name = _normalize_blob_name(storage_path)
        return container_client.get_blob_client(blob_name).exists()

    return os.path.exists(storage_path)


def delete_file(storage_path):
    if _azure_enabled():
        container_client = _blob_container_client()
        if container_client is None:
            return

        blob_name = _normalize_blob_name(storage_path)
        container_client.delete_blob(blob_name, delete_snapshots="include")
        return

    if os.path.exists(storage_path):
        os.remove(storage_path)
import os


def save_file(uploaded_file, storage_path):
    """
    Save file to storage.
    Currently local storage.
    Later Azure Blob Storage.
    """

    uploaded_file.save(storage_path)

    return storage_path


def file_exists(storage_path):

    return os.path.exists(storage_path)


def delete_file(storage_path):

    if os.path.exists(storage_path):
        os.remove(storage_path)
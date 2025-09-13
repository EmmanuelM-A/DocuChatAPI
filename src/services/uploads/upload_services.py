"""
Responsible for all upload related operations.
"""

# TODO: NORMALIZE AND REVIEW TABLES
# TODO: SEPARATE USER TABLES INTO USER AND ACCOUNT


class FileUploadService:
    """Abstraction"""

    def __init__(self, dependencies):
        self.dependencies = dependencies

    def upload_file(self):
        """Handles file uploads"""

        # Receive upload request

        # Assign a unique file id

        # Validate file
        # - Allowed extension
        # - Max file size not exceeded
        # - Security checks (sanitize filename, check MIME type)

        # Pre-processing compression if file size exceeds MAX
        # - compress file
        # - store compressed file as the canonical raw file
        # - meta records og size + comp size
        # - FileCompressionService

        # Storage
        # - dev: on disks in users/ user123/ files/
        # - prod: upload external storage like AWS, S3
        # - Store meta in db table as well as content (opt) save_metadata()
        # - StorageAdapter: LocalStorageAdapter + CloudStorageAdapter depends on ENV

        """
            StorageAdapter:
            - save_file()
            - delete_file()
            - get_file(filename)
            - get_files()
        """
        # Return response
        # - File ID + metadata + storage URL/file path

    def upload_files(self):
        pass

    def get_user_files(self):
        pass

    def delete_file(self):
        pass

    def delete_files(self):
        pass

from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'
    # tell S3 to not override files with the same name.
    file_overwrite = False
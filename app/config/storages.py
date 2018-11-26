from storages.backends.s3boto3 import   S3Boto3Storage
# S3Boto3 Storage로 STATICFILES_STORAGE설정하신 분들은
# 해제하고 ROOT_DIR/.static 을 STATIC_ROOT로 사용하도록 수정

__all__ = (
    'S3DefaultStorage',
)


class S3DefaultStorage(S3Boto3Storage):
    location = 'media'
import logging
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


logger = logging.getLogger("supabase_storage")


class SupabaseStorage(S3Boto3Storage):
    """
    Supabase Storage backend using S3 compatibility layer
    but forcing correct PUBLIC URL generation.
    """

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    default_acl = None
    querystring_auth = False
    file_overwrite = False

    def exists(self, name):
        """
        Supabase S3 blocks HEAD requests used by django-storages.
        Always return False so Django skips the existence check.
        """
        return False
    
    def _normalize_name(self, name):
        return name.replace("\\", "/")

    def _get_client(self):
        """
        Create raw boto3 client for diagnostics.
        """
        return boto3.client(
            "s3",
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def check_connection(self):
        """
        Run diagnostics to detect configuration issues.
        """
        try:
            client = self._get_client()

            logger.info("🔎 Checking Supabase connection...")

            # 1️⃣ Check endpoint connectivity
            try:
                client.list_buckets()
                logger.info("✅ Supabase endpoint reachable")
            except EndpointConnectionError:
                logger.error("❌ Cannot reach Supabase endpoint")
                raise

            # 2️⃣ Check bucket existence
            try:
                client.head_bucket(Bucket=self.bucket_name)
                logger.info(f"✅ Bucket '{self.bucket_name}' exists")
            except ClientError as e:
                logger.error(f"❌ Bucket '{self.bucket_name}' not accessible")
                logger.error(e)
                raise

            # 3️⃣ Check write permission
            try:
                client.put_object(
                    Bucket=self.bucket_name,
                    Key="diagnostic_test.txt",
                    Body=b"test",
                )
                logger.info("✅ Write permission confirmed")
            except ClientError as e:
                logger.error("❌ Write permission denied")
                logger.error(e)
                raise

        except Exception as e:
            logger.error("❌ Supabase diagnostic failed:")
            logger.error(e)
            raise

    def url(self, name, parameters=None, expire=None):
        """
        Override URL generation to use Supabase PUBLIC endpoint
        instead of the private /s3/ endpoint.
        """
        name = self._normalize_name(name)

        return (
            f"{settings.SUPABASE_URL}"
            f"/storage/v1/object/public/"
            f"{self.bucket_name}/{name}"
        )
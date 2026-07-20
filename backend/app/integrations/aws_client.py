from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.core.config import settings

if TYPE_CHECKING:
    import boto3

logger = logging.getLogger(__name__)


class AWSClient:
    """
    Enterprise AWS Client

    Authentication Priority:
    1. Explicit credentials from .env
    2. IAM Role (EC2)
    3. AWS CLI credentials (~/.aws)
    """

    def __init__(self):
        self._session = None

    def _get_session(self):
        if self._session is None:
            try:
                import boto3
                session_kwargs = {"region_name": settings.AWS_REGION}
                if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
                    session_kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
                    session_kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
                self._session = boto3.Session(**session_kwargs)
            except ImportError:
                logger.error("boto3 not installed")
                raise
        return self._session

    # ==========================================================
    # AWS Clients
    # ==========================================================

    def ec2(self):
        return self.session.client("ec2")

    def s3(self):
        return self.session.client("s3")

    def iam(self):
        return self.session.client("iam")

    def sts(self):
        return self.session.client("sts")

    def rds(self):
        return self.session.client("rds")

    def cloudwatch(self):
        return self.session.client("cloudwatch")

    def autoscaling(self):
        return self.session.client("autoscaling")

    def elbv2(self):
        return self.session.client("elbv2")

    # ==========================================================
    # AWS Resources
    # ==========================================================

    def ec2_resource(self):
        return self.session.resource("ec2")

    def s3_resource(self):
        return self.session.resource("s3")


aws_client = AWSClient()
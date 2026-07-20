import logging

from typing import Any

from botocore.exceptions import ClientError
from app.integrations.aws_client import aws_client

logger = logging.getLogger(__name__)


class AWSService:
    def __init__(self):
        self.client = aws_client

    async def list_ec2_instances(self) -> list[dict]:
        try:
            ec2 = self.client.ec2()
            response = ec2.describe_instances()
            instances = []
            for reservation in response.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instances.append({
                        "instance_id": instance.get("InstanceId", ""),
                        "instance_type": instance.get("InstanceType", ""),
                        "state": instance.get("State", {}).get("Name", ""),
                        "public_ip": instance.get("PublicIpAddress", ""),
                        "private_ip": instance.get("PrivateIpAddress", ""),
                        "name": next(
                            (t["Value"] for t in instance.get("Tags", []) if t["Key"] == "Name"),
                            "",
                        ),
                        "launch_time": str(instance.get("LaunchTime", "")),
                    })
            return instances
        except Exception as e:
            logger.error(f"Failed to list EC2 instances: {e}")
            return []

    async def list_s3_buckets(self) -> list[dict]:
        try:
            s3 = self.client.s3()
            response = s3.list_buckets()
            buckets = []
            for bucket in response.get("Buckets", []):
                buckets.append({
                    "name": bucket.get("Name", ""),
                    "creation_date": str(bucket.get("CreationDate", "")),
                })
            return buckets
        except Exception as e:
            logger.error(f"Failed to list S3 buckets: {e}")
            return []

    async def list_vpcs(self) -> list[dict]:
        try:
            ec2 = self.client.ec2()
            response = ec2.describe_vpcs()
            vpcs = []
            for vpc in response.get("Vpcs", []):
                name = next(
                    (t["Value"] for t in vpc.get("Tags", []) if t["Key"] == "Name"),
                    "",
                )
                vpcs.append({
                    "vpc_id": vpc.get("VpcId", ""),
                    "cidr_block": vpc.get("CidrBlock", ""),
                    "state": vpc.get("State", ""),
                    "name": name,
                })
            return vpcs
        except Exception as e:
            logger.error(f"Failed to list VPCs: {e}")
            return []

    async def list_rds_instances(self) -> list[dict]:
        try:
            rds = self.client.rds()
            response = rds.describe_db_instances()
            instances = []
            for db in response.get("DBInstances", []):
                instances.append({
                    "db_instance_id": db.get("DBInstanceIdentifier", ""),
                    "engine": db.get("Engine", ""),
                    "status": db.get("DBInstanceStatus", ""),
                    "endpoint": db.get("Endpoint", {}).get("Address", ""),
                    "instance_class": db.get("DBInstanceClass", ""),
                })
            return instances
        except Exception as e:
            logger.error(f"Failed to list RDS instances: {e}")
            return []

    async def get_instance_status(self, instance_id: str) -> dict:
        try:
            ec2 = self.client.ec2()
            response = ec2.describe_instance_status(InstanceIds=[instance_id])
            statuses = response.get("InstanceStatuses", [])
            if statuses:
                status = statuses[0]
                return {
                    "instance_id": instance_id,
                    "system_status": status.get("SystemStatus", {}).get("Status", "unknown"),
                    "instance_status": status.get("InstanceStatus", {}).get("Status", "unknown"),
                }
            return {"instance_id": instance_id, "system_status": "unknown", "instance_status": "unknown"}
        except Exception as e:
            logger.error(f"Failed to get instance status for {instance_id}: {e}")
            return {"instance_id": instance_id, "system_status": "error", "instance_status": "error"}


    async def list_ec2_instances(self) -> list[dict]:
        """
        List all EC2 instances.
        """

        try:
            ec2 = self.client.ec2()

            paginator = ec2.get_paginator("describe_instances")

            instances = []

            for page in paginator.paginate():

                for reservation in page.get("Reservations", []):

                    for instance in reservation.get("Instances", []):

                        name = ""

                        for tag in instance.get("Tags", []):

                            if tag["Key"] == "Name":
                                name = tag["Value"]

                        instances.append(
                            {
                                "instance_id": instance.get("InstanceId"),
                                "name": name,
                                "instance_type": instance.get("InstanceType"),
                                "state": instance.get("State", {}).get("Name"),
                                "public_ip": instance.get("PublicIpAddress"),
                                "private_ip": instance.get("PrivateIpAddress"),
                                "public_dns": instance.get("PublicDnsName"),
                                "private_dns": instance.get("PrivateDnsName"),
                                "availability_zone": instance.get(
                                    "Placement", {}
                                ).get("AvailabilityZone"),
                                "launch_time": str(
                                    instance.get("LaunchTime")
                                ),
                            }
                        )

            return instances

        except Exception as e:
            logger.exception(e)
            return []

    async def get_instance(
        self,
        instance_id: str,
    ) -> dict:

        try:

            ec2 = self.client.ec2()

            response = ec2.describe_instances(
                InstanceIds=[instance_id]
            )

            reservations = response.get("Reservations", [])

            if not reservations:
                return {}

            instance = reservations[0]["Instances"][0]

            tags = {
                tag["Key"]: tag["Value"]
                for tag in instance.get("Tags", [])
            }

            return {
                "instance_id": instance["InstanceId"],
                "name": tags.get("Name"),
                "instance_type": instance["InstanceType"],
                "state": instance["State"]["Name"],
                "public_ip": instance.get("PublicIpAddress"),
                "private_ip": instance.get("PrivateIpAddress"),
                "public_dns": instance.get("PublicDnsName"),
                "private_dns": instance.get("PrivateDnsName"),
                "subnet_id": instance.get("SubnetId"),
                "vpc_id": instance.get("VpcId"),
                "security_groups": instance.get("SecurityGroups"),
                "launch_time": str(instance.get("LaunchTime")),
                "tags": tags,
            }

        except ClientError as e:

            logger.error(e)

            return {}

    async def get_instance_status(
        self,
        instance_id: str,
    ) -> dict:

        try:

            ec2 = self.client.ec2()

            response = ec2.describe_instance_status(
                InstanceIds=[instance_id],
                IncludeAllInstances=True,
            )

            statuses = response.get(
                "InstanceStatuses",
                [],
            )

            if not statuses:

                return {
                    "instance_id": instance_id,
                    "status": "unknown",
                }

            status = statuses[0]

            return {
                "instance_id": instance_id,
                "state": status["InstanceState"]["Name"],
                "system_status": status["SystemStatus"]["Status"],
                "instance_status": status["InstanceStatus"]["Status"],
            }

        except ClientError as e:

            logger.error(e)

            return {}

    async def start_instance(
        self,
        instance_id: str,
    ) -> bool:

        try:

            ec2 = self.client.ec2()

            ec2.start_instances(
                InstanceIds=[instance_id]
            )

            logger.info(
                "Started EC2 instance %s",
                instance_id,
            )

            return True

        except ClientError as e:

            logger.error(e)

            return False

    async def stop_instance(
        self,
        instance_id: str,
    ) -> bool:

        try:

            ec2 = self.client.ec2()

            ec2.stop_instances(
                InstanceIds=[instance_id]
            )

            logger.info(
                "Stopped EC2 instance %s",
                instance_id,
            )

            return True

        except ClientError as e:

            logger.error(e)

            return False

    async def reboot_instance(
        self,
        instance_id: str,
    ) -> bool:

        try:

            ec2 = self.client.ec2()

            ec2.reboot_instances(
                InstanceIds=[instance_id]
            )

            logger.info(
                "Rebooted EC2 instance %s",
                instance_id,
            )

            return True

        except ClientError as e:

            logger.error(e)

            return False

    async def terminate_instance(
        self,
        instance_id: str,
    ) -> bool:

        try:

            ec2 = self.client.ec2()

            ec2.terminate_instances(
                InstanceIds=[instance_id]
            )

            logger.info(
                "Terminated EC2 instance %s",
                instance_id,
            )

            return True

        except ClientError as e:

            logger.error(e)

            return False

    async def list_security_groups(self) -> list[dict]:

        try:

            ec2 = self.client.ec2()

            response = ec2.describe_security_groups()

            groups = []

            for sg in response["SecurityGroups"]:

                groups.append(
                    {
                        "group_id": sg["GroupId"],
                        "group_name": sg["GroupName"],
                        "description": sg["Description"],
                        "vpc_id": sg.get("VpcId"),
                    }
                )

            return groups

        except ClientError as e:

            logger.error(e)

            return []

    async def list_key_pairs(self) -> list[dict]:

        try:

            ec2 = self.client.ec2()

            response = ec2.describe_key_pairs()

            keys = []

            for key in response["KeyPairs"]:

                keys.append(
                    {
                        "name": key["KeyName"],
                        "key_pair_id": key["KeyPairId"],
                        "fingerprint": key["KeyFingerprint"],
                    }
                )

            return keys

        except ClientError as e:

            logger.error(e)

            return []

    async def list_instance_types(self) -> list[str]:

        try:

            ec2 = self.client.ec2()

            response = ec2.describe_instance_types(
                MaxResults=100
            )

            return [
                i["InstanceType"]
                for i in response["InstanceTypes"]
            ]

        except ClientError as e:

            logger.error(e)

            return []

    # ==========================================================
    # S3
    # ==========================================================

    async def list_s3_buckets(self) -> list[dict]:
        """
        List all S3 buckets.
        """

        try:

            s3 = self.client.s3()

            response = s3.list_buckets()

            buckets = []

            for bucket in response.get("Buckets", []):

                bucket_name = bucket["Name"]

                try:
                    location = s3.get_bucket_location(
                        Bucket=bucket_name
                    ).get("LocationConstraint")

                    if location is None:
                        location = "us-east-1"

                except ClientError:
                    location = "unknown"

                buckets.append(
                    {
                        "name": bucket_name,
                        "creation_date": str(
                            bucket.get("CreationDate")
                        ),
                        "region": location,
                    }
                )

            return buckets

        except ClientError as e:

            logger.error(e)

            return []

    async def get_bucket(
        self,
        bucket_name: str,
    ) -> dict:
        """
        Get bucket details.
        """

        try:

            s3 = self.client.s3()

            location = s3.get_bucket_location(
                Bucket=bucket_name
            ).get("LocationConstraint")

            if location is None:
                location = "us-east-1"

            return {
                "bucket": bucket_name,
                "region": location,
                "versioning": await self.get_bucket_versioning(
                    bucket_name
                ),
                "encryption": await self.get_bucket_encryption(
                    bucket_name
                ),
                "public_access": await self.get_bucket_public_access(
                    bucket_name
                ),
            }

        except ClientError as e:

            logger.error(e)

            return {}

    async def list_bucket_objects(
        self,
        bucket_name: str,
        max_keys: int = 100,
    ) -> list[dict]:
        """
        List bucket objects.
        """

        try:

            s3 = self.client.s3()

            response = s3.list_objects_v2(
                Bucket=bucket_name,
                MaxKeys=max_keys,
            )

            objects = []

            for obj in response.get("Contents", []):

                objects.append(
                    {
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "etag": obj["ETag"],
                        "last_modified": str(
                            obj["LastModified"]
                        ),
                        "storage_class": obj["StorageClass"],
                    }
                )

            return objects

        except ClientError as e:

            logger.error(e)

            return []

    async def get_bucket_location(
        self,
        bucket_name: str,
    ) -> str:

        try:

            s3 = self.client.s3()

            response = s3.get_bucket_location(
                Bucket=bucket_name
            )

            location = response.get(
                "LocationConstraint"
            )

            return location or "us-east-1"

        except ClientError as e:

            logger.error(e)

            return "unknown"

    async def get_bucket_versioning(
        self,
        bucket_name: str,
    ) -> dict:

        try:

            s3 = self.client.s3()

            response = s3.get_bucket_versioning(
                Bucket=bucket_name
            )

            return {
                "status": response.get(
                    "Status",
                    "Disabled",
                )
            }

        except ClientError as e:

            logger.error(e)

            return {
                "status": "Unknown"
            }

    async def get_bucket_encryption(
        self,
        bucket_name: str,
    ) -> dict:

        try:

            s3 = self.client.s3()

            response = s3.get_bucket_encryption(
                Bucket=bucket_name
            )

            rules = response[
                "ServerSideEncryptionConfiguration"
            ]["Rules"]

            return {
                "enabled": True,
                "algorithm": rules[0][
                    "ApplyServerSideEncryptionByDefault"
                ]["SSEAlgorithm"],
            }

        except ClientError:

            return {
                "enabled": False,
                "algorithm": None,
            }

    async def get_bucket_public_access(
        self,
        bucket_name: str,
    ) -> dict:

        try:

            s3 = self.client.s3()

            response = s3.get_public_access_block(
                Bucket=bucket_name
            )

            return response[
                "PublicAccessBlockConfiguration"
            ]

        except ClientError:

            return {
                "BlockPublicAcls": False,
                "IgnorePublicAcls": False,
                "BlockPublicPolicy": False,
                "RestrictPublicBuckets": False,
            }

    async def bucket_exists(
        self,
        bucket_name: str,
    ) -> bool:

        try:

            s3 = self.client.s3()

            s3.head_bucket(
                Bucket=bucket_name
            )

            return True

        except ClientError:

            return False

    async def get_bucket_size(
        self,
        bucket_name: str,
    ) -> dict:
        """
        Approximate bucket size by listing objects.
        """

        try:

            s3 = self.client.s3()

            paginator = s3.get_paginator(
                "list_objects_v2"
            )

            total_size = 0
            total_objects = 0

            for page in paginator.paginate(
                Bucket=bucket_name
            ):

                for obj in page.get(
                    "Contents",
                    [],
                ):

                    total_size += obj["Size"]
                    total_objects += 1

            return {
                "bucket": bucket_name,
                "objects": total_objects,
                "size_bytes": total_size,
                "size_mb": round(
                    total_size / (1024 * 1024),
                    2,
                ),
                "size_gb": round(
                    total_size / (1024 * 1024 * 1024),
                    2,
                ),
            }

        except ClientError as e:

            logger.error(e)

            return {}

    async def delete_bucket(
        self,
        bucket_name: str,
    ) -> bool:

        try:

            s3 = self.client.s3()

            s3.delete_bucket(
                Bucket=bucket_name
            )

            logger.info(
                "Deleted bucket %s",
                bucket_name,
            )

            return True

        except ClientError as e:

            logger.error(e)

            return False

    # ==========================================================
    # VPC
    # ==========================================================

    async def list_vpcs(self) -> list[dict]:
        """
        List all VPCs.
        """

        try:

            ec2 = self.client.ec2()

            response = ec2.describe_vpcs()

            vpcs = []

            for vpc in response.get("Vpcs", []):

                tags = {
                    tag["Key"]: tag["Value"]
                    for tag in vpc.get("Tags", [])
                }

                vpcs.append(
                    {
                        "vpc_id": vpc["VpcId"],
                        "name": tags.get("Name", ""),
                        "cidr_block": vpc["CidrBlock"],
                        "state": vpc["State"],
                        "is_default": vpc["IsDefault"],
                        "owner_id": vpc.get("OwnerId"),
                    }
                )

            return vpcs

        except ClientError as e:

            logger.error(e)

            return []

    async def get_vpc(
        self,
        vpc_id: str,
    ) -> dict:
        """
        Get VPC details.
        """

        try:

            ec2 = self.client.ec2()

            response = ec2.describe_vpcs(
                VpcIds=[vpc_id]
            )

            if not response["Vpcs"]:
                return {}

            vpc = response["Vpcs"][0]

            tags = {
                tag["Key"]: tag["Value"]
                for tag in vpc.get("Tags", [])
            }

            return {
                "vpc_id": vpc["VpcId"],
                "name": tags.get("Name", ""),
                "cidr_block": vpc["CidrBlock"],
                "state": vpc["State"],
                "is_default": vpc["IsDefault"],
                "owner_id": vpc.get("OwnerId"),
            }

        except ClientError as e:

            logger.error(e)

            return {}

    async def list_subnets(
        self,
        vpc_id: str | None = None,
    ) -> list[dict]:
        """
        List all subnets.
        """

        try:

            ec2 = self.client.ec2()

            kwargs = {}

            if vpc_id:
                kwargs["Filters"] = [
                    {
                        "Name": "vpc-id",
                        "Values": [vpc_id],
                    }
                ]

            response = ec2.describe_subnets(**kwargs)

            subnets = []

            for subnet in response["Subnets"]:

                tags = {
                    tag["Key"]: tag["Value"]
                    for tag in subnet.get("Tags", [])
                }

                subnets.append(
                    {
                        "subnet_id": subnet["SubnetId"],
                        "name": tags.get("Name", ""),
                        "vpc_id": subnet["VpcId"],
                        "cidr_block": subnet["CidrBlock"],
                        "availability_zone": subnet["AvailabilityZone"],
                        "available_ips": subnet["AvailableIpAddressCount"],
                        "public": subnet.get(
                            "MapPublicIpOnLaunch",
                            False,
                        ),
                    }
                )

            return subnets

        except ClientError as e:

            logger.error(e)

            return []

    async def list_route_tables(
        self,
        vpc_id: str | None = None,
    ) -> list[dict]:
        """
        List Route Tables.
        """

        try:

            ec2 = self.client.ec2()

            kwargs = {}

            if vpc_id:
                kwargs["Filters"] = [
                    {
                        "Name": "vpc-id",
                        "Values": [vpc_id],
                    }
                ]

            response = ec2.describe_route_tables(
                **kwargs
            )

            tables = []

            for table in response["RouteTables"]:

                tags = {
                    tag["Key"]: tag["Value"]
                    for tag in table.get("Tags", [])
                }

                tables.append(
                    {
                        "route_table_id": table["RouteTableId"],
                        "name": tags.get("Name", ""),
                        "vpc_id": table["VpcId"],
                        "routes": len(
                            table.get("Routes", [])
                        ),
                        "associations": len(
                            table.get(
                                "Associations",
                                [],
                            )
                        ),
                    }
                )

            return tables

        except ClientError as e:

            logger.error(e)

            return []

    async def list_security_groups(
        self,
        vpc_id: str | None = None,
    ) -> list[dict]:
        """
        List Security Groups.
        """

        try:

            ec2 = self.client.ec2()

            kwargs = {}

            if vpc_id:
                kwargs["Filters"] = [
                    {
                        "Name": "vpc-id",
                        "Values": [vpc_id],
                    }
                ]

            response = ec2.describe_security_groups(
                **kwargs
            )

            groups = []

            for sg in response["SecurityGroups"]:

                groups.append(
                    {
                        "group_id": sg["GroupId"],
                        "group_name": sg["GroupName"],
                        "description": sg["Description"],
                        "vpc_id": sg["VpcId"],
                        "ingress_rules": len(
                            sg.get(
                                "IpPermissions",
                                [],
                            )
                        ),
                        "egress_rules": len(
                            sg.get(
                                "IpPermissionsEgress",
                                [],
                            )
                        ),
                    }
                )

            return groups

        except ClientError as e:

            logger.error(e)

            return []

    async def list_internet_gateways(
        self,
        vpc_id: str | None = None,
    ) -> list[dict]:
        """
        List Internet Gateways.
        """

        try:

            ec2 = self.client.ec2()

            kwargs = {}

            if vpc_id:
                kwargs["Filters"] = [
                    {
                        "Name": "attachment.vpc-id",
                        "Values": [vpc_id],
                    }
                ]

            response = ec2.describe_internet_gateways(
                **kwargs
            )

            gateways = []

            for igw in response["InternetGateways"]:

                gateways.append(
                    {
                        "internet_gateway_id": igw[
                            "InternetGatewayId"
                        ],
                        "attachments": igw.get(
                            "Attachments",
                            [],
                        ),
                    }
                )

            return gateways

        except ClientError as e:

            logger.error(e)

            return []

    async def list_nat_gateways(
        self,
        vpc_id: str | None = None,
    ) -> list[dict]:
        """
        List NAT Gateways.
        """

        try:

            ec2 = self.client.ec2()

            kwargs = {}

            if vpc_id:
                kwargs["Filter"] = [
                    {
                        "Name": "vpc-id",
                        "Values": [vpc_id],
                    }
                ]

            response = ec2.describe_nat_gateways(
                **kwargs
            )

            gateways = []

            for nat in response["NatGateways"]:

                gateways.append(
                    {
                        "nat_gateway_id": nat[
                            "NatGatewayId"
                        ],
                        "vpc_id": nat["VpcId"],
                        "subnet_id": nat["SubnetId"],
                        "state": nat["State"],
                        "public_ips": [
                            address["PublicIp"]
                            for address in nat.get(
                                "NatGatewayAddresses",
                                [],
                            )
                            if "PublicIp" in address
                        ],
                    }
                )

            return gateways

        except ClientError as e:

            logger.error(e)

            return []


aws_service = AWSService()

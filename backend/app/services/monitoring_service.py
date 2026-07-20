import logging
from datetime import datetime, timedelta, timezone

from app.integrations.aws_client import aws_client

logger = logging.getLogger(__name__)


class MonitoringService:
    def __init__(self):
        self.client = aws_client

    def _get_metric_statistics(self, namespace: str, metric_name: str, dimensions: list[dict], period: int = 300) -> list[dict]:
        try:
            cw = self.client.cloudwatch()
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(hours=1)
            response = cw.get_metric_statistics(
                Namespace=namespace,
                MetricName=metric_name,
                Dimensions=dimensions,
                StartTime=start_time,
                EndTime=end_time,
                Period=period,
                Statistics=["Average"],
            )
            return [
                {"timestamp": dp["Timestamp"].isoformat(), "value": round(dp["Average"], 2)}
                for dp in sorted(response.get("Datapoints", []), key=lambda x: x["Timestamp"])
            ]
        except Exception as e:
            logger.error(f"Failed to get metric {metric_name}: {e}")
            return []

    async def get_cpu_metrics(self, instance_id: str, period: int = 300) -> list[dict]:
        return self._get_metric_statistics(
            namespace="AWS/EC2",
            metric_name="CPUUtilization",
            dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            period=period,
        )

    async def get_memory_metrics(self, instance_id: str) -> list[dict]:
        return self._get_metric_statistics(
            namespace="CWAgent",
            metric_name="mem_used_percent",
            dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            period=300,
        )

    async def get_disk_metrics(self, instance_id: str) -> list[dict]:
        return self._get_metric_statistics(
            namespace="CWAgent",
            metric_name="disk_used_percent",
            dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            period=300,
        )

    async def get_all_metrics(self, instance_id: str) -> dict:
        cpu = await self.get_cpu_metrics(instance_id)
        memory = await self.get_memory_metrics(instance_id)
        disk = await self.get_disk_metrics(instance_id)
        return {
            "instance_id": instance_id,
            "cpu": cpu,
            "memory": memory,
            "disk": disk,
        }

    async def get_terraform_status(self) -> dict:
        return {
            "running": False,
            "active_workspaces": [],
            "last_execution": datetime.now(timezone.utc).isoformat(),
        }


monitoring_service = MonitoringService()

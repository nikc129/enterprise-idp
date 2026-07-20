import logging
from typing import Any

import docker

logger = logging.getLogger(__name__)


class DockerClient:
    def __init__(self):
        try:
            self.client = docker.from_env()
            self.available = True
        except Exception as e:
            logger.warning(f"Docker not available: {e}")
            self.client = None
            self.available = False

    def list_containers(self, all: bool = True) -> list[dict]:
        if not self.available:
            return []
        try:
            containers = self.client.containers.list(all=all)
            return [
                {
                    "id": c.id[:12],
                    "name": c.name,
                    "status": c.status,
                    "image": c.image.tags[0] if c.image.tags else str(c.image.id)[:12],
                    "created": c.attrs.get("Created", ""),
                    "ports": self._format_ports(c),
                }
                for c in containers
            ]
        except Exception as e:
            logger.error(f"Failed to list containers: {e}")
            return []

    def get_container(self, container_id: str) -> dict | None:
        if not self.available:
            return None
        try:
            c = self.client.containers.get(container_id)
            return {
                "id": c.id[:12],
                "name": c.name,
                "status": c.status,
                "image": c.image.tags[0] if c.image.tags else str(c.image.id)[:12],
                "created": c.attrs.get("Created", ""),
                "ports": self._format_ports(c),
            }
        except docker.errors.NotFound:
            return None
        except Exception as e:
            logger.error(f"Failed to get container {container_id}: {e}")
            return None

    def get_container_logs(self, container_id: str, tail: int = 100) -> str:
        if not self.available:
            return "Docker not available"
        try:
            c = self.client.containers.get(container_id)
            logs = c.logs(tail=tail, timestamps=True).decode("utf-8", errors="replace")
            return logs
        except Exception as e:
            logger.error(f"Failed to get logs for {container_id}: {e}")
            return f"Error: {e}"

    def get_container_stats(self, container_id: str) -> dict:
        if not self.available:
            return {}
        try:
            c = self.client.containers.get(container_id)
            stats = c.stats(stream=False)
            return self._parse_stats(stats)
        except Exception as e:
            logger.error(f"Failed to get stats for {container_id}: {e}")
            return {}

    def get_docker_info(self) -> dict:
        if not self.available:
            return {"available": False}
        try:
            info = self.client.info()
            return {
                "available": True,
                "containers_running": info.get("ContainersRunning", 0),
                "containers_stopped": info.get("ContainersStopped", 0),
                "containers_paused": info.get("ContainersPaused", 0),
                "images": info.get("Images", 0),
                "docker_version": info.get("ServerVersion", "unknown"),
            }
        except Exception as e:
            return {"available": False, "error": str(e)}

    def _format_ports(self, container) -> str:
        ports = container.ports
        if not ports:
            return ""
        parts = []
        for container_port, host_bindings in ports.items():
            if host_bindings:
                for binding in host_bindings:
                    parts.append(f"{binding.get('HostIp', '')}:{binding.get('HostPort', '')}->{container_port}")
            else:
                parts.append(container_port)
        return ", ".join(parts)

    def _parse_stats(self, stats: dict) -> dict:
        result = {}
        cpu_stats = stats.get("cpu_stats", {})
        precpu_stats = stats.get("precpu_stats", {})
        cpu_delta = cpu_stats.get("cpu_usage", {}).get("total_usage", 0) - \
                    precpu_stats.get("cpu_usage", {}).get("total_usage", 0)
        system_delta = cpu_stats.get("system_cpu_usage", 0) - \
                       precpu_stats.get("system_cpu_usage", 0)
        num_cpus = cpu_stats.get("online_cpus", 1)
        if system_delta > 0:
            result["cpu_percent"] = round((cpu_delta / system_delta) * num_cpus * 100, 2)

        memory_stats = stats.get("memory_stats", {})
        usage = memory_stats.get("usage", 0)
        limit = memory_stats.get("limit", 1)
        result["memory_usage_mb"] = round(usage / (1024 * 1024), 2)
        result["memory_limit_mb"] = round(limit / (1024 * 1024), 2)
        result["memory_percent"] = round((usage / limit) * 100, 2)

        return result
    
    def start_container(self, container_id: str) -> bool:
        if not self.available:
            return False

        try:
            self.client.containers.get(container_id).start()
            return True
        except Exception as e:
            logger.error(f"Failed to start container: {e}")
            return False
    def stop_container(self, container_id: str) -> bool:
        if not self.available:
            return False

        try:
            self.client.containers.get(container_id).stop()
            return True
        except Exception as e:
            logger.error(f"Failed to stop container: {e}")
            return False
    def restart_container(self, container_id: str) -> bool:
        if not self.available:
            return False

        try:
            self.client.containers.get(container_id).restart()
            return True
        except Exception as e:
            logger.error(f"Failed to restart container: {e}")
            return False

    def remove_container(self, container_id: str, force: bool = False) -> bool:
        if not self.available:
            return False

        try:
            self.client.containers.get(container_id).remove(force=force)
            return True
        except Exception as e:
            logger.error(f"Failed to remove container: {e}")
            return False

    def list_images(self) -> list[dict]:
        if not self.available:
            return []

        try:
            images = self.client.images.list()

            return [
                {
                    "id": image.id[:12],
                    "tags": image.tags,
                    "created": image.attrs.get("Created"),
                    "size": image.attrs.get("Size"),
                }
                for image in images
            ]

        except Exception as e:
            logger.error(f"Failed to list images: {e}")
            return [] 

    def pull_image(self, image: str) -> bool:
        if not self.available:
            return False

        try:
            self.client.images.pull(image)
            return True
        except Exception as e:
            logger.error(f"Failed to pull image: {e}")
            return False

    def list_networks(self) -> list[dict]:
        if not self.available:
            return []

        try:
            return [
                {
                    "id": network.id,
                    "name": network.name,
                    "driver": network.attrs["Driver"],
                    "scope": network.attrs["Scope"],
                }
                for network in self.client.networks.list()
            ]
        except Exception as e:
            logger.error(f"Failed to list networks: {e}")
            return []
    
    def list_volumes(self) -> list[dict]:
        if not self.available:
            return []

        try:
            volumes = self.client.volumes.list()

            return [
                {
                    "name": volume.name,
                    "driver": volume.attrs["Driver"],
                    "mountpoint": volume.attrs["Mountpoint"],
                }
                for volume in volumes
            ]

        except Exception as e:
            logger.error(f"Failed to list volumes: {e}")
            return []



docker_client = DockerClient()

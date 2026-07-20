import logging

from app.integrations.docker_client import docker_client

logger = logging.getLogger(__name__)


class DockerService:
    """
    Docker Service

    Business layer for Docker operations.
    """

    def __init__(self):
        self.client = docker_client

    # ==========================================================
    # Docker Information
    # ==========================================================

    def get_docker_info(self) -> dict:
        return self.client.get_docker_info()

    def get_version(self) -> dict:
        return self.client.get_version()

    # ==========================================================
    # Containers
    # ==========================================================

    def list_containers(
        self,
        all: bool = True,
    ) -> list[dict]:
        return self.client.list_containers(all=all)

    def get_container(
        self,
        container_id: str,
    ) -> dict:
        return self.client.get_container(container_id)

    def get_container_logs(
        self,
        container_id: str,
        lines: int = 100,
    ) -> str:
        return self.client.get_container_logs(
            container_id,
            tail=lines,
        )

    def get_container_stats(
        self,
        container_id: str,
    ) -> dict:
        return self.client.get_container_stats(container_id)

    def start_container(
        self,
        container_id: str,
    ) -> bool:
        return self.client.start_container(container_id)

    def stop_container(
        self,
        container_id: str,
    ) -> bool:
        return self.client.stop_container(container_id)

    def restart_container(
        self,
        container_id: str,
    ) -> bool:
        return self.client.restart_container(container_id)

    def remove_container(
        self,
        container_id: str,
        force: bool = False,
    ) -> bool:
        return self.client.remove_container(
            container_id,
            force=force,
        )

    # ==========================================================
    # Images
    # ==========================================================

    def list_images(self) -> list[dict]:
        return self.client.list_images()

    def pull_image(
        self,
        image: str,
    ) -> bool:
        return self.client.pull_image(image)

    def remove_image(
        self,
        image: str,
        force: bool = False,
    ) -> bool:
        return self.client.remove_image(
            image,
            force=force,
        )

    # ==========================================================
    # Networks
    # ==========================================================

    def list_networks(self) -> list[dict]:
        return self.client.list_networks()

    # ==========================================================
    # Volumes
    # ==========================================================

    def list_volumes(self) -> list[dict]:
        return self.client.list_volumes()

    # ==========================================================
    # Health
    # ==========================================================

    def ping(self) -> bool:
        return self.client.ping()


docker_service = DockerService()
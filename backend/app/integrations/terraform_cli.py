import asyncio
import logging
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger(__name__)


class TerraformCLI:
    """
    Enterprise Terraform CLI Wrapper

    Responsible only for executing Terraform commands.

    Project Structure:

    enterprise-idp/
    ├── terraform/
    │   ├── bootstrap/
    │   ├── environments/
    │   │   ├── dev/
    │   │   ├── stage/
    │   │   └── prod/
    │   └── modules/

    Examples:

        await terraform_cli.init("dev")
        await terraform_cli.plan("dev")
        await terraform_cli.apply("dev")
        await terraform_cli.destroy("dev")
    """

    def __init__(self):
        self.binary = settings.TERRAFORM_BINARY

    # ==========================================================
    # Helpers
    # ==========================================================

    def _environment_path(self, environment: str) -> Path:
        """
        Resolve terraform environment directory.
        """

        path = Path(settings.TERRAFORM_ENVIRONMENTS_DIR) / environment

        if not path.exists():
            raise FileNotFoundError(
                f"Terraform environment not found: {path}"
            )

        return path

    async def _run(
        self,
        cmd: list[str],
        cwd: Path,
    ) -> tuple[int, str, str]:

        logger.info(
            "Running command: %s",
            " ".join(cmd),
        )

        logger.info(
            "Working directory: %s",
            cwd,
        )

        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=str(cwd),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        stdout_str = stdout.decode(
            "utf-8",
            errors="replace",
        )

        stderr_str = stderr.decode(
            "utf-8",
            errors="replace",
        )

        logger.info(
            "Terraform exited with code %s",
            process.returncode,
        )

        return (
            process.returncode,
            stdout_str,
            stderr_str,
        )

    # ==========================================================
    # Core Commands
    # ==========================================================

    async def init(
        self,
        environment: str = "dev",
    ):
        return await self._run(
            [
                self.binary,
                "init",
                "-input=false",
            ],
            self._environment_path(environment),
        )

    async def validate(
        self,
        environment: str = "dev",
    ):
        return await self._run(
            [
                self.binary,
                "validate",
            ],
            self._environment_path(environment),
        )

    async def fmt(self):
        return await self._run(
            [
                self.binary,
                "fmt",
                "-recursive",
            ],
            Path(settings.TERRAFORM_ROOT_DIR),
        )

    async def plan(
        self,
        environment: str = "dev",
        var_file: str | None = None,
    ):
        cmd = [
            self.binary,
            "plan",
            "-input=false",
            "-out=tfplan",
        ]

        if var_file:
            cmd.extend(
                [
                    "-var-file",
                    var_file,
                ]
            )

        return await self._run(
            cmd,
            self._environment_path(environment),
        )

    async def apply(
        self,
        environment: str = "dev",
    ):
        return await self._run(
            [
                self.binary,
                "apply",
                "-auto-approve",
                "-input=false",
                "tfplan",
            ],
            self._environment_path(environment),
        )

    async def destroy(
        self,
        environment: str = "dev",
    ):
        return await self._run(
            [
                self.binary,
                "destroy",
                "-auto-approve",
                "-input=false",
            ],
            self._environment_path(environment),
        )

    # ==========================================================
    # State
    # ==========================================================

    async def output(
        self,
        environment: str = "dev",
    ):
        return await self._run(
            [
                self.binary,
                "output",
                "-json",
            ],
            self._environment_path(environment),
        )

    async def state_list(
        self,
        environment: str = "dev",
    ):
        return await self._run(
            [
                self.binary,
                "state",
                "list",
            ],
            self._environment_path(environment),
        )

    async def show(
        self,
        environment: str = "dev",
    ):
        return await self._run(
            [
                self.binary,
                "show",
                "-json",
                "tfplan",
            ],
            self._environment_path(environment),
        )

    # ==========================================================
    # Workspace
    # ==========================================================

    async def workspace_list(
        self,
        environment: str = "dev",
    ):
        return await self._run(
            [
                self.binary,
                "workspace",
                "list",
            ],
            self._environment_path(environment),
        )

    async def workspace_select(
        self,
        workspace: str,
        environment: str = "dev",
    ):
        return await self._run(
            [
                self.binary,
                "workspace",
                "select",
                workspace,
            ],
            self._environment_path(environment),
        )

    # ==========================================================
    # Utility
    # ==========================================================

    async def version(self):
        return await self._run(
            [
                self.binary,
                "version",
            ],
            Path(settings.TERRAFORM_ROOT_DIR),
        )


terraform_cli = TerraformCLI()
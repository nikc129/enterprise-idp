import json
import logging

from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.client = None

    async def natural_language_provision(self, query: str) -> dict:
        if not self.client:
            return self._fallback_provision(query)

        system_prompt = """You are an infrastructure provisioning assistant for an Internal Developer Platform.
Given a natural language request, extract the intent and return a JSON object with:
- intent: what the user wants to do
- resource_type: one of ec2, s3, vpc, rds
- parameters: object with the required parameters for that resource type
- plan: human-readable description of what will be provisioned

Available resource types and their parameters:
- ec2: instance_name (string), instance_type (string, default t3.micro)
- s3: bucket_name (string), versioning (bool, default true), encryption (bool, default true)
- vpc: vpc_name (string), cidr_block (string, default 10.0.0.0/16)
- rds: db_name (string), instance_class (string, default db.t3.micro), engine (string, default postgres), engine_version (string, default 16.4), allocated_storage (int, default 20), username (string, default admin), password (string)

Return ONLY valid JSON, no markdown."""

        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ],
                temperature=0.3,
                max_tokens=500,
            )
            content = response.choices[0].message.content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(content)
        except Exception as e:
            logger.error(f"AI provision error: {e}")
            return self._fallback_provision(query)

    def _fallback_provision(self, query: str) -> dict:
        query_lower = query.lower()
        if "ec2" in query_lower or "instance" in query_lower or "server" in query_lower:
            return {
                "intent": "Create EC2 instance",
                "resource_type": "ec2",
                "parameters": {"instance_name": "ai-created-instance", "instance_type": "t3.micro"},
                "plan": "Will create a t3.micro EC2 instance in the default VPC.",
            }
        elif "s3" in query_lower or "bucket" in query_lower or "storage" in query_lower:
            return {
                "intent": "Create S3 bucket",
                "resource_type": "s3",
                "parameters": {"bucket_name": "ai-created-bucket", "versioning": True, "encryption": True},
                "plan": "Will create an S3 bucket with versioning and encryption enabled.",
            }
        elif "vpc" in query_lower or "network" in query_lower:
            return {
                "intent": "Create VPC",
                "resource_type": "vpc",
                "parameters": {"vpc_name": "ai-created-vpc", "cidr_block": "10.0.0.0/16"},
                "plan": "Will create a VPC with CIDR 10.0.0.0/16.",
            }
        elif "rds" in query_lower or "database" in query_lower or "db" in query_lower:
            return {
                "intent": "Create RDS database",
                "resource_type": "rds",
                "parameters": {
                    "db_name": "ai-created-db",
                    "instance_class": "db.t3.micro",
                    "engine": "postgres",
                    "engine_version": "16.4",
                    "allocated_storage": 20,
                    "username": "admin",
                    "password": "changeme123",
                },
                "plan": "Will create a PostgreSQL RDS instance (db.t3.micro) with 20GB storage.",
            }
        return {
            "intent": "Unknown",
            "resource_type": "",
            "parameters": {},
            "plan": f"Could not parse intent from: {query}. Please specify resource type (ec2, s3, vpc, rds).",
        }

    async def cost_optimization_advisor(self, resources: list[dict], metrics: dict = None) -> dict:
        if not self.client:
            return {
                "recommendations": [
                    {"resource": "general", "recommendation": "Enable CloudWatch detailed monitoring for cost tracking"},
                    {"resource": "general", "recommendation": "Use Spot instances for non-critical workloads"},
                    {"resource": "general", "recommendation": "Right-size instances based on utilization"},
                ],
                "total_estimated_savings": "Unable to calculate without AI service",
            }

        system_prompt = """You are a cloud cost optimization advisor.
Given a list of AWS resources and their metrics, provide cost optimization recommendations.
Return a JSON object with:
- recommendations: array of {resource, recommendation, estimated_savings}
- total_estimated_savings: estimated monthly savings string"""

        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Resources: {json.dumps(resources[:10])}\nMetrics: {json.dumps(metrics or {})}"},
                ],
                temperature=0.3,
                max_tokens=800,
            )
            content = response.choices[0].message.content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(content)
        except Exception:
            return {
                "recommendations": [{"resource": "general", "recommendation": "Review instance types for right-sizing"}],
                "total_estimated_savings": "Unable to calculate",
            }

    async def troubleshoot(self, resource_info: dict, logs: str = "") -> dict:
        if not self.client:
            return {
                "diagnosis": "AI service not configured. Check resource manually.",
                "root_cause": "Unknown",
                "suggested_fixes": ["Check AWS Console for resource status", "Review CloudWatch logs"],
            }

        system_prompt = """You are a troubleshooting assistant for cloud infrastructure.
Analyze the resource information and logs, then return a JSON object with:
- diagnosis: what's happening
- root_cause: likely root cause
- suggested_fixes: array of suggested fixes"""

        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Resource: {json.dumps(resource_info)}\nLogs: {logs[:2000]}"},
                ],
                temperature=0.3,
                max_tokens=600,
            )
            content = response.choices[0].message.content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(content)
        except Exception:
            return {
                "diagnosis": "Unable to analyze with AI. Manual investigation required.",
                "root_cause": "Unknown",
                "suggested_fixes": ["Check AWS Console", "Review CloudWatch metrics"],
            }


ai_service = AIService()

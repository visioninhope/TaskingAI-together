import aiohttp
from typing import Dict, Optional
from tkhelper.utils import ResponseWrapper
from app.config import CONFIG

__all__ = [
    "verify_credentials",
    "health_check",
]


async def verify_credentials(
    model_schema_id: str,
    provider_model_id: Optional[str],
    configs: Dict,
    model_type: Optional[str],
    credentials: Optional[Dict],
    encrypted_credentials: Optional[Dict],
    properties: Optional[Dict],
) -> ResponseWrapper:
    payload = {
        "model_schema_id": model_schema_id,
        "provider_model_id": provider_model_id,
        "model_type": model_type,
        "properties": properties,
        "configs": configs,
    }
    if credentials is not None:
        payload["credentials"] = credentials
    else:
        payload["encrypted_credentials"] = encrypted_credentials

    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/verify_credentials",
            json=payload,
        )
        return ResponseWrapper(response.status, await response.json())


async def health_check() -> ResponseWrapper:
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/health_check",
        )
        return ResponseWrapper(response.status, await response.json())

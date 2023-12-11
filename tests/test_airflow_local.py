# Third Party
import base64

import aiohttp
import pytest

HOST = "http://localhost:8080/api/v1/dags"
BASIC_AUTH = base64.b64encode(b"airflow:airflow").decode()

headers = {"Authorization": f"Basic {BASIC_AUTH}"}


@pytest.mark.asyncio
@pytest.mark.docker
async def test_airflow_local(dockercompose) -> None:
    """Start docker compose fixture and run dbcheck endpoint."""
    print(headers)
    async with aiohttp.ClientSession() as session:
        async with session.get(HOST, headers=headers) as response:
            data = await response.json()

    assert "dags" in data
    assert len(data["dags"]) > 0

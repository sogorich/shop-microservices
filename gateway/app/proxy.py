import httpx

from fastapi import APIRouter, Request, Response, HTTPException
from app.config import settings


router = APIRouter()
client = httpx.AsyncClient(timeout=settings.request_timeout)
METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]


@router.api_route("/{service}", methods=METHODS)
@router.api_route("/{service}/", methods=METHODS)
@router.api_route("/{service}/{path:path}", methods=METHODS)
async def proxy(service: str, path: str, request: Request):

    base_url = settings.services.get(service)

    if not base_url:
        raise HTTPException(404, f"Unknown serivce {service}")

    url = f"{base_url}/{path}"
    if request.url.query:
        url += f"?{request.url.query}"

    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in {"host", "content-length", "connection"}
    }

    body = await request.body()

    try:
        upstream = await client.request(request.method, url, headers=headers, content=body)

    except httpx.RequestError as e:
        raise HTTPException(502, f"Bad gateway {e}")

    response_headers = {
        k: v for k, v in upstream.headers.items()
        if k.lower() not in {"content-encoding", "transfer-encoding", "connection"}
    }
    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers=response_headers,
        media_type=upstream.headers.get("content-type")
    )
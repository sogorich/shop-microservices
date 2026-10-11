import httpx

from fastapi import APIRouter, Request, Response, HTTPException, status
from app.config import settings
from app.utils import exclude_headers


router = APIRouter()


@router.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
async def proxy(service: str, path: str, request: Request):

    base_url = settings.services.get(service)

    if not base_url:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Unknown serivce {service}")

    url = f"{base_url}/{path}"

    if request.url.query:
        url += f"?{request.url.query}"

    headers = exclude_headers(request, {"host", "content-length", "connection"})
    body = await request.body()

    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        try:
            upstream = await client.request(request.method, url, headers=headers, content=body)
            response_headers = exclude_headers(upstream, {"content-encoding", "transfer-encoding", "connection"})

            return Response(
                content=upstream.content,
                status_code=upstream.status_code,
                headers=response_headers,
                media_type=upstream.headers.get("content-type")
            )

        except httpx.RequestError as e:
            raise HTTPException(status.HTTP_502_BAD_GATEWAY, f"Bad gateway {e}")
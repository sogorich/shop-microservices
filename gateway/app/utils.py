from fastapi import Request
from httpx import Response


def exclude_headers(request_repsponse_obj: Request | Response, headers: set[str]) -> dict:
    """Исключает переданные заголовки (в частности для исключения hop-by-hop)"""
    return {
        k: _ for k, _ in request_repsponse_obj.headers.items()
        if k.lower() not in headers
    }
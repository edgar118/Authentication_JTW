import logging
from fastapi import APIRouter, Depends, Request
from starlette.datastructures import MutableHeaders

module_name = 'auth'
module_prefix = f"/{module_name}"


async def log_request_info(request: Request):
    request_body = await request.body()

    logging.info(
        f"{request.method} request to {request.url} metadata\n"
        f"\tHeaders: {request.headers}\n"
        f"\tBody: {request_body}\n"
        f"\tPath Params: {request.path_params}\n"
        f"\tQuery Params: {request.query_params}\n"
        f"\tCookies: {request.cookies}\n"
    )
    new_header = MutableHeaders(request._headers)
    new_header["xxxxx"] = "XXXXX"
    request._headers = new_header
    return request

auth_router = APIRouter(
    prefix=module_prefix,
    tags=[module_name],
    dependencies=[
        Depends(log_request_info)
    ]
)

from .router.user import *
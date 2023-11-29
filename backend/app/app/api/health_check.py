from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/healthcheck")
async def get_health() -> Response:
    return Response(status_code=200)

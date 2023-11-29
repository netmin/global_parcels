from loguru import logger

from fastapi import APIRouter, HTTPException, Query
from starlette.requests import Request

from app.models.pydantic import ParcelIn, ParcelOut
from app.models.tortoise import (
    Parcel,
    Parcel_Pydantic,
    ParcelType,
    ParcelType_Pydantic,
    ParcelTypeIn_Pydantic,
)
from app.producer import send_to_queue


router = APIRouter()


@router.post("/parcels", status_code=202)
async def create_parcel(parcel_data: ParcelIn, request: Request) -> dict[str, str]:
    """
    Accept a parcel registration request.

    - **parcel_data**: Parcel information including type, name, weight, and content value.
    - **request**: HTTP request object.
    """
    data = parcel_data.dict()
    logger.info(f"Creating parcel: {data}")
    try:
        parcel_type = await ParcelType.get(name=parcel_data.parcel_type)
        data["parcel_type_id"] = parcel_type.id
        logger.info(
            f"Parcel type '{parcel_data.parcel_type}' found with ID {parcel_type.id}"
        )
    except ParcelType.DoesNotExist:
        # Handle the case where the ParcelType is not found
        logger.error(f"Parcel type '{parcel_data.parcel_type}' not found")
        raise HTTPException(status_code=404, detail="Parcel type not found")

    data["session_id"] = request.cookies.get("session_id")
    data["content_value_cents"] = parcel_data.value_in_cents()
    data["parcel_type_id"]: parcel_type.id

    # Send data to Celery task
    await send_to_queue(data)

    return {"message": "Parcel accepted and will be processed"}


@router.get("/parcels/my", response_model=list[ParcelOut])
async def get_my_parcels(
    request: Request,
    parcel_type_id: int = Query(None, description="Filter by parcel type ID"),
    has_delivery_cost: bool = Query(
        None, description="Filter by the presence of calculated delivery cost"
    ),
    skip: int = 0,
    limit: int = 10,
) -> list[ParcelOut]:
    """
    Retrieve a list of parcels associated with the current user's session.

    This endpoint retrieves parcels based on session ID, with optional filters for parcel type ID and delivery cost presence. Supports pagination through `skip` and `limit` parameters.

    - **Response**: List of ParcelOut objects representing the parcels.
    """
    session_id = request.cookies.get("session_id")
    query = Parcel.filter(session_id=session_id).prefetch_related("parcel_type")

    if parcel_type_id is not None:
        query = query.filter(parcel_type_id=parcel_type_id)
    if has_delivery_cost is not None:
        query = query.filter(delivery_cost_cents__isnull=not has_delivery_cost)

    parcels = await query.offset(skip).limit(limit).all()
    result = [await ParcelOut.from_orm(parcel) for parcel in parcels]
    return result


@router.get("/parcels/{parcel_id}", response_model=Parcel_Pydantic)
async def get_parcel_details(parcel_id: str) -> Parcel_Pydantic:
    """
    Retrieve detailed information about a specific parcel using its unique identifier.

    This endpoint is used to fetch detailed information about a parcel, such as its name, weight, type, content value,
    and delivery cost, based on the parcel's unique ID.

    - **parcel_id**: The unique identifier of the parcel. This is a required path parameter.

    ### Response
    - A `Parcel_Pydantic` object containing detailed information about the parcel.
    - If the parcel with the specified ID is not found, a 404 error with a "Parcel not found" message is returned.

    ### Errors
    - `404 Not Found`: Returned if no parcel is found with the given ID.
    """
    parcel = await Parcel.filter(id=parcel_id).prefetch_related("parcel_type").first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    return await Parcel_Pydantic.from_tortoise_orm(parcel)


@router.post("/parcel_types", response_model=ParcelType_Pydantic)
async def create_parcel_type(parcel_data: ParcelTypeIn_Pydantic):
    """
    Create a new parcel type with the specified name.

    ### Request Body
    - `name`: String - The name of the new parcel type.

    ### Response
    - JSON object of the created parcel type with its ID and name.
    """
    parcel = await ParcelType.create(**parcel_data.model_dump(exclude_unset=True))

    return await ParcelType_Pydantic.from_tortoise_orm(parcel)


@router.get("/parcel_types", response_model=list[ParcelType_Pydantic])
async def get_parcel_types():
    """
    Retrieve a list of all available parcel types.

    Each type includes an identifier and the name of the type.
    """
    return await ParcelType_Pydantic.from_queryset(ParcelType.all())

from unittest.mock import Mock
import pytest
from httpx import AsyncClient

from app.models.tortoise import ParcelType


@pytest.mark.anyio
async def test_create_parcel(client: AsyncClient, mocker):
    parcel_type = await ParcelType.create(name="clothes")
    mocker.patch("app.api.parcel.send_to_queue", return_value=Mock())
    parcel_data = {
        "name": "Parcel for testing",
        "weight": 1.5,
        "content_value_cents": 1000,
        "session_id": "1234",
        "delivery_cost_cents": None,
        "parcel_type_id": 1,
        "parcel_type": "clothes",
    }

    response = await client.post(
        "/parcels",
        json=parcel_data,
    )

    # Check that status code is success
    assert response.status_code == 202

    # Validate response
    assert response.json() == {"message": "Parcel accepted and will be processed"}

    await parcel_type.delete()


@pytest.mark.anyio
async def test_get_my_parcels(client: AsyncClient):
    response = await client.get(
        "/parcels/my",
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

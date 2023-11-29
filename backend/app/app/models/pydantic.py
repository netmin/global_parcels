from pydantic import BaseModel

from app.models.tortoise import ParcelIn_Pydantic, Parcel_Pydantic, ParcelType_Pydantic


class ParcelInWithTypeId(BaseModel):
    parcel_type_id: None | int
    parcel_type: str


class ParcelTypeInParcel(BaseModel):
    id: int
    name: str


class ParcelIn(ParcelIn_Pydantic, ParcelInWithTypeId):
    def value_in_cents(self) -> int:
        return int(self.content_value_cents * 100)


class ParcelOut(BaseModel):
    id: str
    name: str
    weight: float
    content_value_cents: int
    delivery_cost_cents: int | None
    session_id: str | None
    parcel_type: str

    @classmethod
    async def from_orm(cls, obj):
        parcel_type_data = await ParcelType_Pydantic.from_tortoise_orm(obj.parcel_type)
        parcel_data = await Parcel_Pydantic.from_tortoise_orm(obj)
        return cls(
            **parcel_data.dict(exclude={"id", "parcel_type"}),
            id=str(obj.id),
            parcel_type=parcel_type_data.name
        )

from decimal import Decimal

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ParcelType(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(
        max_length=50, unique=True, description="Name of the parcel type"
    )

    class Meta:
        table = "parcel_types"

    def __str__(self):
        return self.name


class Parcel(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=100, description="Name of the parcel")
    weight = fields.FloatField(description="Weight of the parcel")
    content_value_cents = fields.IntField(description="Value of the content in cents")
    delivery_cost_cents = fields.IntField(
        null=True, description="Delivery cost in cents"
    )
    parcel_type = fields.ForeignKeyField(
        "models.ParcelType", related_name="parcels", description="Type of the parcel"
    )
    session_id = fields.CharField(
        max_length=255, null=True, description="ID of the users session"
    )

    class Meta:
        table = "parcel"

    def __str__(self):
        return self.name


# Creating Pydantic models for Tortoise ORM models
ParcelType_Pydantic = pydantic_model_creator(ParcelType, name="ParcelType")
ParcelTypeIn_Pydantic = pydantic_model_creator(
    ParcelType, name="ParcelTypeIn", exclude_readonly=True
)
Parcel_Pydantic = pydantic_model_creator(
    Parcel,
    name="Parcel",
)
ParcelIn_Pydantic = pydantic_model_creator(
    Parcel, name="ParcelIn", exclude_readonly=True
)

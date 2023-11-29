import asyncio
import os
from tortoise import Tortoise

from models.tortoise import ParcelType


async def init():
    await Tortoise.init(
        db_url=os.getenv("DATABASE_URL"), modules={"models": ["models.tortoise"]}
    )
    await Tortoise.generate_schemas()


async def fill_db():
    await ParcelType.create(name="clothes")
    await ParcelType.create(name="electronics")
    await ParcelType.create(name="others")


async def main():
    await init()
    await fill_db()

    parcels = await ParcelType.all()
    for parcel in parcels:
        print(parcel.name)


if __name__ == "__main__":
    asyncio.run(main())

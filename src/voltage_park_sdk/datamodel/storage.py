from typing import Literal

from pydantic import BaseModel, Field

from voltage_park_sdk.datamodel.shared import ListResponse

StorageVolumeStatusOptions = Literal["active", "inactive"]


class StorageVolume(BaseModel):
    id: str = Field(
        description="The ID of the created storage volume",
    )
    size_in_gb: int = Field(
        description="The size of the storage volume in GB",
        gt=0,
    )
    name: str = Field(
        description="The name of the storage volume",
    )
    status: StorageVolumeStatusOptions = Field(
        description="The status of the storage volume",
    )
    rate_hourly: str = Field(
        description="The hourly rate of the storage volume",
    )
    order_ids: list[str] = Field(
        description="The IDs of the orders associated with the storage volume",
    )
    tenant_id: int = Field(
        description="VAST tenant ID",
    )
    vip: str = Field(
        description="The IP address to mount the storage volume",
    )


# GET storage/hourly-rate
class StorageHourlyRate(BaseModel):
    hourly_rate_per_gb: str


# POST storage


class StorageVolumeCreatePayload(BaseModel):
    size_in_gb: int = Field(
        description="The size of the storage volume in GB",
        gt=0,
    )
    name: str = Field(
        description="The name of the storage volume",
    )
    order_ids: list[str] = Field(
        description="The IDs of the orders to associate with the storage volume",
    )


class StorageVolumeCreateResponse(StorageVolume):
    pass


# GET storage/
class StorageVolumesGetResponse(ListResponse[StorageVolume]):
    pass


# PATCH storage/{storage_id}
class StorageVolumePatchPayload(BaseModel):
    size_in_gb: int | None = Field(
        description="The size of the storage volume in GB",
    )
    name: str | None = Field(
        description="The name of the storage volume",
    )
    order_ids: list[str] | None = Field(
        description="The IDs of the orders to associate with the storage volume",
    )


class StorageVolumePatchResponse(StorageVolume):
    pass


# GET storage/{storage_id}
class StorageVolumeGetResponse(StorageVolume):
    used_capacity_bytes: int = Field(
        description="The used capacity of the storage volume in bytes",
    )

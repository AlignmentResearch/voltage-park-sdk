from typing import Literal

from pydantic import BaseModel, Field

from voltage_park_sdk.datamodel.shared import (
    CloudInitFile,
    GPUModelOptions,
    ListResponse,
    OrganizationSSHKey,
    OrganzationSSHKeyNone,
)

BaremetalNetworkType = Literal["infiniband", "ethernet"]


class BaremetalNodeSpec(BaseModel):
    gpu_model: GPUModelOptions = Field(
        description="The model of the GPU", default="h100-sxm5-80gb"
    )
    gpu_count: int = Field(description="The number of GPUs", ge=0, default=8)
    cpu_model: str = Field(description="The model of the CPU")
    cpu_count: int = Field(
        description="The number of CPUs",
        ge=0,
    )
    ram_gb: int = Field(
        description="The amount of RAM in GB",
        ge=0,
    )
    storage_gb: int = Field(
        description="The amount of storage in GB",
        ge=0,
    )


class BaremetalLocation(BaseModel):
    id: str = Field(description="The ID of the location")
    gpu_count_ethernet: int = Field(
        description="The number of GPUs available on ethernet",
        ge=0,
    )
    gpu_price_ethernet: str = Field(
        description="The price of a GPU on ethernet",
    )
    gpu_count_infiniband: int = Field(
        description="The number of GPUs available on infiniband",
        ge=0,
    )
    gpu_price_infiniband: str = Field(
        description="The price of a GPU on infiniband",
    )
    specs_per_node: BaremetalNodeSpec = Field(
        description="The specs per node",
    )


class BaremetalLocations(ListResponse[BaremetalLocation]):
    pass


class BaremetalCloudInit(BaseModel):
    packages: list[str] | None = None
    write_files: list[CloudInitFile] | None = None
    runcmd: list[str] | None = None


class BaremetalRentalCreatePayload(BaseModel):
    location_id: str = Field(
        description="The ID of the location to create the rental on"
    )
    gpu_count: int = Field(description="The number of GPUs to rent", gt=0)
    name: str = Field(description="The name of the rental")
    organization_ssh_keys: OrganizationSSHKey = Field(
        description="The SSH keys to use for the rental",
        discriminator="mode",
        default=OrganzationSSHKeyNone(),
    )
    ssh_keys: list[str] | None = Field(
        description="The SSH keys to use for the rental",
        default=None,
    )
    network_type: BaremetalNetworkType = Field(description="The type of network to use")
    suborder: int | None = Field(description="The suborder to use for the rental")
    storage_id: str | None = Field(
        description="The ID of the storage to use for the rental"
    )
    tags: list[str] | None = Field(description="The tags to use for the rental")
    cloudinit_script: BaremetalCloudInit | None = Field(
        description="The cloudinit script to use for the rental",
        default=None,
    )


class NodeNetworking(BaseModel):
    public_ip: str
    private_ip: str


class BaremetalRental(BaseModel):
    id: str
    name: str
    creation_timestamp: str
    status: str
    power_status: str | None = None
    node_count: int | None = None
    specs_per_node: BaremetalNodeSpec | None = None
    rate_hourly: str
    network_type: str | None = None
    username: str | None = None
    node_networking: list[NodeNetworking] | None = None
    sub_order: str | None = None
    storage_id: str | None
    storage_pv: str | None
    storage_pvc: str | None
    k8s_cluster_id: str | None
    kubeconfig: str | None
    tags: list[str]


class BaremetalRentals(ListResponse[BaremetalRental]):
    pass

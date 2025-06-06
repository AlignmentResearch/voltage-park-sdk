from typing import Annotated, Literal

from pydantic import BaseModel, Field

from voltage_park_sdk.datamodel.shared import (
    CloudInitFile,
    GPUModelOptions,
    ListResponse,
    OrganizationSSHKey,
    OrganzationSSHKeyNone,
)

# General components
BaremetalNetworkTypeOptions = Literal[
    "infiniband",
    "ethernet",
]
BaremetalRentalStatusOptions = Literal[
    "Running",
    "Terminated",
    "Pending",
    "Failed",
]
BaremetalRentalPowerStatusOptions = Literal[
    "Running",
    "Stopped",
]
BaremetalRentalPutPowerStatusOptions = Literal[
    "started",
    "stopped",
]


class BaremetalNodeSpec(BaseModel):
    gpu_model: GPUModelOptions = Field(
        description="The model of the GPU",
        default="h100-sxm5-80gb",
    )
    gpu_count: int = Field(
        description="The number of GPUs",
        ge=0,
    )
    cpu_model: str = Field(
        description="The model of the CPU",
    )
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


# GET bare-metal/locations/
# GET bare-metal/locations/{location_id}
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


# POST bare-metal/
class BaremetalCloudInit(BaseModel):
    packages: list[str] | None = None
    write_files: list[CloudInitFile] | None = None
    runcmd: list[str] | None = None


class BaremetalRentalCreatePayload(BaseModel):
    location_id: str = Field(
        description="The ID of the location to create the rental on"
    )
    gpu_count: int = Field(
        description="The number of GPUs to rent",
        gt=0,
    )
    name: str = Field(
        description="The name of the rental",
    )
    organization_ssh_keys: OrganizationSSHKey = Field(
        description="The SSH keys to use for the rental",
        discriminator="mode",
        default=OrganzationSSHKeyNone(),
    )
    ssh_keys: list[str] | None = Field(
        description="The SSH keys to use for the rental",
        default=None,
    )
    network_type: BaremetalNetworkTypeOptions = Field(
        description="The type of network to use",
    )
    suborder: int | None = Field(
        description="The suborder to use for the rental",
        default=None,
    )
    storage_id: str | None = Field(
        description="The ID of the storage to use for the rental"
    )
    tags: list[str] | None = Field(
        description="The tags to use for the rental",
        default=None,
    )
    cloudinit_script: BaremetalCloudInit | None = Field(
        description="The cloudinit script to use for the rental",
        default=None,
    )


class BaremetalRentalCreateResponse(BaseModel):
    rental_id: str = Field(
        description="The ID of the rental",
    )
    warning: str | None = Field(
        description="Any warnings about the rental creation",
        default=None,
    )


# GET bare-metal/
class NodeNetworking(BaseModel):
    public_ip: str = Field(
        description="The public IP of the node",
    )
    private_ip: str = Field(
        description="The private IP of the node",
    )


class BaremetalRentalBase(BaseModel):
    id: str = Field(
        description="The ID of the rental",
    )
    name: str = Field(
        description="The name of the rental",
    )
    creation_timestamp: str = Field(
        description="The creation timestamp of the rental",
    )
    rate_hourly: str = Field(
        description="The hourly rate of the rental",
    )
    suborder: str | None = Field(
        description="The suborder of the rental",
        default=None,
    )


class BaremetalRentalPending(BaremetalRentalBase):
    status: Literal["Pending"] = "Pending"


class BaremetalRentalActive(BaremetalRentalBase):
    power_status: BaremetalRentalPowerStatusOptions = Field(
        description="The power status of the rental",
    )
    node_count: int = Field(
        description="The number of nodes in the rental",
        ge=0,
    )
    specs_per_node: BaremetalNodeSpec = Field(
        description="The specs per node",
    )
    rate_hourly: str = Field(
        description="The hourly rate of the rental",
    )
    network_type: BaremetalNetworkTypeOptions = Field(
        description="The type of network to use",
    )
    username: str | None = Field(
        description="The username of the on the rental machine",
    )
    node_networking: list[NodeNetworking] = Field(
        description="The networking of the nodes in the rental",
    )
    sub_order: str | None = Field(
        description="The suborder of the rental",
    )
    storage_id: str | None = Field(
        description="The ID of the storage associated with the rental",
    )
    storage_pv: str | None = Field(
        description="The ID of the storage pv associated with the rental",
    )
    storage_pvc: str | None = Field(
        description="The ID of the storage pvc associated with the rental",
    )
    k8s_cluster_id: str | None = Field(
        description="The ID of the k8s cluster associated with the rental",
    )
    kubeconfig: str | None = Field(
        description="The kubeconfig associated with the rental",
    )
    tags: list[str] | None = Field(
        description="The tags associated with the rental",
    )


class BaremetalRentalTerminated(BaremetalRentalActive):
    status: Literal["Terminated"] = "Terminated"


class BaremetalRentalFailed(BaremetalRentalActive):
    status: Literal["Failed"] = "Failed"


class BaremetalRentalRunning(BaremetalRentalActive):
    status: Literal["Running"] = "Running"


BaremetalRental = Annotated[
    BaremetalRentalPending
    | BaremetalRentalTerminated
    | BaremetalRentalFailed
    | BaremetalRentalRunning,
    Field(discriminator="status"),
]


class BaremetalRentals(ListResponse[BaremetalRental]):
    pass


# PUT bare-metal/{baremetal_rental_id}/power-status
class BaremetalRentalPowerStatusPayload(BaseModel):
    status: BaremetalRentalPutPowerStatusOptions = Field(
        description="The power status to set the rental to",
    )


# PATCH bare-metal/{baremetal_rental_id}
class BaremetalRentalPatchPayload(BaseModel):
    name: str | None = Field(
        description="The name of the rental",
    )
    tags: list[str] | None = Field(
        description="The tags of the rental",
    )


class BaremetalRentalPatchResponse(BaseModel):
    name: str | None = Field(
        description="The name of the rental",
    )
    tags: list[str] | None = Field(
        description="The tags of the rental",
    )


# POST bare-metal/{baremetal_rental_id}/reboot
class BaremetalRentalRebootNodesPayload(BaseModel):
    public_ips: list[str] = Field(
        description="The public IPs of the nodes to reboot",
    )


# PATCH bare-metal/{baremetal_rental_id}/remove-nodes
class BaremetalRentalRemoveNodesPayload(BaseModel):
    public_ips: list[str] = Field(
        description="The public IPs of the nodes to remove",
    )

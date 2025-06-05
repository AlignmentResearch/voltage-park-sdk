from typing import Literal

from pydantic import BaseModel, Field

from voltage_park_sdk.datamodel.shared import CloudInit, ListResponse

VirtualMachineType = Literal[
    "ondem",
    "spot",
    "subscription",
]
VirtualMachineStatus = Literal[
    "Running",
    "StoppedDisassociated",
    "Stopped",
    "Terminated",
    "Outbid",
    "Relocating",
]
VirtualMachinePowerStatus_ = Literal[
    "started",
    "stopped",
    "stopped_disassociated",
]
VirtualMachineOperatingSystem = Literal[
    "Ubuntu 20.04 LTS",
    "Ubuntu 22.04 LTS",
    "TensorML 20 TensorFlow",
    "TensorML 20 PyTorch",
    "TensorML 20 Everything",
    "Ubuntu 24.04 LTS",
    "TensorML 24 TensorFlow",
    "TensorML 24 PyTorch",
    "TensorML 24 Everything",
    "Windows 10",
]


class VirtualMachinePowerStatus(BaseModel):
    status: VirtualMachinePowerStatus_ = Field(
        description="The power status of the virtual machine"
    )


class GPUResource(BaseModel):
    count: int = Field(description="The number of GPUs of this type", gt=0)


class VirtualMachineResources(BaseModel):
    gpus: dict[str, GPUResource] = Field(
        description="Mapping between GPU type and number of GPUs"
    )
    ram_gb: int = Field(description="The amount of RAM in GB", gt=0)
    storage_gb: int = Field(description="The amount of storage in GB", gt=0)
    vcpu_count: int = Field(description="The number of vCPUs", gt=0)


class VirtualMachinePreset(BaseModel):
    id: str = Field(description="The ID of the preset")
    resources: VirtualMachineResources = Field(
        description="The resources available in this preset"
    )
    operating_system: VirtualMachineOperatingSystem = Field(
        description="The operating system of the preset"
    )
    compute_rate_hourly: str = Field(description="The compute rate per hour")
    storage_rate_hourly: str = Field(description="The storage rate per hour")
    available_vms: int = Field(
        description="The number of VMs that can be created with this preset",
        ge=0,
    )


class VirtualMachineLocation(BaseModel):
    id: str = Field(description="The ID of the location")
    available_presets: list[VirtualMachinePreset] = Field(
        description="The presets available at this location"
    )


class VirtualMachineLocations(ListResponse[VirtualMachineLocation]):
    pass


class VirtualMachinePricing(BaseModel):
    gpus_per_hr: str
    vcpu_per_hr: str
    ram_per_hr: str
    storage_per_hr: str
    total_associated_per_hr: str
    total_disassociated_per_hr: str


class PortForward(BaseModel):
    internal_port: int = Field(
        description="The internal port of the port forward",
        ge=1,
        le=65535,
    )
    external_port: int = Field(
        description="The external port of the port forward",
        ge=1,
        le=65535,
    )


class VirtualMachine(BaseModel):
    id: str = Field(description="The ID of the virtual machine")
    hostnode_id: str = Field(description="The ID of the host node")
    type: VirtualMachineType = Field(description="The type of the virtual machine")
    status: VirtualMachineStatus = Field(
        description="The status of the virtual machine"
    )
    name: str = Field(description="The name of the virtual machine")
    resources: VirtualMachineResources = Field(
        description="The resources of the virtual machine"
    )
    operating_system: VirtualMachineOperatingSystem = Field(
        description="The operating system of the virtual machine"
    )
    pricing: VirtualMachinePricing = Field(
        description="The pricing of the virtual machine"
    )
    public_ip: str = Field(description="The public IP of the virtual machine")
    internal_ip: str = Field(description="The internal IP of the virtual machine")
    port_forwards: list[PortForward] = Field(
        description="The port forwards of the virtual machine"
    )
    timestamp_creation: str = Field(
        description="The timestamp of the creation of the virtual machine"
    )
    tags: list[str] = Field(description="The tags of the virtual machine")


class VirtualMachines(ListResponse[VirtualMachine]):
    pass


class VirtualMachineDeployPayload(BaseModel):
    config_id: str = Field(description="The ID of the config to deploy")
    name: str = Field(description="The name of the virtual machine")
    password: str | None = Field(
        description="The password to use for the virtual machine"
    )
    organization_ssh_keys: dict[str, str] | None = Field(
        description="The organization SSH keys to use for the virtual machine"
    )
    ssh_keys: list[str] | None = Field(
        description="The SSH keys to use for the virtual machine"
    )
    cloud_init: CloudInit | None = Field(
        description="The cloud init to use for the virtual machine"
    )
    tags: list[str] | None = Field(
        description="The tags to use for the virtual machine"
    )


class VirtualMachineDeployResponse(BaseModel):
    vm_id: str = Field(description="The ID of the virtual machine")


class VirtualMachinePatchPayload(BaseModel):
    name: str | None = Field(description="The name of the virtual machine")
    tags: list[str] | None = Field(description="The tags of the virtual machine")


class VirtualMachinePatchResponse(BaseModel):
    name: str | None = Field(description="The name of the virtual machine")
    tags: list[str] | None = Field(description="The tags of the virtual machine")

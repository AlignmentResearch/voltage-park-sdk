from typing import Generic, Self, TypeVar

from pydantic import BaseModel, model_validator


class GPUResource(BaseModel):
    count: int


class AvailableResources(BaseModel):
    gpus: dict[str, GPUResource]
    ram_gb: int
    storage_gb: int
    vcpu_count: int


class Pricing(BaseModel):
    per_gpu_hr: dict[str, str]
    per_vcpu_hr: str
    per_gb_ram_hr: str
    per_gb_storage_hr: str


class HostNode(BaseModel):
    location_id: str
    available_resources: AvailableResources
    pricing: Pricing
    available_ports: list[int]

    @model_validator(mode="after")
    def validate_gpu_names(self) -> Self:
        for gpu_name in self.available_resources.gpus:
            if gpu_name not in self.pricing.per_gpu_hr:
                msg = f"GPU name {gpu_name} not found in pricing"
                raise ValueError(msg)
        return self


class Location(BaseModel):
    city: str
    region: str
    country: str
    hostnodes: list[HostNode]


class VMPricing(BaseModel):
    gpus_per_hr: str
    vcpu_per_hr: str
    ram_per_hr: str
    storage_per_hr: str
    total_associated_per_hr: str
    total_disassociated_per_hr: str


class PortForward(BaseModel):
    internal_port: int
    external_port: int


class VirtualMachine(BaseModel):
    id: str
    hostnode_id: str
    type: str
    status: str
    name: str
    resources: AvailableResources
    operating_system: str
    pricing: VMPricing
    public_ip: str
    port_forwards: list[PortForward]
    timestamp_creation: str
    tags: list[str]


class InstantDeployPreset(BaseModel):
    id: str
    resources: AvailableResources
    operating_system: str
    compute_rate_hourly: str
    storage_rate_hourly: str
    location_ids_with_availability: list[str]


class BaremetalNodeSpec(BaseModel):
    gpu_model: str
    gpu_count: int
    cpu_model: str
    cpu_count: int
    ram_gb: int
    storage_gb: int


class BaremetalLocation(BaseModel):
    id: str
    gpu_count_ethernet: int
    gpu_price_ethernet: float
    gpu_count_infiniband: int
    gpu_price_infiniband: float
    specs_per_node: BaremetalNodeSpec


class NodeNetworking(BaseModel):
    public_ip: str
    private_ip: str


class BaremetalRental(BaseModel):
    id: str
    name: str
    creation_timestamp: str
    status: str
    power_status: str
    node_count: int
    specs_per_node: BaremetalNodeSpec
    rate_hourly: str
    network_type: str
    username: str
    node_networking: list[NodeNetworking]
    sub_order: str | None
    storage_id: str | None
    storage_pv: str | None
    storage_pvc: str | None
    k8s_cluster_id: str | None
    kubeconfig: str | None
    tags: list[str]


class BillingHourlyRate(BaseModel):
    rate_hourly: str


class BillingTransactionLinkedInstance(BaseModel):
    id: str
    virtual_machine_id: str | None = None
    baremetal_rental_id: str | None = None
    timestamp_creation: str
    timestamp_deletion: str | None


class BillingTransactionDetails(BaseModel):
    type: str
    linked_instance: BillingTransactionLinkedInstance | None = None
    note_public: str | None = None


class BillingTransaction(BaseModel):
    id: str
    total_amount: str
    timestamp_creation: str
    timestamp_completion: str | None
    details: BillingTransactionDetails
    period_amount: str


class MonthlyBillingReport(BaseModel):
    transactions: list[BillingTransaction]
    balance_at_period_start: str
    balance_at_period_end: str
    balance_delta_in_period: str


class SSHKey(BaseModel):
    id: str
    name: str
    content: str


class StorageHourlyRate(BaseModel):
    hourly_rate_per_gb: str


class StorageVolume(BaseModel):
    id: str
    size_in_gb: int
    name: str
    status: str
    rate_hourly: str
    order_ids: list[str]
    tenant_id: int
    vip: str


ResponseT = TypeVar("ResponseT", bound=BaseModel)


class ListResponse(BaseModel, Generic[ResponseT]):
    results: list[ResponseT]
    total_result_count: int
    has_previous: bool
    has_next: bool


class Locations(ListResponse[Location]):
    pass


class HostNodes(ListResponse[HostNode]):
    pass


class VirtualMachines(ListResponse[VirtualMachine]):
    pass


class BaremetalLocations(ListResponse[BaremetalLocation]):
    pass


class BaremetalRentals(ListResponse[BaremetalRental]):
    pass


class BillingTransactions(ListResponse[BillingTransaction]):
    pass


class SSHKeys(ListResponse[SSHKey]):
    pass


class StorageVolumes(ListResponse[StorageVolume]):
    pass

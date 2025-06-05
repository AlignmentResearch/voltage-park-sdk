from pydantic import BaseModel

from voltage_park_sdk.datamodel.shared import ListResponse


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


class BillingTransactions(ListResponse[BillingTransaction]):
    pass


class StorageVolumes(ListResponse[StorageVolume]):
    pass

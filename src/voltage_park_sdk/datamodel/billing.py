from datetime import datetime
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, Field

from voltage_park_sdk.datamodel.shared import ListResponse

BillingResourceTypeOptions = Literal[
    "virtual_machine",
    "baremetal",
    "storage_block",
    "storage",
]


# GET billing/hourly-rate
class BillingHourlyRate(BaseModel):
    rate_hourly: str = Field(
        description="The current hourly rate for all resources in the organization",
    )


def is_valid_date(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d").date()  # noqa: DTZ007
    except ValueError as e:
        msg = "Value must be in YYYY-MM-DD format (e.g. '2024-01-01')"
        raise ValueError(msg) from e
    return value


def is_valid_datetime(value: str) -> str:
    # Try ISO format with microseconds
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")  # noqa: DTZ007
    except ValueError:
        pass
    else:
        return value

    # Try ISO format without microseconds
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")  # noqa: DTZ007
    except ValueError:
        pass
    else:
        return value

    msg = "Value must be in ISO format (e.g. '2024-01-01T00:00:00Z' or '2024-01-01T00:00:00.000Z')"
    raise ValueError(msg)


def is_valid_date_or_none(value: str | None) -> str | None:
    if value is None:
        return None
    return is_valid_date(value)


def is_valid_datetime_or_none(value: str | None) -> str | None:
    if value is None:
        return None
    return is_valid_datetime(value)


Date = Annotated[str, AfterValidator(is_valid_date)]
MaybeDate = Annotated[str | None, AfterValidator(is_valid_date_or_none)]
Datetime = Annotated[str, AfterValidator(is_valid_datetime)]
MaybeDatetime = Annotated[str | None, AfterValidator(is_valid_datetime_or_none)]


# GET billing/transactions
class BillingTransactionsPayload(BaseModel):
    limit: int | None = Field(
        description="The maximum number of transactions to return",
        default=None,
    )
    offset: int | None = Field(
        description="The number of transactions to skip",
        default=None,
    )
    types: list[BillingResourceTypeOptions] | None = Field(
        description="The types of transactions to return",
        default=None,
    )
    earliest: MaybeDate = Field(
        description="The start date of the period to return transactions for",
        default=None,
    )
    latest: MaybeDate = Field(
        description="The end date of the period to return transactions for",
        default=None,
    )


class TransactionLinkedInstance(BaseModel):
    id: str = Field(
        description="The ID of the linked transaction instance",
    )
    timestamp_creation: Datetime = Field(
        description="When the transaction instance was created",
    )
    timestamp_deletion: MaybeDatetime = Field(
        description="When the transaction instance was deleted",
    )


class StripeDepositBillingDetails(BaseModel):
    type: Literal["stripe_deposit"] = Field(
        description="The type of billing details",
    )


class StoragePayoutBillingDetails(BaseModel):
    type: Literal["storage_payout"] = Field(
        description="The type of billing details",
    )
    linked_instance: TransactionLinkedInstance = Field(
        description="The linked transaction instance",
    )


class StorageChargeBillingDetails(BaseModel):
    type: Literal["storage_charge"] = Field(
        description="The type of billing details",
    )
    linked_instance: TransactionLinkedInstance = Field(
        description="The linked transaction instance",
    )


class OtherBillingDetails(BaseModel):
    type: Literal["other"] = Field(
        description="The type of billing details",
    )
    note_public: str | None = Field(
        description="The public note for the transaction",
    )


class VMTransactionLinkedInstance(TransactionLinkedInstance):
    type: Literal["virtual_machine_instance", "storage_block_instance"] = Field(
        description="The type of linked transaction instance",
    )
    virtual_machine_id: str = Field(
        description="The ID of the virtual machine instance",
    )


class VMPayoutBillingDetails(BaseModel):
    type: Literal["payout"] = Field(
        description="The type of billing details",
    )
    linked_instance: VMTransactionLinkedInstance = Field(
        description="The linked transaction instance",
    )


class VMChargeBillingDetails(BaseModel):
    type: Literal["charge"] = Field(
        description="The type of billing details",
    )
    linked_instance: VMTransactionLinkedInstance = Field(
        description="The linked transaction instance",
    )


class BaremetalTransactionLinkedInstance(TransactionLinkedInstance):
    baremetal_rental_id: str = Field(
        description="The ID of the baremetal rental instance",
    )


class BaremetalPayoutBillingDetails(BaseModel):
    type: Literal["baremetal_payout"] = Field(
        description="The type of billing details",
    )
    linked_instance: BaremetalTransactionLinkedInstance = Field(
        description="The linked transaction instance",
    )


class BaremetalChargeBillingDetails(BaseModel):
    type: Literal["baremetal_charge"] = Field(
        description="The type of billing details",
    )
    linked_instance: BaremetalTransactionLinkedInstance = Field(
        description="The linked transaction instance",
    )


BillingDetails = Annotated[
    StripeDepositBillingDetails
    | StoragePayoutBillingDetails
    | StorageChargeBillingDetails
    | OtherBillingDetails
    | VMPayoutBillingDetails
    | VMChargeBillingDetails
    | BaremetalPayoutBillingDetails
    | BaremetalChargeBillingDetails,
    Field(discriminator="type"),
]


class BillingTransaction(BaseModel):
    id: str = Field(
        description="The ID of the transaction",
    )
    total_amount: str = Field(
        description="The total amount of the transaction",
    )
    timestamp_creation: Datetime = Field(
        description="When the transaction was created",
    )
    timestamp_completion: MaybeDatetime = Field(
        description="When the transaction was completed",
    )
    details: BillingDetails = Field(
        description="The details of the transaction",
    )
    period_amount: str = Field(
        description="The amount of the transaction for the period",
    )


class BillingTransactionsResponse(ListResponse[BillingTransaction]):
    pass


# GET billing/reports/{year}/{month}/transactions
class MonthlyBillingReport(BaseModel):
    transactions: list[BillingTransaction] = Field(
        description="The transactions for the month",
    )
    balance_at_period_start: str = Field(
        description="The balance at the start of the period",
    )
    balance_at_period_end: str = Field(
        description="The balance at the end of the period",
    )
    balance_delta_in_period: str = Field(
        description="The balance delta in the period",
    )

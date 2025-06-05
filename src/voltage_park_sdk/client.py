from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import requests

from voltage_park_sdk.model import (
    BaremetalLocation,
    BaremetalLocations,
    BaremetalRental,
    BaremetalRentals,
    BillingHourlyRate,
    BillingTransactions,
    HostNode,
    HostNodes,
    InstantDeployPreset,
    Location,
    Locations,
    MonthlyBillingReport,
    SSHKey,
    SSHKeys,
    StorageHourlyRate,
    StorageVolume,
    StorageVolumes,
    VirtualMachine,
    VirtualMachines,
)


class VoltageParkClient:
    def __init__(self, token: str | Path) -> None:
        self._api_url = "https://cloud-api.voltagepark.com/api/v1/"
        self._token = token

    def _headers(
        self,
        operation: Literal["get", "post", "put", "patch", "delete"],
        **overrides: str,
    ) -> dict[str, str]:
        operation_headers: dict[str, str] = {
            "get": {
                "Authorization": f"Bearer {self._token}",
                "Accept": "*/*",
            },
            "post": {
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
            },
            "put": {
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
            },
            "patch": {
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
            },
            "delete": {
                "Authorization": f"Bearer {self._token}",
                "Accept": "*/*",
            },
        }[operation]
        operation_headers.update(overrides)
        return operation_headers

    def _params(self, **params: str) -> dict[str, str]:
        return {k: v for k, v in params.items() if v is not None}

    ################
    # GET requests #
    ################

    def get(self, endpoint: str, **params: int | str | bool | None) -> Any:
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(
            f"{self._api_url}{endpoint}",
            headers=self._headers("get"),
            params=params,
            timeout=10,
        )
        return response.json()

    def get_locations(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Locations:
        endpoint = "locations/"
        response = self.get(endpoint, limit=limit, offset=offset)
        return Locations(**response)

    def get_location(self, location_id: str) -> Location:
        endpoint = f"locations/{location_id}"
        response = self.get(endpoint)
        return Location(**response)

    def get_hostnodes(self) -> HostNodes:
        msg = "Not implemented by the API"
        raise NotImplementedError(msg)

    def get_hostnode(self, hostnode_id: str) -> HostNode:
        endpoint = f"hostnodes/{hostnode_id}"
        response = self.get(endpoint)
        return HostNode(**response)

    def get_virtual_machines(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> VirtualMachines:
        endpoint = "virtual-machines/"
        response = self.get(endpoint, limit=limit, offset=offset)
        return VirtualMachines(**response)

    def get_virtual_machine(self, vm_id: str) -> VirtualMachine:
        endpoint = f"virtual-machines/{vm_id}"
        response = self.get(endpoint)
        return VirtualMachine(**response)

    def get_instant_deploy_presets(
        self,
        available: bool | None = None,
    ) -> list[InstantDeployPreset]:
        endpoint = "instant-deploy-presets/"
        response = self.get(endpoint, available=available)
        return [InstantDeployPreset(**preset) for preset in response]

    def get_instant_deploy_preset(self, preset_id: str) -> InstantDeployPreset:
        endpoint = f"instant-deploy-presets/{preset_id}"
        response = self.get(endpoint)
        return InstantDeployPreset(**response)

    def get_baremetal_locations(self) -> BaremetalLocations:
        endpoint = "bare-metal/locations/"
        response = self.get(endpoint)
        return BaremetalLocations(**response)

    def get_baremetal_location(self, location_id: str) -> BaremetalLocation:
        msg = "Not implemented by the API"
        raise NotImplementedError(msg)

    def get_baremetal_rentals(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> BaremetalRentals:
        endpoint = "bare-metal/"
        response = self.get(endpoint, limit=limit, offset=offset)
        return BaremetalRentals(**response)

    def get_baremetal_rental(self, rental_id: str) -> BaremetalRental:
        msg = "Not implemented by the API"
        raise NotImplementedError(msg)

    def get_billing_hourly_rates(self) -> BillingHourlyRate:
        endpoint = "billing/hourly-rate"
        response = self.get(endpoint)
        return BillingHourlyRate(**response)

    def get_billing_transactions(
        self,
        limit: int | None = None,
        offset: int | None = None,
        earliest: str | None = None,
        latest: str | None = None,
    ) -> BillingTransactions:
        self._validate_date_format(earliest, "earliest")
        self._validate_date_format(latest, "latest")

        endpoint = "billing/transactions/"
        response = self.get(
            endpoint,
            limit=limit,
            offset=offset,
            earliest=earliest,
            latest=latest,
        )
        return BillingTransactions(**response)

    def get_monthly_billing_report(
        self,
        year: int,
        month: int,
    ) -> MonthlyBillingReport:
        endpoint = f"billing/reports/{year}/{month}/transactions"
        response = self.get(endpoint)
        return MonthlyBillingReport(**response)

    def get_ssh_keys(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SSHKeys:
        endpoint = "organization/ssh-keys"
        response = self.get(endpoint, limit=limit, offset=offset)
        return SSHKeys(**response)

    def get_ssh_key(self, ssh_key_id: str) -> SSHKey:
        msg = "Not implemented by the API"
        raise NotImplementedError(msg)

    def get_storage_hourly_rate(self) -> StorageHourlyRate:
        endpoint = "storage/hourly-rate"
        response = self.get(endpoint)
        return StorageHourlyRate(**response)

    def get_storage_volumes(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> StorageVolumes:
        endpoint = "storage"
        response = self.get(endpoint, limit=limit, offset=offset)
        return StorageVolumes(**response)

    def get_storage_volume(self, storage_id: str) -> StorageVolume:
        endpoint = f"storage/{storage_id}"
        response = self.get(endpoint)
        return StorageVolume(**response)

    @staticmethod
    def _validate_date_format(date_str: str | None, param_name: str) -> None:
        if date_str is None:
            return
        try:
            datetime.strptime(date_str, "%Y-%m-%d").date()  # noqa: DTZ007
        except ValueError as e:
            msg = f"{param_name} must be in YYYY-MM-DD format (e.g. '2024-01-01')"
            raise ValueError(msg) from e

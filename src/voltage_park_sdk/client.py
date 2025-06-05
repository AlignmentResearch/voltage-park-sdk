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
    VirtualMachine,
    VirtualMachines,
)


class VoltageParkClient:
    def __init__(self, token: str | Path) -> None:
        self._api_url = "https://cloud-api.voltagepark.com/api/v1/"
        self._token = token

    def headers(
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

    ################
    # GET requests #
    ################

    def get(self, endpoint: str, **params: str) -> Any:
        response = requests.get(
            f"{self._api_url}{endpoint}",
            headers=self.headers("get"),
            params=params,
            timeout=10,
        )
        return response.json()

    def get_locations(self) -> Locations:
        endpoint = "locations/"
        response = self.get(endpoint)
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

    def get_virtual_machines(self) -> VirtualMachines:
        endpoint = "virtual-machines/"
        response = self.get(endpoint)
        return VirtualMachines(**response)

    def get_virtual_machine(self, vm_id: str) -> VirtualMachine:
        endpoint = f"virtual-machines/{vm_id}"
        response = self.get(endpoint)
        return VirtualMachine(**response)

    def get_instant_deploy_presets(self) -> list[InstantDeployPreset]:
        endpoint = "instant-deploy-presets/"
        response = self.get(endpoint)
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

    def get_baremetal_rentals(self) -> BaremetalRentals:
        endpoint = "bare-metal/"
        response = self.get(endpoint)
        return BaremetalRentals(**response)

    def get_baremetal_rental(self, rental_id: str) -> BaremetalRental:
        msg = "Not implemented by the API"
        raise NotImplementedError(msg)

    def get_billing_hourly_rates(self) -> BillingHourlyRate:
        endpoint = "billing/hourly-rate"
        response = self.get(endpoint)
        return BillingHourlyRate(**response)

    def get_billing_transactions(self) -> BillingTransactions:
        endpoint = "billing/transactions/"
        response = self.get(endpoint)
        return BillingTransactions(**response)

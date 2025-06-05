# We are incrementally adding methods to the client as we need them, but
# writing method signatures for the whole API, so we need to ignore unused
# args and variables for the time being.
# ruff: noqa: ARG002, F841
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import requests

from voltage_park_sdk.datamodel.baremetal import (
    BaremetalLocations,
    BaremetalRentals,
)
from voltage_park_sdk.datamodel.organization import (
    Organization,
    OrganizationPatchPayload,
    OrganizationPatchResponse,
    SSHKeyCreatePayload,
    SSHKeyCreateResponse,
    SSHKeys,
)
from voltage_park_sdk.datamodel.shared import (
    OrganizationSSHKey,
    get_organization_ssh_key,
)
from voltage_park_sdk.datamodel.virtual_machines import (
    VirtualMachine,
    VirtualMachineCloudInit,
    VirtualMachineDeployPayload,
    VirtualMachineDeployResponse,
    VirtualMachineLocation,
    VirtualMachineLocations,
    VirtualMachinePatchPayload,
    VirtualMachinePatchResponse,
    VirtualMachinePowerStatus,
    VirtualMachinePowerStatusOptions,
    VirtualMachines,
)
from voltage_park_sdk.model import (
    BillingHourlyRate,
    BillingTransactions,
    MonthlyBillingReport,
    StorageHourlyRate,
    StorageVolume,
    StorageVolumes,
)


class VoltageParkClient:
    def __init__(self, token: str | Path) -> None:
        self._api_url = "https://cloud-api.voltagepark.com/api/v1/"
        self._token = token

    ################
    # Organization #
    ################

    def get_organization(self) -> Organization:
        endpoint = "organization"
        response = self.get(endpoint)
        return Organization(**response)

    def patch_organization(
        self,
        billing_notification_target_emails: list[str],
    ) -> Organization:
        payload = OrganizationPatchPayload(
            billing_notification_target_emails=billing_notification_target_emails,
        )
        endpoint = "organization"
        response = self.patch(endpoint, **payload.model_dump())
        return OrganizationPatchResponse(**response)

    def get_ssh_keys(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SSHKeys:
        endpoint = "organization/ssh-keys"
        response = self.get(endpoint, limit=limit, offset=offset)
        return SSHKeys(**response)

    def post_ssh_key(
        self,
        name: str,
        content: str,
    ) -> SSHKeyCreateResponse:
        payload = SSHKeyCreatePayload(
            name=name,
            content=content,
        )
        endpoint = "organization/ssh-keys"
        response = self.post(endpoint, **payload.model_dump())
        return SSHKeyCreateResponse(**response)

    def delete_ssh_key(self, ssh_key_id: str) -> None:
        endpoint = f"organization/ssh-keys/{ssh_key_id}"
        self.delete(endpoint)

    ####################
    # Virtual machines #
    ####################

    def get_virtual_machine_locations(self) -> VirtualMachineLocations:
        endpoint = "virtual-machines/instant/locations/"
        response = self.get(endpoint)
        return VirtualMachineLocations(**response)

    def get_virtual_machine_location(
        self,
        location_id: str,
    ) -> VirtualMachineLocation:
        endpoint = f"virtual-machines/instant/locations/{location_id}"
        response = self.get(endpoint)
        return VirtualMachineLocation(**response)

    def post_new_virtual_machine(  # noqa: PLR0913
        self,
        config_id: str,
        name: str,
        password: str | None = None,
        organization_ssh_keys: OrganizationSSHKey | dict[str, Any] | None = None,
        ssh_keys: list[str] | None = None,
        cloud_init: VirtualMachineCloudInit | dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> VirtualMachineDeployResponse:
        organization_ssh_keys = get_organization_ssh_key(organization_ssh_keys)
        if isinstance(cloud_init, dict):
            cloud_init = VirtualMachineCloudInit(**cloud_init)

        payload = VirtualMachineDeployPayload(
            config_id=config_id,
            name=name,
            password=password,
            organization_ssh_keys=organization_ssh_keys,
            ssh_keys=ssh_keys,
            cloud_init=cloud_init,
            tags=tags,
        )
        endpoint = "virtual-machines/instant/locations/"
        response = self.post(endpoint, **payload.model_dump())
        return VirtualMachineDeployResponse(**response)

    def get_virtual_machines(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> VirtualMachines:
        endpoint = "virtual-machines/"
        response = self.get(endpoint, limit=limit, offset=offset)
        return VirtualMachines(**response)

    def get_virtual_machine(self, virtual_machine_id: str) -> VirtualMachine:
        endpoint = f"virtual-machines/{virtual_machine_id}"
        response = self.get(endpoint)
        return VirtualMachine(**response)

    def patch_virtual_machine(
        self,
        virtual_machine_id: str,
        name: str | None = None,
        tags: list[str] | None = None,
    ) -> VirtualMachinePatchResponse:
        payload = VirtualMachinePatchPayload(
            name=name,
            tags=tags,
        )
        endpoint = f"virtual-machines/{virtual_machine_id}"
        response = self.patch(endpoint, **payload.model_dump())
        return VirtualMachinePatchResponse(**response)

    def delete_virtual_machine(self, virtual_machine_id: str) -> None:
        endpoint = f"virtual-machines/{virtual_machine_id}"
        self.delete(endpoint)

    def put_vm_power_status(
        self,
        virtual_machine_id: str,
        status: VirtualMachinePowerStatusOptions,
    ) -> VirtualMachinePowerStatus:
        payload = VirtualMachinePowerStatus(status=status)
        endpoint = f"virtual-machines/{virtual_machine_id}/power-status"
        response = self.put(endpoint, **payload.model_dump())
        return VirtualMachinePowerStatus(**response)

    def post_relocate_virtual_machine(
        self,
        virtual_machine_id: str,
    ) -> None:
        endpoint = f"virtual-machines/{virtual_machine_id}/relocate"
        self.post(endpoint)

    #####################
    # Baremetal rentals #
    #####################

    def get_baremetal_locations(self) -> BaremetalLocations:
        endpoint = "bare-metal/locations/"
        response = self.get(endpoint)
        return BaremetalLocations(**response)

    def post_new_baremetal_rental(  # noqa: PLR0913
        self,
        location_id: str,
        gpu_count: int,
        network_type: Literal["infiniband", "ethernet"],
        organization_ssh_keys: dict[str, Any] | None = None,
        ssh_keys: list[str] | None = None,
        suborder: int | None = None,
        storage_id: str | None = None,
        tags: list[str] | None = None,
        cloudinit_script: dict[str, Any] | None = None,
    ) -> str:
        endpoint = "bare-metal/"
        msg = "Not currently implemented by the SDK"
        raise NotImplementedError(msg)

    def get_baremetal_rentals(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> BaremetalRentals:
        endpoint = "bare-metal/"
        response = self.get(endpoint, limit=limit, offset=offset)
        return BaremetalRentals(**response)

    def post_reboot_baremetal_rental(
        self,
        baremetal_rental_id: str,
        public_ips: list[str],
    ) -> None:
        endpoint = f"bare-metal/{baremetal_rental_id}/reboot"
        msg = "Not currently implemented by the SDK"
        raise NotImplementedError(msg)

    def patch_baremetal_rental(
        self,
        baremetal_rental_id: str,
        name: str | None = None,
        tags: list[str] | None = None,
    ) -> None:
        endpoint = f"bare-metal/{baremetal_rental_id}"
        msg = "Not currently implemented by the SDK"
        raise NotImplementedError(msg)

    def put_baremetal_rental_power_status(
        self,
        baremetal_rental_id: str,
        status: Literal["started", "stopped"],
    ) -> None:
        endpoint = f"bare-metal/{baremetal_rental_id}/power-status"
        msg = "Not currently implemented by the SDK"
        raise NotImplementedError(msg)

    def delete_baremetal_rental(self, baremetal_rental_id: str) -> None:
        endpoint = f"bare-metal/{baremetal_rental_id}"
        msg = "Not currently implemented by the SDK"
        raise NotImplementedError(msg)

    ###########
    # Storage #
    ###########

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

    def post_new_storage_volume(
        self,
        size_in_gb: int,
        name: str,
        order_ids: list[str] | None = None,
    ) -> str:
        endpoint = "storage"
        msg = "Not currently implemented by the SDK"
        raise NotImplementedError(msg)

    def patch_storage_volume(
        self,
        storage_id: str,
        size_in_gb: int | None = None,
        name: str | None = None,
        order_ids: list[str] | None = None,
    ) -> None:
        endpoint = f"storage/{storage_id}"
        msg = "Not currently implemented by the SDK"
        raise NotImplementedError(msg)

    def delete_storage_volume(self, storage_id: str) -> None:
        endpoint = f"storage/{storage_id}"
        msg = "Not currently implemented by the SDK"
        raise NotImplementedError(msg)

    #########################
    # Cloudinit validation #
    #########################

    def post_validate_cloudinit_script(
        self,
        type: Literal["instant-vm", "vm", "baremetal"],  # noqa: A002
        content: str,
    ) -> str:
        endpoint = "validate/cloudinit"
        msg = "Not currently implemented by the SDK"
        raise NotImplementedError(msg)

    ###########
    # Billing #
    ###########

    def get_billing_hourly_rates(self) -> BillingHourlyRate:
        endpoint = "billing/hourly-rate"
        response = self.get(endpoint)
        return BillingHourlyRate(**response)

    def get_storage_hourly_rate(self) -> StorageHourlyRate:
        endpoint = "storage/hourly-rate"
        response = self.get(endpoint)
        return StorageHourlyRate(**response)

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

    ##################
    # Public helpers #
    ##################

    def get(self, endpoint: str, **params: Any) -> Any:
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(
            f"{self._api_url}{endpoint}",
            headers=self._headers("get"),
            data=json.dumps(params),
            timeout=10,
        )
        return response.json()

    def post(self, endpoint: str, **params: Any) -> Any:
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.post(
            f"{self._api_url}{endpoint}",
            headers=self._headers("post"),
            data=json.dumps(params),
            timeout=10,
        )
        return response.json()

    def patch(self, endpoint: str, **params: Any) -> Any:
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.patch(
            f"{self._api_url}{endpoint}",
            headers=self._headers("patch"),
            data=json.dumps(params),
            timeout=10,
        )
        return response.json()

    def delete(self, endpoint: str) -> Any:
        response = requests.delete(
            f"{self._api_url}{endpoint}",
            headers=self._headers("delete"),
            timeout=10,
        )
        try:
            return response.json()
        except json.JSONDecodeError:
            return None

    def put(self, endpoint: str, **params: Any) -> Any:
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.put(
            f"{self._api_url}{endpoint}",
            headers=self._headers("put"),
            data=json.dumps(params),
            timeout=10,
        )
        return response.json()

    ###################
    # Private helpers #
    ###################

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

    @staticmethod
    def _validate_date_format(date_str: str | None, param_name: str) -> None:
        if date_str is None:
            return
        try:
            datetime.strptime(date_str, "%Y-%m-%d").date()  # noqa: DTZ007
        except ValueError as e:
            msg = f"{param_name} must be in YYYY-MM-DD format (e.g. '2024-01-01')"
            raise ValueError(msg) from e

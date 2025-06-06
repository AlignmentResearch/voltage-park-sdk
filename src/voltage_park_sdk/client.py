# We are incrementally adding methods to the client as we need them, but
# writing method signatures for the whole API, so we need to ignore unused
# args and variables for the time being.
# ruff: noqa: ARG002, F841
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import requests
from pydantic import ValidationError

from voltage_park_sdk.datamodel.baremetal import (
    BaremetalCloudInit,
    BaremetalLocations,
    BaremetalNetworkTypeOptions,
    BaremetalRentalCreatePayload,
    BaremetalRentalCreateResponse,
    BaremetalRentalPatchPayload,
    BaremetalRentalPatchResponse,
    BaremetalRentalPowerStatusPayload,
    BaremetalRentalPutPowerStatusOptions,
    BaremetalRentalRebootNodesPayload,
    BaremetalRentalRemoveNodesPayload,
    BaremetalRentals,
)
from voltage_park_sdk.datamodel.billing import (
    BillingHourlyRate,
    BillingResourceTypeOptions,
    BillingTransactionsPayload,
    BillingTransactionsResponse,
    MonthlyBillingReport,
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
from voltage_park_sdk.datamodel.storage import (
    StorageHourlyRate,
    StorageVolumeCreatePayload,
    StorageVolumeCreateResponse,
    StorageVolumeGetResponse,
    StorageVolumePatchPayload,
    StorageVolumePatchResponse,
    StorageVolumesGetResponse,
)
from voltage_park_sdk.datamodel.validation import (
    CloudinitValidationPayload,
    CloudinitValidationResponse,
    CloudinitValidationTypeOptions,
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
    VirtualMachinePowerStatusOptions,
    VirtualMachinePowerStatusPayload,
    VirtualMachinePowerStatusResponse,
    VirtualMachines,
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
        return self._format_response(response, OrganizationPatchResponse)

    def get_ssh_keys(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SSHKeys:
        endpoint = "organization/ssh-keys"
        response = self.get(endpoint, limit=limit, offset=offset)
        return self._format_response(response, SSHKeys)

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
        return self._format_response(response, SSHKeyCreateResponse)

    def delete_ssh_key(self, ssh_key_id: str) -> Any:
        endpoint = f"organization/ssh-keys/{ssh_key_id}"
        # Don't decode the response, as it's None if the key was deleted
        # and we want the raw response if there was an error
        return self.delete(endpoint)

    ####################
    # Virtual machines #
    ####################

    def get_virtual_machine_locations(self) -> VirtualMachineLocations:
        endpoint = "virtual-machines/instant/locations/"
        response = self.get(endpoint)
        return self._format_response(response, VirtualMachineLocations)

    def get_virtual_machine_location(
        self,
        location_id: str,
    ) -> VirtualMachineLocation:
        endpoint = f"virtual-machines/instant/locations/{location_id}"
        response = self.get(endpoint)
        return self._format_response(response, VirtualMachineLocation)

    def post_virtual_machine(  # noqa: PLR0913
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
        endpoint = "virtual-machines/instant"
        response = self.post(endpoint, **payload.model_dump())
        return self._format_response(response, VirtualMachineDeployResponse)

    def get_virtual_machines(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> VirtualMachines:
        endpoint = "virtual-machines/"
        response = self.get(endpoint, limit=limit, offset=offset)
        return self._format_response(response, VirtualMachines)

    def get_virtual_machine(self, virtual_machine_id: str) -> VirtualMachine:
        endpoint = f"virtual-machines/{virtual_machine_id}"
        response = self.get(endpoint)
        return self._format_response(response, VirtualMachine)

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
        return self._format_response(response, VirtualMachinePatchResponse)

    def delete_virtual_machine(self, virtual_machine_id: str) -> Any:
        endpoint = f"virtual-machines/{virtual_machine_id}"
        # Don't decode the response, as it's None if the VM was deleted
        # and we want the raw response if there was an error
        return self.delete(endpoint)

    def put_vm_power_status(
        self,
        virtual_machine_id: str,
        status: VirtualMachinePowerStatusOptions,
    ) -> VirtualMachinePowerStatusResponse:
        payload = VirtualMachinePowerStatusPayload(status=status)
        endpoint = f"virtual-machines/{virtual_machine_id}/power-status"
        response = self.put(endpoint, **payload.model_dump())
        return self._format_response(response, VirtualMachinePowerStatusResponse)

    def post_relocate_virtual_machine(
        self,
        virtual_machine_id: str,
    ) -> Any:
        endpoint = f"virtual-machines/{virtual_machine_id}/relocate"
        # Don't decode the response, as it's None if the VM was relocated
        # and we want the raw response if there was an error
        return self.post(endpoint)

    #####################
    # Baremetal rentals #
    #####################

    def get_baremetal_locations(self) -> BaremetalLocations:
        endpoint = "bare-metal/locations/"
        response = self.get(endpoint)
        return self._format_response(response, BaremetalLocations)

    def post_baremetal_rental(  # noqa: PLR0913
        self,
        location_id: str,
        gpu_count: int,
        name: str,
        network_type: BaremetalNetworkTypeOptions,
        organization_ssh_keys: OrganizationSSHKey | dict[str, Any] | None = None,
        ssh_keys: list[str] | None = None,
        suborder: int | None = None,
        storage_id: str | None = None,
        tags: list[str] | None = None,
        cloudinit_script: BaremetalCloudInit | dict[str, Any] | None = None,
    ) -> BaremetalRentalCreateResponse:
        organization_ssh_keys = get_organization_ssh_key(organization_ssh_keys)
        if isinstance(cloudinit_script, dict):
            cloudinit_script = BaremetalCloudInit(**cloudinit_script)

        endpoint = "bare-metal/"
        payload = BaremetalRentalCreatePayload(
            location_id=location_id,
            gpu_count=gpu_count,
            name=name,
            organization_ssh_keys=organization_ssh_keys,
            ssh_keys=ssh_keys,
            network_type=network_type,
            suborder=suborder,
            storage_id=storage_id,
            tags=tags,
            cloudinit_script=cloudinit_script,
        )
        response = self.post(endpoint, **payload.model_dump())
        return self._format_response(response, BaremetalRentalCreateResponse)

    def get_baremetal_rentals(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> BaremetalRentals:
        endpoint = "bare-metal/"
        response = self.get(endpoint, limit=limit, offset=offset)
        return self._format_response(response, BaremetalRentals)

    def put_baremetal_rental_power_status(
        self,
        baremetal_rental_id: str,
        status: BaremetalRentalPutPowerStatusOptions,
    ) -> Any:
        payload = BaremetalRentalPowerStatusPayload(status=status)
        endpoint = f"bare-metal/{baremetal_rental_id}/power-status"
        # Don't decode the response as it's None if the power status was
        # properly set and we want the raw response if there was an error
        # or we tried to set the power status to the same value as the current
        # power status
        return self.put(endpoint, **payload.model_dump())

    def delete_baremetal_rental(self, baremetal_rental_id: str) -> Any:
        endpoint = f"bare-metal/{baremetal_rental_id}"
        # Don't decode the response, as it's None if the rental was deleted
        # and we want the raw response if there was an error
        return self.delete(endpoint)

    def patch_baremetal_rental(
        self,
        baremetal_rental_id: str,
        name: str | None = None,
        tags: list[str] | None = None,
    ) -> BaremetalRentalPatchResponse:
        payload = BaremetalRentalPatchPayload(
            name=name,
            tags=tags,
        )
        endpoint = f"bare-metal/{baremetal_rental_id}"
        response = self.patch(endpoint, **payload.model_dump())
        return self._format_response(response, BaremetalRentalPatchResponse)

    def post_reboot_baremetal_rental_nodes(
        self,
        baremetal_rental_id: str,
        public_ips: list[str],
    ) -> Any:
        endpoint = f"bare-metal/{baremetal_rental_id}/reboot"
        payload = BaremetalRentalRebootNodesPayload(
            public_ips=public_ips,
        )
        # Don't decode the response, as it's None if the nodes were rebooted
        # and we want the raw response if there was an error
        return self.post(endpoint, **payload.model_dump())

    def patch_remove_baremetal_rental_nodes(
        self,
        baremetal_rental_id: str,
        public_ips: list[str],
    ) -> Any:
        endpoint = f"bare-metal/{baremetal_rental_id}/remove-nodes"
        payload = BaremetalRentalRemoveNodesPayload(
            public_ips=public_ips,
        )
        # Don't decode the response, as it's None if the nodes were removed
        # and we want the raw response if there was an error
        return self.patch(endpoint, **payload.model_dump())

    ###########
    # Billing #
    ###########

    def get_billing_hourly_rate(self) -> BillingHourlyRate:
        endpoint = "billing/hourly-rate"
        response = self.get(endpoint)
        return self._format_response(response, BillingHourlyRate)

    def get_billing_transactions(
        self,
        limit: int | None = None,
        offset: int | None = None,
        types: list[BillingResourceTypeOptions] | None = None,
        earliest: str | None = None,
        latest: str | None = None,
    ) -> BillingTransactionsResponse:
        payload = BillingTransactionsPayload(
            limit=limit,
            offset=offset,
            types=types,
            earliest=earliest,
            latest=latest,
        )
        endpoint = "billing/transactions/"
        response = self.get(endpoint, **payload.model_dump())
        return self._format_response(response, BillingTransactionsResponse)

    def get_monthly_billing_report(
        self,
        year: int,
        month: int,
    ) -> MonthlyBillingReport:
        endpoint = f"billing/reports/{year}/{month}/transactions"
        response = self.get(endpoint)
        return self._format_response(response, MonthlyBillingReport)

    #########################
    # Cloudinit validation #
    #########################

    def post_validate_cloudinit_script(
        self,
        type: CloudinitValidationTypeOptions,  # noqa: A002
        content: str,
    ) -> CloudinitValidationResponse:
        payload = CloudinitValidationPayload(
            type=type,
            content=content,
        )
        endpoint = "validate/cloudinit"
        response = self.post(endpoint, **payload.model_dump())
        return self._format_response(response, CloudinitValidationResponse)

    ###########
    # Storage #
    ###########

    def get_storage_hourly_rate(self) -> StorageHourlyRate:
        endpoint = "storage/hourly-rate"
        response = self.get(endpoint)
        return self._format_response(response, StorageHourlyRate)

    def get_storage_volumes(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> StorageVolumesGetResponse:
        endpoint = "storage"
        response = self.get(endpoint, limit=limit, offset=offset)
        return self._format_response(response, StorageVolumesGetResponse)

    def get_storage_volume(self, storage_id: str) -> StorageVolumeGetResponse:
        endpoint = f"storage/{storage_id}"
        response = self.get(endpoint)
        return self._format_response(response, StorageVolumeGetResponse)

    def post_new_storage_volume(
        self,
        size_in_gb: int,
        name: str,
        order_ids: list[str],
    ) -> StorageVolumeCreateResponse:
        endpoint = "storage"
        payload = StorageVolumeCreatePayload(
            size_in_gb=size_in_gb,
            name=name,
            order_ids=order_ids,
        )
        response = self.post(endpoint, **payload.model_dump())
        return self._format_response(response, StorageVolumeCreateResponse)

    def patch_storage_volume(
        self,
        storage_id: str,
        size_in_gb: int | None = None,
        name: str | None = None,
        order_ids: list[str] | None = None,
    ) -> Any:
        endpoint = f"storage/{storage_id}"
        payload = StorageVolumePatchPayload(
            size_in_gb=size_in_gb,
            name=name,
            order_ids=order_ids,
        )
        # Don't decode the response, as it's None if the storage volume was
        # patched and we want the raw response if there was an error
        response = self.patch(endpoint, **payload.model_dump())
        return self._format_response(response, StorageVolumePatchResponse)

    def delete_storage_volume(self, storage_id: str) -> Any:
        endpoint = f"storage/{storage_id}"
        # Don't decode the response, as it's None if the storage volume was
        # deleted and we want the raw response if there was an error
        return self.delete(endpoint)

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
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, **params: Any) -> Any:
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.post(
            f"{self._api_url}{endpoint}",
            headers=self._headers("post"),
            data=json.dumps(params),
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def patch(self, endpoint: str, **params: Any) -> Any:
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.patch(
            f"{self._api_url}{endpoint}",
            headers=self._headers("patch"),
            data=json.dumps(params),
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> Any:
        response = requests.delete(
            f"{self._api_url}{endpoint}",
            headers=self._headers("delete"),
            timeout=10,
        )
        response.raise_for_status()
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
        response.raise_for_status()
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

    def _format_response[ResponseT](
        self, response: Any, response_class: type[ResponseT]
    ) -> ResponseT:
        try:
            return response_class(**response)
        except ValidationError as e:
            print(f"Raw response: {response}")  # noqa: T201
            raise

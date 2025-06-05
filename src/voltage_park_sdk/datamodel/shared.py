from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, Field

GPUModelOptions = Literal[
    "h100-sxm5-80gb",
    "v100-sxm2-16gb",
    "v100-sxm2-32gb",
    "v100-sxm3-32gb",
    "a100-sxm4-80gb",
    "a100-pcie-80gb",
    "a100-pcie-40gb",
    "a40-pcie-48gb",
    "a2-pcie-16gb",
    "l40s-pcie-48gb",
    "l40-pcie-48gb",
    "l4-pcie-24gb",
    "rtx6000ada-pcie-48gb",
    "rtx5000ada-pcie-32gb",
    "rtx4500ada-pcie-24gb",
    "rtx4000ada-pcie-20gb",
    "rtx4000sffada-pcie-20gb",
    "rtxa6000-pcie-48gb",
    "rtxa5500-pcie-24gb",
    "rtxa5000-pcie-24gb",
    "rtxa4500-pcie-20gb",
    "rtxa4000-pcie-16gb",
    "quadrortx8000-pcie-48gb",
    "quadrortx6000-pcie-48gb",
    "teslap4-pcie-8gb",
    "teslap100-sxm2-16gb",
    "teslap100-pcie-16gb",
    "teslam40-pcie-24gb",
    "geforcertx4090-pcie-24gb",
    "geforcertx4080super-pcie-16gb",
    "geforcertx4080-pcie-16gb",
    "geforcertx4070tisuper-pcie-16gb",
    "geforcertx3090ti-pcie-24gb",
    "geforcertx3090-pcie-24gb",
    "geforcertx3080ti-pcie-12gb",
    "geforcertx3080-pcie-10gb",
    "geforcertx3080lhr-pcie-10gb",
    "geforcertx3070ti-pcie-8gb",
    "geforcertx3070-pcie-8gb",
    "geforcertx3060ti-pcie-8gb",
    "geforcertx3060tilhr-pcie-8gb",
    "geforcertx3060lhr-pcie-12gb",
    "geforcertx3060-pcie-12gb",
    "geforcertx3050-pcie-8gb",
    "geforcertx2080ti-pcie-11gb",
    "geforcertx2080super-pcie-8gb",
    "geforcertx2060super-pcie-8gb",
    "geforcegtx1650-pcie-4gb",
    "geforcegtx1070-pcie-8gb",
    "geforcegtx1060-pcie-6gb",
    "geforcegtx1660super-pcie-6gb",
    "geforecegt710-pcie-1gb",
]

ResponseT = TypeVar("ResponseT", bound=BaseModel)


class ListResponse(BaseModel, Generic[ResponseT]):
    results: list[ResponseT]
    total_result_count: int
    has_previous: bool
    has_next: bool


class CloudInitFile(BaseModel):
    content: str
    path: str
    encoding: str | None = None
    owner: str | None = None
    permissions: str | None = None


class OrganzationSSHKeyNone(BaseModel):
    mode: Literal["none"] = "none"


class OrganzationSSHKeyAll(BaseModel):
    mode: Literal["all"] = "all"


class OrganzationSSHKeySelective(BaseModel):
    mode: Literal["selective"] = "selective"
    ssh_keys: list[str] = Field(
        description="A list of organization SSH keys to use for the rental",
    )


OrganizationSSHKey = (
    OrganzationSSHKeyNone | OrganzationSSHKeyAll | OrganzationSSHKeySelective
)


def get_organization_ssh_key(
    ssh_key: dict[str, Any] | OrganizationSSHKey | None,
) -> OrganizationSSHKey:
    if isinstance(ssh_key, OrganizationSSHKey):
        return ssh_key
    if ssh_key is None or ssh_key.get("mode") is None:
        return OrganzationSSHKeyNone()
    if ssh_key.get("mode") == "all":
        return OrganzationSSHKeyAll()
    if ssh_key.get("mode") == "selective":
        return OrganzationSSHKeySelective(ssh_keys=ssh_key.get("ssh_keys", []))

    msg = f"Invalid SSH key mode: {ssh_key.get('mode')}"
    raise ValueError(msg)

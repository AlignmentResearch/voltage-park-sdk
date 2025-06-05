from pydantic import BaseModel, Field

from voltage_park_sdk.datamodel.shared import ListResponse


# GET organization
class Organization(BaseModel):
    id: str = Field(description="The ID of the organization")
    name: str = Field(description="The name of the organization")
    billing_notification_target_emails: list[str] = Field(
        description=(
            "A list of email addresses to which billing-related emails will "
            "be sent, in addition to all registered users of the organization."
        )
    )


# PATCH organization
class OrganizationPatchPayload(BaseModel):
    billing_notification_target_emails: list[str] = Field(
        description=(
            "A list of email addresses to which billing-related emails will "
            "be sent, in addition to all registered users of the organization."
        )
    )


class OrganizationPatchResponse(Organization):
    pass


# GET organization/ssh-keys
class SSHKey(BaseModel):
    id: str = Field(description="The ID of the SSH key")
    name: str = Field(description="The name of the SSH key")
    content: str = Field(description="The content of the SSH key")


class SSHKeys(ListResponse[SSHKey]):
    pass


# POST organization/ssh-keys
class SSHKeyCreatePayload(BaseModel):
    name: str = Field(description="The name of the SSH key")
    content: str = Field(description="The content of the SSH key")


class SSHKeyCreateResponse(SSHKey):
    pass

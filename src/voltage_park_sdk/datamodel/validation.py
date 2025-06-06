from typing import Literal

from pydantic import BaseModel, Field

CloudinitValidationTypeOptions = Literal["instant-vm", "vm", "baremetal"]


# POST validate/cloudinit
class CloudinitValidationPayload(BaseModel):
    type: CloudinitValidationTypeOptions = Field(
        description="The type of cloudinit script",
    )
    content: str = Field(
        description="The content of the cloudinit script",
    )


class CloudinitValidationResponse(BaseModel):
    error: bool = Field(
        description="Whether the cloudinit script is valid",
    )
    message: str | None = Field(
        description="The error message if the cloudinit script is invalid",
    )

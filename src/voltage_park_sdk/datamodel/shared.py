from typing import Generic, TypeVar

from pydantic import BaseModel

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


class CloudInit(BaseModel):
    packages: list[str] | None = None
    write_files: list[CloudInitFile] | None = None
    runcmd: list[str] | None = None

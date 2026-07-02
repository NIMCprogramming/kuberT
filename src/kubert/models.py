from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class ManualCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["manual"]


class CommandCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["command"]
    cmd: str
    expect: str
    timeout_seconds: int = 30


class MultipleCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["multiple"]
    checks: list[CommandCheck]


Check = Annotated[
    ManualCheck | CommandCheck | MultipleCheck,
    Field(discriminator="type"),
]


Requirement = Literal["cluster"]


class Lesson(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    module: str
    order: int
    estimated_minutes: int = 5
    intro: str
    task: str
    hint: str = ""
    check: Check
    requires: list[Requirement] = Field(default_factory=list)


class UserProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    completed_lessons: list[str] = Field(default_factory=list)
    current_cluster_name: str | None = None

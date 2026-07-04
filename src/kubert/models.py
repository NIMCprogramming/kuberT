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


QuestionKind = Literal["recall", "multiple_choice", "debug", "scenario"]


class Question(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str
    answer: str
    kind: QuestionKind = "recall"
    options: list[str] = Field(default_factory=list)
    concept: str = ""


class Troubleshooting(BaseModel):
    model_config = ConfigDict(extra="forbid")
    scenario: str
    question: str
    diagnosis: str
    concept: str = ""


class Mistake(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mistake: str
    fix: str


RevisitWhen = Literal["next", "2-3", "5-7", "capstone"]


class SpacedHook(BaseModel):
    model_config = ConfigDict(extra="forbid")
    concept: str
    when: RevisitWhen


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
    cheat: str = ""
    check: Check
    requires: list[Requirement] = Field(default_factory=list)
    learning_goal: str = ""
    prerequisites: list[str] = Field(default_factory=list)
    warm_up: list[Question] = Field(default_factory=list)
    troubleshooting: Troubleshooting | None = None
    review_questions: list[Question] = Field(default_factory=list)
    common_mistakes: list[Mistake] = Field(default_factory=list)
    summary: str = ""
    spaced_hooks: list[SpacedHook] = Field(default_factory=list)


class MissedConcept(BaseModel):
    model_config = ConfigDict(extra="forbid")
    concept: str
    lesson_id: str
    count: int = 1


class UserProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    completed_lessons: list[str] = Field(default_factory=list)
    current_cluster_name: str | None = None
    missed_concepts: list[MissedConcept] = Field(default_factory=list)

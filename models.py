from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class SchoolNote(BaseModel):
    school_name: str = Field(description="Name of the school")
    reason_for_absence: str = Field(description="Reason for the absence")
    date_of_return: str = Field(description="Date of return to school")


class PopulateResult(BaseModel):
    completed: bool = Field(description="Whether the template was fully populated")
    questions: list[str] | None = Field(
        default=None,
        description="Follow-up questions to ask the parent if not completed",
    )
    template: SchoolNote | None = Field(
        default=None, description="Populated template if completed"
    )

    @model_validator(mode="after")
    def validate_result(self):
        if self.completed and self.template is None:
            raise ValueError("Template is required when completed is True")
        if not self.completed and not self.questions:
            raise ValueError("Questions are required when completed is False")
        return self


class PopulateRequest(BaseModel):
    conversation_history: str

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class SchoolNote(BaseModel):
    student_first_name: str = Field(description="Student's first name")
    student_last_name: str = Field(description="Student's last name")
    school_name: str = Field(description="Name of the school")
    grade: str = Field(description="Grade level, e.g. '5th', '10th'")
    absence_date: str = Field(
        description="Date or date range of absence in YYYY-MM-DD format"
    )
    reason: str = Field(description="Reason for the absence")
    parent_guardian_name: str = Field(
        description="Full name of the parent or guardian"
    )
    additional_notes: str | None = Field(
        default=None, description="Any additional context or requests"
    )


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

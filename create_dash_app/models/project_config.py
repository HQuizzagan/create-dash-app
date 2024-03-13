from typing import Any, List

from pydantic import BaseModel, Field, field_validator


class ProjectConfig(BaseModel):
    """Defines the required and optional fields for the project configuration."""

    project_name: str = Field(..., description="The name of the project.")
    author_name: str = Field(..., description="The name of the author.")
    author_email: str = Field(..., description="The email of the author.")
    description: str = Field(..., description="The description of the project.")
    styling: List[str] = Field(default=[], description="The styling framework to use.")
    animations: List[str] = Field(default=[], description="The animation library to use.")
    include_pages: bool = Field(default=False, description="Whether to include pages.")
    include_tests: bool = Field(default=True, description="Whether to include pytest scaffolding.")
    include_auth: bool = Field(default=False, description="Whether to include authentication.")
    include_database: bool = Field(default=False, description="Whether to include a database.")
    include_docker: bool = Field(
        default=True, description="Whether to include a Dockerfile and docker-compose.yml."
    )
    configure_pre_commit: bool = Field(
        default=True,
        description=(
            "Whether to include pre-commit hook configuration for linting and formatting "
            "for the generated project."
        ),
    )
    port: int = Field(default=8000, description="The port to run the application on.")

    @field_validator("styling", "animations", mode="before")
    @classmethod
    def validate_none(cls, value: Any) -> List[str]:
        """Either
        - removes `none` from the list of values if there are other values in the list, or
        - returns an empty list if `none` is the only value in the list
        """
        if not value:
            return []

        # Convert to list if it's not already (e.g., if it's a string)
        if not isinstance(value, list):
            value = [value]

        # Remove "none" from the list
        filtered: List[str] = [v for v in value if v != "none"]  # type: ignore

        # If "none" was the only value, return empty list
        if "none" in value and not filtered:
            return []

        return filtered

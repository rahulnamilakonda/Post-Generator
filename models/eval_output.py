from typing import Annotated, Literal
from pydantic import BaseModel, Field


class EvalOutputSchema(BaseModel):
    status: Literal["approved", "refused"] = Field(
        description="This is status of the post"
    )
    feedback: Annotated[
        str,
        Field(
            description="A breif description as why the post is approved or refused, so to use to for the next iteration for improvement"
        ),
    ]

from pydantic import BaseModel, Field
from typing import List


class Body(BaseModel):
    text: str = Field(description="The input text to analyze.")


class Suggestion(BaseModel):
    sentence: str = Field(description="The incorrect sentence from the input.")
    correct: str = Field(description="The grammatically correct version.")
    reason: str = Field(
        description="Explanation of what was wrong and how it was corrected."
    )


class Response(BaseModel):
    suggestions: List[Suggestion] = Field(
        description="The list of suggestions for the input text."
    )

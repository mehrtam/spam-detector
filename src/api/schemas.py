# src/api/schemas.py

from pydantic import BaseModel, field_validator


class PredictRequest(BaseModel):
    text: str
    sender_email: str | None = None

    @field_validator("text")
    @classmethod
    def text_must_be_valid(cls, v):
        if not v or not v.strip():
            raise ValueError("text cannot be empty")
        if len(v) > 10000:
            raise ValueError("text exceeds maximum length")
        return v.strip().lower()


class PredictResponse(BaseModel):
    is_spam: bool
    confidence: float
    model_version: str

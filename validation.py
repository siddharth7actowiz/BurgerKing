from pydantic import BaseModel, field_validator, HttpUrl
from typing import Optional
import re


class Store(BaseModel):
    name:     str
    store_id : Optional[int]=None
    city:     Optional[str] = None
    state:    Optional[str] = None
    address:  Optional[str] = None
    phone:    Optional[str] = None
    timings:  Optional[str] = None
    website:  Optional[str] = None
    map_url:  Optional[str] = None

    # ── name ──────────────────────────────────────────────────────────────────
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("name must not be empty")
        return v.strip()

    # ── city / state ──────────────────────────────────────────────────────────
    @field_validator("city", "state", mode="before")
    @classmethod
    def clean_text(cls, v):
        if v is None or v.strip() == "":
            return None
        return v.strip().title()

    # ── address ───────────────────────────────────────────────────────────────
    @field_validator("address", mode="before")
    @classmethod
    def clean_address(cls, v):
        if v is None or v.strip() == "":
            return None
        return " ".join(v.split())   # collapse extra whitespace

    # ── phone ─────────────────────────────────────────────────────────────────
    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone(cls, v):
        if v is None or v.strip() == "":
            return None
        digits = re.sub(r"\D", "", v)
        if len(digits) < 10:
            raise ValueError(f"Invalid phone number: '{v}'")
        return v.strip()

    # ── timings ───────────────────────────────────────────────────────────────
    @field_validator("timings", mode="before")
    @classmethod
    def clean_timings(cls, v):
        if v is None or v.strip() == "":
            return None
        return v.strip()

    # ── website / map_url ─────────────────────────────────────────────────────
    @field_validator("website", "map_url", mode="before")
    @classmethod
    def validate_url(cls, v):
        if v is None or v.strip() == "":
            return None
        if not v.startswith("http"):
            raise ValueError(f"Invalid URL: '{v}'")
        return v.strip()
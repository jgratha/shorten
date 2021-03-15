from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ShortenRequestDto(BaseModel):
    url: Optional[str]
    shortcode: Optional[str]


class ShortcodeStatsDto(BaseModel):
    created: datetime
    lastRedirect: Optional[datetime]
    redirectCount: int


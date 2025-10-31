from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Tuple, Dict
import re
from app.utils.verify_utils import VerifyUtils


@dataclass
class DeckCreateDTO:
    """Model to create a deck"""

    creator_id: int
    name: str
    bio: str
    access: Optional[str]
    image: str
    access_key: Optional[str]

    VALID_ACCESS = {"PUBLIC", "PRIVATE", "PROTECTED"}

    def from_json(data: dict) -> Tuple[Optional["DeckCreateDTO"], Optional[Dict]]:
        """Validate and parse a JSON dict into a DeckCreateDTO"""
        if not data:
            return None, {"error": "No data provided"}
        creator_id = data.get("creator_id")
        name = (data.get("name") or "").strip().capitalize()
        bio = (data.get("bio") or "").strip()
        access = (data.get("access") or "").strip()
        image = (data.get("image") or "").strip()
        access_key = (data.get("access_key") or "").strip()

        required_fields = {"name": name, "creator_id": creator_id}
        # verify required
        for field, value in required_fields.items():
            if not value:
                return None, {"error": f"Missing field: {field}"}
        # verify access
        if access not in DeckCreateDTO.VALID_ACCESS:
            return None, {
                "error": f"Invalid access. Must be one of {DeckCreateDTO.VALID_ACCESS}"
            }
        if access == "PROTECTED":
            if access_key == None:
                return None, {"error": f"protected decks must have a valid access_key"}
        if access != "PROTECTED":
            access_key = None
        # verify image format
        if not VerifyUtils.is_valid_image(image):
            return None, {"error": "image format invalid"}
        # verify password
        # pour l'instant on passe
        return (
            DeckCreateDTO(
                creator_id=creator_id,
                name=name,
                bio=bio,
                access=access,
                image=image,
                access_key=access_key,
            ),
            None,
        )

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Tuple, Dict
import re
from app.utils.verify_utils import VerifyUtils


@dataclass
class TagCreateDTO:

    name: str
    description: str

    # todo rajouter une verification, est ce que le tag existe déja ?
    @staticmethod
    def from_json(data: dict) -> Tuple[Optional["TagCreateDTO"], Optional[Dict]]:
        """Validate and parse a JSON dict into a TagCreateDTO"""
        if not data:
            return None, {"error": "No data provided"}

        name = (data.get("name") or "").strip().capitalize()
        description = (data.get("description") or "").strip().capitalize()

        required_fields = {"name": name, "description": description}
        for field, value in required_fields.items():
            if not value:
                return None, {"error": f"Missing field: {field}"}

        return TagCreateDTO(name=name, description=description), None


@dataclass
class TagPatchDTO:
    """Model to patch a Tag"""

    name: Optional[str]
    description: Optional[str]

    @staticmethod
    def from_json(data: dict) -> Tuple[Optional["TagPatchDTO"], Optional[Dict]]:
        """Validate and parse a JSON dict into a TagPatchDTO"""
        if not data:
            return None, {"error": "No data provided"}

        name = data.get("name")
        description = data.get("description")

        if name is not None:
            name = name.strip().capitalize()
        if description is not None:
            description = description.strip().capitalize()

        return TagPatchDTO(name=name, description=description), None

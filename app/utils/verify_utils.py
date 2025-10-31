import re
from datetime import datetime, date
from typing import Optional


class VerifyUtils:
    EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")
    IMAGE_REGEX = re.compile(r"^.+\.(jpg|jpeg|png|gif|bmp|webp)$", re.IGNORECASE)
    PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$")
    VALID_GENDERS = {"M", "F", "U"}

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return bool(VerifyUtils.EMAIL_REGEX.match(email))

    @staticmethod
    def is_valid_password(password: str) -> bool:
        return bool(VerifyUtils.PASSWORD_REGEX.match(password))

    @staticmethod
    def is_valid_gender(gender: str) -> bool:
        return gender in VerifyUtils.VALID_GENDERS

    @staticmethod
    def is_valid_image(image: str) -> bool:
        return bool(VerifyUtils.IMAGE_REGEX.match(image))

    @staticmethod
    def parse_birthdate(birthdate: Optional[str | date]) -> Optional[date]:
        if isinstance(birthdate, date):
            return birthdate
        if isinstance(birthdate, str):
            try:
                return datetime.strptime(birthdate, "%Y-%m-%d").date()
            except ValueError:
                return None
        return None

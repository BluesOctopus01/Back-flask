from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Tuple, Dict
import re


@dataclass
class UserCreateDTO:
    """Model to create a User"""

    username: str
    first_name: str
    last_name: str
    password: str
    email: str
    gender: str
    phone_number: str
    birthdate: date
    country: str
    address: str
    user_bio: Optional[str] = None
    image: Optional[str] = None

    # Authorized values
    VALID_GENDERS = {"M", "F", "U"}
    EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")

    PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$")

    # règle mot de passe
    # il doit y avoir au moins une lettre minuscule
    # il doit y avoir au moins une lettre majuscule
    # il doit y avoir au moins un chiffre
    # il doit y avoir au moins un caractère spécial parmi ceux listés
    # au moins 8 caractères au total
    @staticmethod
    def is_valid_password(password: str) -> bool:
        """Verify if the password is good enough else return False"""
        return bool(UserCreateDTO.PASSWORD_REGEX.match(password))

    @staticmethod
    def from_json(data: dict) -> Tuple[Optional["UserCreateDTO"], Optional[Dict]]:
        """Validate and parse a JSON dict into a UserCreateDTO"""

        if not data:
            return None, {"error": "No data provided"}

        # === Extracting Data | Normalization removing space | Captitalizing or lowering ===

        username = (data.get("username") or "").strip()
        first_name = (data.get("first_name") or "").strip().capitalize()
        last_name = (data.get("last_name") or "").strip().capitalize()
        password = (data.get("password") or "").strip()
        email = (data.get("email") or "").strip().lower()
        gender = (data.get("gender") or "").strip()
        phone_number = (data.get("phone_number") or "").strip()
        birthdate = data.get("birthdate")
        country = (data.get("country") or "").strip().capitalize()
        address = (data.get("address") or "").strip()
        user_bio = (data.get("user_bio") or "").strip() or None
        image = (data.get("image") or "").strip() or None

        # === Required fields ===

        required_fields = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "email": email,
            "gender": gender,
            "phone_number": phone_number,
            "birthdate": birthdate,
            "country": country,
            "address": address,
        }
        for field, value in required_fields.items():
            if not value:
                return None, {"error": f"Missing field: {field}"}

        # === Check the date format ===

        if isinstance(birthdate, str):
            try:
                birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d").date()
            except ValueError:
                return None, {"error": "birthdate must be in format YYYY-MM-DD"}
        elif isinstance(birthdate, date):
            birthdate_obj = birthdate
        else:
            return None, {"error": "birthdate must be a string or date"}

        # === Check if the gender is accepted ===

        if gender not in UserCreateDTO.VALID_GENDERS:
            return None, {
                "error": f"Invalid gender. Must be one of {UserCreateDTO.VALID_GENDERS}"
            }

        # === Check the mail format ===

        if not UserCreateDTO.EMAIL_REGEX.match(email):
            return None, {"error": "Invalid email format"}

        # === Checking password security ===

        if not UserCreateDTO.is_valid_password(password):
            return None, {
                "error": (
                    "Password must be at least 8 characters, "
                    "contain uppercase, lowercase, a number, and a special character."
                )
            }
        # todo === Verify image format ===
        return (
            UserCreateDTO(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email,
                gender=gender,
                phone_number=phone_number,
                birthdate=birthdate_obj,
                country=country,
                address=address,
                user_bio=user_bio,
                image=image,
            ),
            None,
        )

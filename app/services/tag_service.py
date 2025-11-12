from app.models.tags import Tag
from app.models.deck import Deck
from app.models import db


# region POST
def create_tag(name: str, description: str) -> Tag:
    """Create a tag and return a tag"""
    new_tag = Tag(name, description)
    db.session.add(new_tag)
    db.session.commit()
    return new_tag


# endregion


# region GET
def fetch_all_tags() -> list[Tag]:
    """Fetch all tag and return a list of tags"""
    return Tag.query.all()


def fetch_tag_by_id(tag_id: int) -> None | Tag:
    """Fetch a tag by his id, return None or a tag"""
    tag = Tag.query.filter_by(id=tag_id)
    if not tag:
        return None
    return tag


# endregion


# region UPDATE
def patch_tag(tag_id: int, name: str | None, description: str | None) -> None | Tag:
    """Fetch a tag by his id, then patch it, if data is provided if not found"""
    new_tag = fetch_tag_by_id(tag_id)
    if not new_tag:
        return None
    if name:
        new_tag.name = name
    if description:
        new_tag.description = description
    db.session.commit()
    return new_tag


# endregion


# region DELETE
def delete_tag(tag_id: int) -> bool:
    """Fetch a tag by his id, then delete it if exist else send back False"""
    tag = fetch_tag_by_id(tag_id)
    if not tag:
        return False
    db.session.delete(tag)
    db.session.commit()
    return True


# endregion

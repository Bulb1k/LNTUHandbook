from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_chat(db: Session, chat_id: int):
    return db.query(models.User).filter(models.User.chat_id == chat_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_stats(db: Session):
    return {
        "total": db.query(models.User).count(),
        "facultatives": db.query(models.User.facultative).distinct().count(),
        "courses": db.query(models.User.course).distinct().count(),
        "groups": db.query(models.User.group).distinct().count(),
    }


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        chat_id=user.chat_id,
        facultative=user.facultative,
        course=user.course,
        group=user.group,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_chat_ids_by_filters(
    db: Session, facultative: str | None = None, course: str | None = None, group: str | None = None
) -> list[int]:
    query = db.query(models.User.chat_id)
    if facultative:
        query = query.filter(models.User.facultative == facultative)
    if course:
        query = query.filter(models.User.course == course)
    if group:
        query = query.filter(models.User.group == group)
    return [row[0] for row in query.all()]

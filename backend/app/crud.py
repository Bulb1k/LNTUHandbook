from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_telegram(db: Session, telegram_id: int):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()


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
        telegram_id=user.telegram_id,
        username=user.username,
        full_name=user.full_name,
        facultative=user.facultative,
        course=user.course,
        group=user.group,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

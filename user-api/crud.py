from sqlalchemy import asc


def get_users(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(UserModel).order_by(asc(UserModel.username))  # Sort in ascending order

    # Apply pagination
    users = query.offset(skip).limit(limit).all()
    return users


def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def create_user(db: Session, username: str, email: str, password: str, role: str = "user"):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db_user = UserModel(
        username=username,
        email=email,
        password=hashed_password.decode('utf-8'),
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, username: str, email: str, password: str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        user.username = username
        user.email = email
        user.password = hashed_password.decode('utf-8')
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


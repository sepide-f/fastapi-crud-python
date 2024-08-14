from auth import verify_password, hash_password,create_access_token,get_current_user_role

# start FastAPI app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/adduser", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return create_user(db, user.username, user.email, user.password, user.role)
    db_user = create_user(db, user.username, user.email, user.password, user.role)
    return db_user


@app.put("/updateuser/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    db_user = update_user(db, user_id, user.username, user.email, user.password)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/deleteuser/{user_id}", response_model=UserResponse)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    db_user = delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users", response_model=List[UserResponse])
def read_users(
        skip: int = Query(0, ge=0),  # Pagination: starting point
        limit: int = Query(10, le=100),  # Pagination: number of records to return
        db: Session = Depends(get_db)
):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/login")
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


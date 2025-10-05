from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from jose import JWTError, jwt
from datetime import datetime, timedelta
import random
import os

# ================= Database =================
DATABASE_URL = "sqlite:///./miloner_game.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ================= JWT ======================
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ================= Models ==================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    score = Column(Integer, default=0)
    scores = relationship("ScoreBord", back_populates="user")

class ScoreBord(Base):
    __tablename__ = "scorebord"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, default=0)
    user = relationship("User", back_populates="scores")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    options = Column(String) 
    correct_answer = Column(String)

# ================= Create Tables =============
Base.metadata.create_all(bind=engine)

# ================= Pydantic Schemas ==========
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

class UserResponse(BaseModel):
    id: int
    username: str
    score: int
    class Config:
        from_attributes = True 

class QuestionCreate(BaseModel):
    question: str
    options: list[str]

class QuestionOutput(BaseModel):
    question: str
    options: list[str]

class Token(BaseModel):
    access_token: str
    token_type: str

class Score(BaseModel):
    username: str
    score: int

# ================= Dependencies =============
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

# ================= FastAPI App ==============
app = FastAPI()


def read_file(db: Session, f_name: str):
    if not os.path.exists(f_name):
        return
    with open(f_name, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            q_text, answers_str = line.split("?", 1)
            q_text = q_text.strip() + "?"
            options = [el.strip() for el in answers_str.split(",") if el.strip()]
            if len(options) < 2:
                continue
            exists = db.query(Question).filter(Question.text == q_text).first()
            if exists:
                continue
            correct_answer = options[0]
            all_options = ",".join(options)
            new_q = Question(text=q_text, correct_answer=correct_answer, options=all_options)
            db.add(new_q)
        db.commit()

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    read_file(db, "questions.txt")
    db.close()

# ================= Register/Login Endpoints ===
@app.post("/register/", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

# ================= Game Endpoints =============
@app.get("/game", response_model=list[QuestionOutput])
def game_start(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    questions = db.query(Question).all()
    selected = random.sample(questions, min(10, len(questions)))
    result = []
    for q in selected:
        opts = q.options.split(",")
        random.shuffle(opts)
        result.append({"question": q.text, "options": opts})
    return result

@app.post("/answer/")
def answer(answer: dict[int, int], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    score = 0
    for q_id, ans_id in answer.items():
        q = db.query(Question).filter(Question.id == q_id).first()
        if not q:
            continue
        opts = q.options.split(",")
        if 0 <= ans_id < len(opts) and opts[ans_id] == q.correct_answer:
            score += 1
   
    sb = db.query(ScoreBord).filter(ScoreBord.user_id == current_user.id).first()
    if not sb:
        sb = ScoreBord(user_id=current_user.id, score=0)
        db.add(sb)
    sb.score += score
    current_user.score += score
    db.commit()
    return {"score": score, "total": len(answer)}

@app.post("/questions/")
def add_question(q: QuestionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    correct = q.options[0]
    all_opts = ",".join(q.options)
    new_q = Question(text=q.question, correct_answer=correct, options=all_opts)
    db.add(new_q)
    db.commit()
    db.refresh(new_q)
    return {"message": "Question added", "id": new_q.id}

@app.get("/top/", response_model=list[Score])
def get_top(db: Session = Depends(get_db)):
    results = db.query(ScoreBord).join(User).order_by(ScoreBord.score.desc()).limit(10).all()
    return [{"username": r.user.username, "score": r.score} for r in results]

@app.get("/users/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
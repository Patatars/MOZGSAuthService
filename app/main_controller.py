from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
from app.schemas.token import Token
from app.schemas.user import UserCreateRequest, UserAuthRequest, UserInfoResponse, UserTokenResponse
from app.core.security import get_password_hash, verify_password
from app.core.jwt import create_token, decode_token
from app.database.models import User
from app.database.session import get_db
from http import HTTPStatus

router = APIRouter()

@router.post("/register")
def register(user: UserCreateRequest, db: Session = Depends(get_db)):
    """
    Регистрирует нового пользователя.

    - **username**: Имя пользователя (уникальное, от 3 до 50 символов)
    - **tg_user_id**: Идентификатор пользователя в Telegram (опционально)
    - **password**: Пароль (от 3 до 60 символов)
    - **phone**: Номер телефона (опционально)

    Возвращает HTTP статус 200 при успешной регистрации.
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="User already exists")
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        tg_user_id=user.tg_user_id,
        phone=user.phone,
        password=hashed_password,
        role_id=1
    )
    db.add(new_user)
    db.commit()
    return HTTPStatus.OK

@router.post("/login", response_model=UserTokenResponse)
def login(user_auth: UserAuthRequest, db: Session = Depends(get_db)):
    """
    Аутентифицирует пользователя и возвращает токен доступа.

    - **username**: Имя пользователя или tg id
    - **password**: Пароль

    Возвращает токен доступа при успешной аутентификации.
    """
    user = db.query(User).filter(User.username == user_auth.username).first()
    if not user or not verify_password(user_auth.password, user.password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid username or password")
    access_token = create_token(Token(id=user.id, role=user.role_id))
    return access_token

@router.get("/me", response_model=UserInfoResponse)
def read_users_me(token: Token = Depends(decode_token), db: Session = Depends(get_db)):
    """
    Возвращает информацию о текущем пользователе.

    - **token**: Токен доступа

    Возвращает информацию о пользователе, включая id, tg_user_id, username, phone и role_id.
    """
    user = db.query(User).filter(User.id == int(token.id)).first()
    return UserInfoResponse.model_validate(user, from_attributes=True)

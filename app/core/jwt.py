from http import HTTPStatus
from typing import Annotated

import jwt
from fastapi import HTTPException, Depends

from ..main_controller import oauth2_scheme
from ..schemas.token import Token
from ..сonfig import settings


def create_token(data: Token) -> str:
    return jwt.encode(data.model_dump(), settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Token:
    try:
        payload: dict = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return Token.model_validate(payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        print(e)
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")

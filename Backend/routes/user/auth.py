from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from Backend.core.database import get_db
from Backend.env_helper import env
from Backend.crud.user.crud_user import user_crud
from Backend.core.security import create_access_token, SECRET_KEY, ALGORITHM
from Backend.schemas.user.user_schema import UserRegister, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=UserResponse)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    hashed_password = user_crud.hash_password(user.hashed_pw)
    user.hashed_pw = hashed_password
    return user_crud.create(db, user)


@router.post("/login")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    verify_user = user_crud.get_by_email(db, form_data.username)

    if not verify_user or not user_crud.verify_password(form_data.password, verify_user.hashed_pw):
        raise HTTPException(
            status_code=400,
            detail="Falsche E-Mail oder falsches Passwort."
        )

    access_token = create_access_token(verify_user)
    cookie_secure = (env("COOKIE_SECURE", "false") or "false").lower() == "true"
    cookie_samesite = env("COOKIE_SAMESITE", "lax") or "lax"

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=cookie_secure,
        samesite=cookie_samesite,
        max_age=60 * 30,
        expires=60 * 30,
        path="/"
    )

    return {"message": "Login erfolgreich"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/"
    )
    return {"message": "Logout erfolgreich"}


@router.get("/verify-token")
def verify_token(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token fehlt"
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "exp": payload.get("exp"), "role": payload.get("role")}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid or expired",
        )

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from Backend.core.security import oauth2_scheme
from Backend.crud.base import CRUDBase
from Backend.model.user.user_model import User
from Backend.schemas.user.user_schema import UserRegister, UserUpdate
from sqlalchemy.orm import Session

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = "Pcb#o£v3,al(7]OW[5E]6)jI&j()bDy."
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class CRUDUser(CRUDBase[User, UserRegister, UserUpdate]):
    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(
            self,
            plain_password: str,
            hashed_password: str
    ) -> bool:
        return pwd_context.verify(
            plain_password,
            hashed_password
        )

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            role: str = payload.get("role")
            last_name: str = payload.get("last_name")
            first_name: str = payload.get("first_name")
            display_name: str = payload.get("display_name")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return {
                "id": int(user_id),
                "role": role,
                "display_name": display_name,
                "last_name": last_name,
                "first_name": first_name,
            }
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")


user_crud = CRUDUser(User)

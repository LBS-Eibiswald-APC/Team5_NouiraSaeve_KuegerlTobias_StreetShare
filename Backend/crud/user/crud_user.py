from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from Backend.crud.base import CRUDBase
from Backend.model.user.user_model import User
from Backend.schemas.user.user_schema import UserRegister, UserUpdate
from sqlalchemy.orm import Session

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



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

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


user_crud = CRUDUser(User)

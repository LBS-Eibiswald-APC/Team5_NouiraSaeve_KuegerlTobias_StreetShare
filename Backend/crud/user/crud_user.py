from crud.base import CRUDBase
from model.user.user_model import User
from schemas.user.user_schema import UserCreate, UserUpdate
from sqlalchemy.orm import Session

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

user_crud = CRUDUser(User)
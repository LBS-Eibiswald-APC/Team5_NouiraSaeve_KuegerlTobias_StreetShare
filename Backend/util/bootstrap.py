from sqlalchemy import inspect, text

from Backend.core.database import SessionLocal, engine
from Backend.crud.user.crud_user import user_crud
from Backend.env_helper import env
from Backend.model.role.role_model import Role
from Backend.model.user.user_model import User


def ensure_schema_updates():
    inspector = inspect(engine)
    transaction_columns = [column["name"] for column in inspector.get_columns("transactions")]
    request_columns = [column["name"] for column in inspector.get_columns("requests")]

    if "request_id" not in transaction_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE transactions ADD COLUMN request_id INTEGER NULL"))

    transaction_column_updates = {
        "status": "ALTER TABLE transactions ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'Bezahlt'",
        "original_tool_condition": "ALTER TABLE transactions ADD COLUMN original_tool_condition VARCHAR(100) NULL",
        "lender_return_condition": "ALTER TABLE transactions ADD COLUMN lender_return_condition VARCHAR(100) NULL",
        "borrower_return_condition": "ALTER TABLE transactions ADD COLUMN borrower_return_condition VARCHAR(100) NULL",
        "final_condition": "ALTER TABLE transactions ADD COLUMN final_condition VARCHAR(100) NULL",
        "return_requested_at": "ALTER TABLE transactions ADD COLUMN return_requested_at DATETIME NULL",
        "return_confirmed_at": "ALTER TABLE transactions ADD COLUMN return_confirmed_at DATETIME NULL",
        "platform_fee": "ALTER TABLE transactions ADD COLUMN platform_fee DECIMAL(10, 2) NULL",
        "lender_payout": "ALTER TABLE transactions ADD COLUMN lender_payout DECIMAL(10, 2) NULL",
        "borrower_refund": "ALTER TABLE transactions ADD COLUMN borrower_refund DECIMAL(10, 2) NULL",
    }

    for column_name, sql in transaction_column_updates.items():
        if column_name not in transaction_columns:
            with engine.begin() as connection:
                connection.execute(text(sql))

    transaction_blob_columns = {"picture_before", "picture_after"}
    existing_transaction_columns = {column["name"] for column in inspector.get_columns("transactions")}

    if transaction_blob_columns.issubset(existing_transaction_columns):
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE transactions MODIFY picture_before MEDIUMBLOB NULL"))
            connection.execute(text("ALTER TABLE transactions MODIFY picture_after MEDIUMBLOB NULL"))

    if "transaction_reviews" not in inspector.get_table_names():
        with engine.begin() as connection:
            connection.execute(text("""
                CREATE TABLE transaction_reviews (
                    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    transaction_id INTEGER NOT NULL UNIQUE,
                    borrower_id INTEGER NULL,
                    lender_id INTEGER NULL,
                    borrower_condition VARCHAR(100) NULL,
                    lender_condition VARCHAR(100) NULL,
                    lender_picture MEDIUMBLOB NULL,
                    review_status VARCHAR(50) NOT NULL DEFAULT 'Offen',
                    support_decision_condition VARCHAR(100) NULL,
                    support_note TEXT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    resolved_at DATETIME NULL,
                    resolved_by INTEGER NULL,
                    CONSTRAINT fk_transaction_reviews_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
                    CONSTRAINT fk_transaction_reviews_borrower FOREIGN KEY (borrower_id) REFERENCES users(id) ON DELETE SET NULL,
                    CONSTRAINT fk_transaction_reviews_lender FOREIGN KEY (lender_id) REFERENCES users(id) ON DELETE SET NULL,
                    CONSTRAINT fk_transaction_reviews_resolved_by FOREIGN KEY (resolved_by) REFERENCES users(id) ON DELETE SET NULL
                )
            """))


def seed_roles_and_admin():
    db = SessionLocal()

    try:
        admin_role = db.query(Role).filter(Role.name == "Admin").first()
        if not admin_role:
            admin_role = Role(name="Admin")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)

        user_role = db.query(Role).filter(Role.name == "User").first()
        if not user_role:
            user_role = Role(name="User")
            db.add(user_role)
            db.commit()
            db.refresh(user_role)

        admin_email = env("ADMIN_EMAIL", "admin@streetshare.local")
        admin_display_name = env("ADMIN_DISPLAY_NAME", "admin")
        admin_password = env("ADMIN_PASSWORD", "admin123")

        admin_user = db.query(User).filter(
            (User.email == admin_email) | (User.display_name == admin_display_name)
        ).first()

        if not admin_user:
            admin_user = User(
                first_name=env("ADMIN_FIRST_NAME", "Tobias"),
                last_name=env("ADMIN_LAST_NAME", "Kuegerl"),
                display_name=admin_display_name,
                hashed_pw=user_crud.hash_password(admin_password),
                email=admin_email,
                phone=env("ADMIN_PHONE", "+436601333780"),
                street=env("ADMIN_STREET", "Klunkeraberg"),
                house_nr=env("ADMIN_HOUSE_NR", "7"),
                zip=env("ADMIN_ZIP", "8530"),
                city=env("ADMIN_CITY", "Deutschlandsberg"),
                country=env("ADMIN_COUNTRY", "Oesterreich"),
                role_id=admin_role.id,
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
        else:
            changed = False

            if admin_user.role_id != admin_role.id:
                admin_user.role_id = admin_role.id
                changed = True

            if admin_email and admin_user.email != admin_email:
                admin_user.email = admin_email
                changed = True

            if admin_display_name and admin_user.display_name != admin_display_name:
                admin_user.display_name = admin_display_name
                changed = True

            if changed:
                db.add(admin_user)
                db.commit()
                db.refresh(admin_user)
    finally:
        db.close()

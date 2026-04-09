import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.core.database import Base, engine
from Backend.routes.user.user_routes import router as user_router
from Backend.routes.role.role_routes import router as role_router
from Backend.routes.tool.tool_routes import router as tool_routes
from Backend.routes.chats.conversation import router as conversation_routes
from Backend.routes.chats.messages import router as messages_routes
from Backend.routes.user.auth import router as auth_router
from Backend.routes.requests.requests_routes import router as request_routes
from Backend.routes.transactions.transaction_routes import router as transaction_routes
from Backend.routes.transactions.transaction_review_routes import router as transaction_review_routes
from Backend.util.bootstrap import ensure_schema_updates, seed_roles_and_admin

Base.metadata.create_all(bind=engine)


ensure_schema_updates()
seed_roles_and_admin()

app = FastAPI(
    title="StreetShare API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://streetshare.online",
        "https://www.streetshare.online",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(role_router)
app.include_router(tool_routes)
app.include_router(request_routes)
app.include_router(conversation_routes)
app.include_router(messages_routes)

app.include_router(auth_router)

app.include_router(transaction_routes)
app.include_router(transaction_review_routes)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

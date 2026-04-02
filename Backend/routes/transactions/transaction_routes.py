from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from Backend.core.database import get_db
from Backend.core.dependencies import is_admin, require_role
from Backend.crud.requests.crud_requests import requests_crud
from Backend.crud.tool.crud_tool import tool_crud
from Backend.crud.transactions.crud_transactions import transaction_crud
from Backend.crud.user.crud_user import user_crud
from Backend.model.user.user_model import User
from Backend.schemas.transactions.transaction_schema import TransactionCreate, TransactionResponse
from Backend.util.image_uploads import normalize_uploaded_image


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

def build_transaction_response(db: Session, transaction):
    tool = tool_crud.get(db, transaction.tool_id)
    borrower = user_crud.get(db, transaction.borrower_id)
    lender = user_crud.get(db, transaction.lender_id)

    return {
        "id": transaction.id,
        "tool_id": transaction.tool_id,
        "request_id": transaction.request_id,
        "tool_name": tool.name if tool else None,
        "borrower_id": transaction.borrower_id,
        "borrower_name": borrower.display_name if borrower else None,
        "lender_id": transaction.lender_id,
        "lender_name": lender.display_name if lender else None,
        "start_date": transaction.start_date,
        "end_date": transaction.end_date,
        "created_at": transaction.created_at,
        "has_picture_before": transaction.picture_before is not None,
        "has_picture_after": transaction.picture_after is not None,
        "status": transaction.status,
        "original_tool_condition": transaction.original_tool_condition,
        "lender_return_condition": transaction.lender_return_condition,
        "borrower_return_condition": transaction.borrower_return_condition,
        "final_condition": transaction.final_condition,
        "return_requested_at": transaction.return_requested_at,
        "return_confirmed_at": transaction.return_confirmed_at,
        "platform_fee": float(transaction.platform_fee) if transaction.platform_fee is not None else None,
        "lender_payout": float(transaction.lender_payout) if transaction.lender_payout is not None else None,
        "borrower_refund": float(transaction.borrower_refund) if transaction.borrower_refund is not None else None,
    }


@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    tool = tool_crud.get(db, transaction.tool_id)

    if not tool:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Tool not found")

    if transaction.lender_id != tool.created_by:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid lender for tool")

    if current_user.id not in [transaction.borrower_id, transaction.lender_id] and not is_admin(current_user):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Sie sind nicht erlaubt dies zu tun.")

    if transaction.original_tool_condition is None:
        transaction = transaction.model_copy(update={"original_tool_condition": tool.tool_condition})

    return transaction_crud.create(db, transaction)


@router.post("/pay-request/{request_id}", response_model=TransactionResponse)
def pay_request_transaction(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    request = requests_crud.get(db, request_id)

    if not request:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Request not found")

    if request.borrower_id != current_user.id and not is_admin(current_user):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Sie sind nicht erlaubt dies zu tun.")

    if request.status != "Akzeptiert":
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Diese Anfrage kann aktuell nicht bezahlt werden.")

    existing_transaction = transaction_crud.get_by_request_id(db, request_id)
    if existing_transaction:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Für diese Anfrage existiert bereits eine Transaktion.")

    tool = tool_crud.get(db, request.tool_id)

    transaction = transaction_crud.create(db, TransactionCreate(
        tool_id=request.tool_id,
        request_id=request.id,
        borrower_id=request.borrower_id,
        lender_id=request.lender_id,
        start_date=request.start_date,
        end_date=request.end_date,
        created_at=request.created_at,
        picture_before=None,
        picture_after=None,
        original_tool_condition=tool.tool_condition if tool else None,
    ))

    requests_crud.update(
        db,
        db_obj=request,
        obj_in={"status": "Bezahlt"}
    )

    transaction = transaction_crud.update(
        db,
        db_obj=transaction,
        obj_in={"status": "Bezahlt"}
    )

    return build_transaction_response(db, transaction)


@router.post("/{transaction_id}/return-request", response_model=TransactionResponse)
def request_return(
    transaction_id: int,
    return_condition: str | None = Form(None),
    borrower_return_condition: str | None = Form(None),
    lender_return_condition: str | None = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    transaction = transaction_crud.get(db, transaction_id)

    if not transaction:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Transaction not found")

    if transaction.borrower_id != current_user.id and not is_admin(current_user):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Sie sind nicht erlaubt dies zu tun.")

    if transaction.status != "Bezahlt":
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Rückgabe kann aktuell nicht erfasst werden.")

    submitted_condition = return_condition or borrower_return_condition or lender_return_condition
    if not submitted_condition:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Bitte eine Kondition angeben.")

    actual_return_time = datetime.utcnow()

    transaction = transaction_crud.update(
        db,
        db_obj=transaction,
        obj_in={
            "status": "Rueckgabe ausstehend",
            "borrower_return_condition": submitted_condition,
            "return_requested_at": actual_return_time,
            "end_date": actual_return_time,
        }
    )

    return build_transaction_response(db, transaction)


@router.post("/{transaction_id}/confirm-return", response_model=TransactionResponse)
async def confirm_return(
    transaction_id: int,
    final_condition: str | None = Form(None),
    lender_return_condition: str | None = Form(None),
    borrower_return_condition: str | None = Form(None),
    picture_after: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    transaction = transaction_crud.get(db, transaction_id)

    if not transaction:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Transaction not found")

    if transaction.lender_id != current_user.id and not is_admin(current_user):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Sie sind nicht erlaubt dies zu tun.")

    if transaction.status != "Rueckgabe ausstehend":
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Rückgabe kann aktuell nicht bestätigt werden.")

    submitted_condition = final_condition or lender_return_condition or borrower_return_condition
    if not submitted_condition:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Bitte eine finale Kondition angeben.")

    if (
        transaction.borrower_return_condition
        and transaction.borrower_return_condition != submitted_condition
    ):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Leiher und Verleiher haben unterschiedliche Konditionen angegeben. Bitte an den Support weitergeben."
        )

    photo_bytes = await normalize_uploaded_image(picture_after)

    tool = tool_crud.get(db, transaction.tool_id)
    platform_fee, lender_payout, borrower_refund = transaction_crud.calculate_return_distribution(
        tool.deposit if tool else 0,
        transaction.original_tool_condition or (tool.tool_condition if tool else None),
        submitted_condition,
    )

    transaction = transaction_crud.update(
        db,
        db_obj=transaction,
        obj_in={
            "status": "Abgeschlossen",
            "lender_return_condition": submitted_condition,
            "final_condition": submitted_condition,
            "picture_after": photo_bytes,
            "return_confirmed_at": datetime.utcnow(),
            "platform_fee": platform_fee,
            "lender_payout": lender_payout,
            "borrower_refund": borrower_refund,
            "end_date": transaction.end_date or datetime.utcnow(),
        }
    )

    return build_transaction_response(db, transaction)


@router.get("/", response_model=List[TransactionResponse])
def get_tools(
    db: Session = Depends(get_db),
    user=Depends(require_role(["Admin"]))
):
    return transaction_crud.get_all(db)


@router.get("/me", response_model=List[TransactionResponse])
def get_my_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    return transaction_crud.get_user_transactions(db, current_user.id)


@router.get("/tool/{tool_id}", response_model=List[TransactionResponse])
def get_tool(
    tool_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    tool = tool_crud.get(db, tool_id)

    if not tool:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Tool not found")

    transactions = transaction_crud.get_all_tools(db, tool_id)
    is_participant = any(
        current_user.id in [transaction["borrower_id"], transaction["lender_id"]]
        for transaction in transactions
    )

    if tool.created_by != current_user.id and not is_participant and not is_admin(current_user):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Sie sind nicht erlaubt dies zu tun.")

    return transactions


@router.delete("/{transaction_id}")
def delete_tool(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_crud.get_current_user),
):
    transaction = transaction_crud.get(db, transaction_id)

    if not transaction:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Transaction not found")

    if current_user.id not in [transaction.borrower_id, transaction.lender_id] and not is_admin(current_user):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Sie sind nicht erlaubt dies zu tun.")

    deleted_transaction = transaction_crud.delete(db, transaction_id)

    if not deleted_transaction:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Transaction not found")

    return {"message": "Transaction deleted"}

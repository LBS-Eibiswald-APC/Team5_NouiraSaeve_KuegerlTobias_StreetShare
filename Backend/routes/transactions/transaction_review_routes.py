from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from Backend.core.database import get_db
from Backend.core.dependencies import is_admin, require_role
from Backend.crud.tool.crud_tool import tool_crud
from Backend.crud.transaction_reviews.crud_transaction_reviews import transaction_review_crud
from Backend.crud.transactions.crud_transactions import transaction_crud
from Backend.crud.user.crud_user import user_crud
from Backend.routes.transactions.transaction_routes import calculate_return_distribution
from Backend.schemas.transaction_reviews.transaction_reviews_schema import TransactionReviewCreate, TransactionReviewResponse
from Backend.util.image_uploads import normalize_uploaded_image


router = APIRouter(
    prefix="/transaction-reviews",
    tags=["transaction-reviews"]
)


@router.post("/{transaction_id}", response_model=TransactionReviewResponse)
async def create_review(
    transaction_id: int,
    lender_condition: str = Form(...),
    lender_picture: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(user_crud.get_current_user),
):
    transaction = transaction_crud.get(db, transaction_id)

    if not transaction:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Transaction not found")

    if transaction.lender_id != current_user.id and not is_admin(current_user):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Sie sind nicht erlaubt dies zu tun.")

    if transaction.status != "Rueckgabe ausstehend":
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Dieser Fall kann aktuell nicht an den Support gegeben werden.")

    existing_review = transaction_review_crud.get_by_transaction_id(db, transaction_id)
    if existing_review:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Für diese Transaktion existiert bereits ein Support-Fall.")

    picture_bytes = await normalize_uploaded_image(lender_picture)

    review = transaction_review_crud.create(db, TransactionReviewCreate(
        transaction_id=transaction.id,
        borrower_id=transaction.borrower_id,
        lender_id=transaction.lender_id,
        borrower_condition=transaction.borrower_return_condition,
        lender_condition=lender_condition,
        lender_picture=picture_bytes,
    ))

    transaction_crud.update(
        db,
        db_obj=transaction,
        obj_in={
            "status": "In Review",
            "lender_return_condition": lender_condition,
        }
    )

    rows = transaction_review_crud.get_all_with_details(db)
    review_row = [row for row in rows if row[0].id == review.id]
    return transaction_review_crud.build_review_response(review_row)[0]


@router.get("/", response_model=List[TransactionReviewResponse])
def get_reviews(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["Admin"]))
):
    rows = transaction_review_crud.get_all_with_details(db)
    return transaction_review_crud.build_review_response(rows)


@router.get("/{review_id}/picture")
def get_review_picture(
    review_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["Admin"]))
):
    review = transaction_review_crud.get(db, review_id)
    if not review:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Support-Fall nicht gefunden.")

    if not review.lender_picture:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Support-Foto nicht gefunden.")

    return Response(content=review.lender_picture, media_type="image/jpeg")


@router.post("/{review_id}/resolve", response_model=TransactionReviewResponse)
def resolve_review(
    review_id: int,
    final_condition: str = Form(...),
    support_note: str | None = Form(None),
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["Admin"]))
):
    review = transaction_review_crud.get(db, review_id)
    if not review:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Support-Fall nicht gefunden.")

    transaction = transaction_crud.get(db, review.transaction_id)
    if not transaction:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Transaction not found")

    tool = tool_crud.get(db, transaction.tool_id)
    platform_fee, lender_payout, borrower_refund = calculate_return_distribution(
        tool.deposit if tool else 0,
        tool.tool_condition if tool else None,
        final_condition,
    )

    transaction_crud.update(
        db,
        db_obj=transaction,
        obj_in={
            "status": "Abgeschlossen",
            "final_condition": final_condition,
            "return_confirmed_at": datetime.utcnow(),
            "platform_fee": platform_fee,
            "lender_payout": lender_payout,
            "borrower_refund": borrower_refund,
        }
    )

    transaction_review_crud.update(
        db,
        db_obj=review,
        obj_in={
            "review_status": "Entschieden",
            "support_decision_condition": final_condition,
            "support_note": support_note,
            "resolved_at": datetime.utcnow(),
            "resolved_by": current_user.id,
        }
    )

    rows = transaction_review_crud.get_all_with_details(db)
    review_row = [row for row in rows if row[0].id == review.id]
    return transaction_review_crud.build_review_response(review_row)[0]

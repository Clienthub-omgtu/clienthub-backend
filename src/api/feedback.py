import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.connection import get_session
from src.db.models import User
from src.schemas import (
    FeedBacksByPhoneNumber,
    ReadFeedBackAboutClient,
    AddFeedbackSuccess,
    CreateFeedBackAboutClient,
)

from src.utils.user import get_current_user
from src.utils.feedback import feedbacks_by_phone_number, add_feedback_about_client
from src.utils.legal_entity import get_legal_entity


api_router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


@api_router.post(
    "/get_feedbacks_by_phone_number",
    status_code=status.HTTP_200_OK,
    response_model=list[ReadFeedBackAboutClient],
    responses={status.HTTP_200_OK: {"description": "success"}},
)
async def get_feedbacks_by_phone_number(
    _: Request,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    data: FeedBacksByPhoneNumber = Body(...),
):
    legal_entity_by_curr_user = await get_legal_entity(
        session=session, legal_entity_id=str(current_user.legal_entity_id)
    )
    subscription = legal_entity_by_curr_user.subscription_expiration_date
    if current_user and subscription and subscription >= datetime.datetime.now():
        feedbacks = await feedbacks_by_phone_number(
            session=session, phone_number=data.phone_number
        )
        if not feedbacks:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return feedbacks
    if current_user and (not subscription or subscription < datetime.datetime.now()):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"description": "subscription is expired"},
        )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@api_router.post(
    "/create_feedback_about_client",
    status_code=status.HTTP_200_OK,
    response_model=AddFeedbackSuccess,
    responses={status.HTTP_200_OK: {"description": "success"}},
)
async def create_feedback_about_client(
    _: Request,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    data: CreateFeedBackAboutClient = Body(...),
):
    legal_entity_by_curr_user = await get_legal_entity(
        session=session, legal_entity_id=str(current_user.legal_entity_id)
    )
    subscription = legal_entity_by_curr_user.subscription_expiration_date
    if current_user and subscription and subscription >= datetime.datetime.now():
        is_success = await add_feedback_about_client(
            session=session, data=data, legal_entity_id=current_user.legal_entity_id
        )
        if is_success:
            return {"message": "success"}

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if current_user and (not subscription or subscription < datetime.datetime.now()):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"description": "Subscription is expired"},
        )

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

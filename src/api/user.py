from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.config import get_settings
from src.db.connection import get_session
from src.db.models import User
from src.schemas import (
    UserRegistration,
    RegistrationSuccess,
    Token,
    UserRead,
    UserUpdate,
    UserUpdatedSuccess,
)

from src.utils.user import (
    authenticate_user,
    create_access_token,
    get_current_user,
    register_user,
    update_user,
    delete_user,
)


api_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@api_router.post(
    "/authentication",
    status_code=status.HTTP_200_OK,
    response_model=Token,
)
async def authentication(
    _: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@api_router.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
    response_model=RegistrationSuccess,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad parameters for registration",
        },
    },
)
async def registration(
    _: Request,
    registration_form: UserRegistration = Body(...),
    session: AsyncSession = Depends(get_session),
):
    is_success, message, email = await register_user(session, registration_form)
    if is_success:
        access_token_expires = timedelta(
            minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            data={"sub": email}, expires_delta=access_token_expires
        )
        return {"message": message, "access_token": access_token}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )


@api_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def get_me(
    _: Request,
    current_user: User = Depends(get_current_user),
):
    return UserRead.from_orm(current_user)


@api_router.post(
    "/update_inf", status_code=status.HTTP_200_OK, response_model=UserUpdatedSuccess
)
async def update_inf_user(
    _: Request,
    current_user: User = Depends(get_current_user),
    data_for_update: UserUpdate = Body(...),
    session: AsyncSession = Depends(get_session),
):
    is_success = await update_user(
        session=session, data=data_for_update, curr_user=current_user
    )
    if is_success:
        return {"message": "success"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@api_router.delete(
    "/takeout",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def takeout(
    _: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await delete_user(session, current_user)

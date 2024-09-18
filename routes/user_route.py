from fastapi import APIRouter, Request
from controllers.user_controller import UserController
from interfaces.create_user import CreateUser
from interfaces.user_login import UserLogin
from interfaces.update_user import UpdateUser
from interfaces.update_password_user import UpdatePassword


router = APIRouter()

user_controller = UserController()


@router.post("/add-user")
async def create_user(request: Request, user: CreateUser):
    return await user_controller.create_user(request, user)

@router.post("/login")
async def login_user(request: Request, user: UserLogin):
    print(f'Login user in router')
    return await user_controller.login_user(request, user)


@router.get("/get-user/{id}")
async def get_user_by_id(request: Request, id: str):
    return await user_controller.get_user_by_id(request, id)


@router.get("/get-users")
async def get_users(request: Request):
    return await user_controller.get_users(request)


@router.put("/update-user/{id}")
async def update_user(request: Request, id: str, user: UpdateUser):
    return await user_controller.update_user(request, id, user)


@router.patch("/update-password/")
async def update_password(request: Request, user: UpdatePassword):
    return await user_controller.update_password(request, user)


@router.delete("/user/{id}")
async def delete_user(request: Request, id: str):
    return await user_controller.delete_user(request, id)
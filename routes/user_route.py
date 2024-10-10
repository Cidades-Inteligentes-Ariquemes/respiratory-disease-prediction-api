from fastapi import APIRouter, Request
from controllers.user_controller import UserController
from interfaces.create_user import CreateUser
from interfaces.user_login import UserLogin
from interfaces.update_user import UpdateUser
from interfaces.update_password_user import UpdatePassword
from interfaces.create_feedback_user import CreateFeedbackUser
from interfaces.update_password_user_common import UpdatePasswordUserCommon
from interfaces.forgot_update_password_model import ForgotUpadatePassword
from interfaces.code_verification_model import CodeVerification
from interfaces.id_verification_model import IdVerification
from utils.examples_routes_returns import ResponseExamples


router = APIRouter()

user_controller = UserController()

response_examples = ResponseExamples()  


@router.post("/user", responses = response_examples.create_user())
async def create_user(request: Request, user: CreateUser):
    return await user_controller.create_user(request, user)

@router.post("/login", responses = response_examples.login_user())
async def login_user(request: Request, user: UserLogin):
    return await user_controller.login_user(request, user)


@router.get("/user/{id}", responses = response_examples.get_user_by_id())
async def get_user_by_id(request: Request, id: str):
    return await user_controller.get_user_by_id(request, id)


@router.get("/users", responses = response_examples.get_users())
async def get_users(request: Request):
    return await user_controller.get_users(request)


@router.put("/user/{id}", responses = response_examples.update_user())
async def update_user(request: Request, id: str, user: UpdateUser):
    return await user_controller.update_user(request, id, user)


@router.patch("/password/", responses = response_examples.update_password())
async def update_password(request: Request, user: UpdatePassword):
    return await user_controller.update_password(request, user)


@router.patch("/password/user/common/{id}", responses = response_examples.update_password_user_common())
async def update_password_user_common(request: Request, id: str, user: UpdatePasswordUserCommon):
    return await user_controller.update_password_user_common(request, id, user)


@router.post("/send-verification-code/{email}", responses = response_examples.send_verification_code())
async def forgot_password(request: Request, email: str):
    return await user_controller.send_verification_code(request, email)


@router.post("/resend-verification-code/{email}", responses = response_examples.resend_verification_code())
async def resend_verification_code(request: Request, email: str, id_verification: IdVerification):
    return await user_controller.resend_verification_code(request, email, id_verification)


@router.post("/confirm-code-verification/{email}", responses = response_examples.confirm_code_verification())
async def code_verification(request: Request, email: str, code: CodeVerification):
    return await user_controller.confirm_code_verification(request, email, code)


@router.patch("/forgot/update-password/{user_id}", responses = response_examples.forgot_update_password())
async def forgot_update_password(request: Request, user_id: str, new_password: ForgotUpadatePassword):
    return await user_controller.forgot_update_password(request, user_id, new_password) 


@router.delete("/user/{id}", responses = response_examples.delete_user())
async def delete_user(request: Request, id: str):
    return await user_controller.delete_user(request, id)


@router.post("/feedback", responses = response_examples.create_feedback())
async def create_feedback(request: Request, feedback: CreateFeedbackUser):
    return await user_controller.create_feedback(request, feedback)


@router.get("/feedbacks", responses = response_examples.get_feedback())
async def get_feedback(request: Request):
    return await user_controller.get_feedback(request)
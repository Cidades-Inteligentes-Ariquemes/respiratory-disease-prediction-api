class ResponseExamples:

    @staticmethod
    def create_user():
        return {
            201: {
                "description": "User created successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "User added successfully",
                                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                                "status_code": 201
                            }
                        }
                    }
                }
            },
            400: {
                "description": "Bad Request - Missing field",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error adding user: {key} cannot be empty",
                                "status_code": 400
                            }
                        }
                    }
                }
            },
            403: {
                "description": "Validation Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error adding user: email is not valid",
                                "status_code": 403
                            }
                        }
                    }
                }
            },
            409: {
                "description": "Validation Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error adding user: email already exists",
                                "status_code": 409
                            }
                        }
                    }
                }
            },
            422: {
                "description": "Validation Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error adding user: profile must be Administrador or Usuario_comum",
                                "status_code": 422
                            }
                        }
                    }
                }
            },
            500: {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error adding user",
                                "status_code": 500
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def login_user():
        return {
            200: {
                "description": "User logged in successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "User logged in successfully",
                                'user_id': '123e4567-e89b-12d3-a456-426614174000',
                                'user_full_name': 'John Doe',
                                'token': 'some_jwt_token',
                                "status_code": 200
                            }
                        }
                    }
                }
            },
            400: {
                "description": "Error creating token",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error logging in user: token could not be created",
                                "status_code": 401
                            }
                        }
                    }
                }
            },
            401: {
                "description": "Unauthorized - Incorrect password",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error logging in user: password is incorrect",
                                "status_code": 401
                            }
                        }
                    }
                }
            },
            404: {
                "description": "User not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error logging in user: user not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            },
        }

    @staticmethod
    def get_user_by_id():
        return {
            200: {
                "description": "User found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "User found",
                                "user": {
                                    "id": "123e4567-e89b-12d3-a456-426614174000",
                                    "full_name": "John Doe",
                                    "email": "john.doe@example.com",
                                    "profile": "Administrador"
                                },
                                "status_code": 200
                            }
                        }
                    }
                }
            },
            404: {
                "description": "User not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error getting user by id: user not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def get_users():
        return {
            200: {
                "description": "Users found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Users found",
                                "users": [
                                    {"id": "123e4567-e89b-12d3-a456-426614174000", "name": "John Doe"},
                                    {"id": "123e4567-e89b-12d3-a456-426614174001", "name": "Jane Doe"}
                                ],
                                "status_code": 200
                            }
                        }
                    }
                }
            },
            404: {
                "description": "Users not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error getting users: users not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def update_user():
        return {
            200: {
                "description": "User updated successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "User updated successfully",
                                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                                "status_code": 200
                            }
                        }
                    }
                }
            },
            400: {
                "description": "Bad Request - Missing field",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error updating user: {key} cannot be empty",
                                "status_code": 400
                            }
                        }
                    }
                }
            },
            409: {
                "description": "Email already exists",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error updating user: email already exists",
                                "status_code": 409
                            }
                        }
                    }
                }
            },
            404: {
                "description": "User not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error updating user: user not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            },
            500: {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error updating user",
                                "status_code": 500
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def update_password():
        return {
            200: {
                "description": "Password updated successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Password updated successfully",
                                "user_email": "john.doe@example.com",
                                "status_code": 200
                            }
                        }
                    }
                }
            },
            400: {
                "description": "Bad Request - Missing field",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error updating password: {key} cannot be empty",
                                "status_code": 400
                            }
                        }
                    }
                }
            },
            404: {
                "description": "User not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error updating password: user not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            },
            500: {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error updating password",
                                "status_code": 500
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def update_password_user_common():
        return {
            200: {
                "description": "Password updated successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Password updated successfully",
                                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                                "status_code": 200
                            }
                        }
                    }
                }
            },
            400: {
                "description": "Bad Request - Missing field",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error updating password: {key} cannot be empty",
                                "status_code": 400
                            }
                        }
                    }
                }
            },
            401: {
                "description": "Unauthorized - Current password incorrect",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error updating password: current password is incorrect",
                                "status_code": 401
                            }
                        }
                    }
                }
            },
            404: {
                "description": "User not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error updating password: user not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            },
            500: {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error updating password",
                                "status_code": 500
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def send_verification_code():
        return {
            200: {
                "description": "Verification code sent successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Verification code sent successfully",
                                "email": "john.doe@example.com",
                                "id_verification": "123e4567-e89b-12d3-a456-426614174000",
                                "verification_code": "123456",
                                "status_code": 200
                            }
                        }
                    }
                }
            },
            422: {
                "description": "Invalid email",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Invalid email",
                                "status_code": 422
                            }
                        }
                    }
                }
            },
            404: {
                "description": "User not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "User not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            },
            500: {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error sending verification code",
                                "status_code": 500
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def resend_verification_code():
        return {
            200: {
                "description": "New verification code sent successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "New Verification code sent successfully",
                                "email": "john.doe@example.com",
                                "id_verification": "123e4567-e89b-12d3-a456-426614174000",
                                "verification_code": "123456",
                                "status_code": 200
                            }
                        }
                    }
                }
            },
            422: {
                "description": "Invalid email",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Invalid email",
                                "status_code": 422
                            }
                        }
                    }
                }
            },
            404: {
                "description": "User not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "User not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            },
            500: {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error resending verification code",
                                "status_code": 500
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def confirm_code_verification():
        return {
            200: {
                "description": "Code verification successful",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Code verification with success",
                                "id_verification": "123e4567-e89b-12d3-a456-426614174000",
                                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                                "user_email": "john.doe@example.com",
                                "status_code": 200
                            }
                        }
                    }
                }
            },
            400: {
                "description": "Incorrect or expired code",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Code expired",
                                "status_code": 400
                            }
                        }
                    }
                }
            },
            403: {
                "description": "Invalid code",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Incorrect code",
                                "status_code": 403
                            }
                        }
                    }
                }
            },
            404: {
                "description": "User or code not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "User not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            },
            500: {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error verifying code",
                                "status_code": 500
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def forgot_update_password():
        return {
            200: {
                "description": "Password updated successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Password updated successfully",
                                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                                "status_code": 200
                            }
                        }
                    }
                }
            },
            400: {
                "description": "code not verified",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "code not verified",
                                "status_code": 400
                            }
                        }
                    }
                }
            },
            403: {
                "description": "Invalid or not verified code",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Invalid code",
                                "status_code": 403
                            }
                        }
                    }
                }
            },
            404: {
                "description": "User not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "User not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            },
            500: {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error updating password",
                                "status_code": 500
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def delete_user():
        return {
            200: {
                "description": "User deleted successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "User deleted successfully",
                                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                                "status_code": 200
                            }
                        }
                    }
                }
            },
            404: {
                "description": "User not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error deleting user: user not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            },
            500: {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error deleting user",
                                "status_code": 500
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def create_feedback():
        return {
            201: {
                "description": "Feedback added successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Feedback added successfully",
                                "feedback_id": "123e4567-e89b-12d3-a456-426614174000",
                                "status_code": 201
                            }
                        }
                    }
                }
            },
            400: {
                "description": "Bad Request - Missing field",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error adding feedback: {key} cannot be empty",
                                "status_code": 400
                            }
                        }
                    }
                }
            },
            500: {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error adding feedback",
                                "status_code": 500
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def get_feedback():
        return {
            200: {
                "description": "Feedbacks found successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Feedbacks found",
                                "feedbacks": {
                                    "covid-19": {
                                        "total_quantity": 50,
                                        "total_quantity_correct": 45
                                    },
                                    "normal": {
                                        "total_quantity": 30,
                                        "total_quantity_correct": 27
                                    }
                                },
                                "status_code": 200
                            }
                        }
                    }
                }
            },
            404: {
                "description": "Feedbacks not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "There are no saved feedbacks",
                                "status_code": 404
                            }
                        }
                    }
                }
            },
            500: {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "Error getting feedbacks: feedbacks not found",
                                "status_code": 500
                            }
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def handle_prediction():
        return {
            200: {
                "description": "Prediction made successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "prediciton": {                           
                                "covid-19": 0.95,
                                "normal": 0.05,
                                "pnemonia viral": 0.0,
                                "pnemonia bacteriana": 0.0            
                            }
                        }
                    }
                }
            },
            400: {
                "description": "Bad Request - Incorrect image format",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": {
                                "message": "An error occurred while processing the image. Please check that the image is in the correct format and try again.",
                                "status_code": 400
                            }
                        }
                    }
                }
            },
        }

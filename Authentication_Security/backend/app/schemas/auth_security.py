from pydantic import BaseModel, EmailStr, Field


class MessageResponse(BaseModel):
    message: str
    # Returned only when AUTH_DEBUG_TOKENS=true for local development/testing.
    debug_token: str | None = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class EmailVerificationRequest(BaseModel):
    token: str


class ResendVerificationRequest(BaseModel):
    email: EmailStr


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TwoFactorSetupResponse(BaseModel):
    secret: str
    otpauth_uri: str


class TwoFactorCodeRequest(BaseModel):
    code: str = Field(min_length=6, max_length=8)


class TwoFactorLoginRequest(BaseModel):
    challenge_token: str
    code: str = Field(min_length=6, max_length=8)

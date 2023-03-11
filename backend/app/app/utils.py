import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jose import jwt
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

from app.core.config import settings


class EmailSchema(BaseModel):
    email: List[EmailStr]


async def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"

    conf = ConnectionConfig(
        MAIL_USERNAME=settings.SMTP_USER,
        MAIL_PASSWORD=settings.SMTP_PASSWORD,
        MAIL_PORT=settings.SMTP_PORT,
        MAIL_SERVER=settings.SMTP_HOST,
        MAIL_SSL_TLS=settings.SMTP_TLS,
        MAIL_STARTTLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        MAIL_FROM=settings.EMAILS_FROM_EMAIL,
        TEMPLATE_FOLDER=settings.EMAIL_TEMPLATES_DIR,
    )

    message = MessageSchema(
        subject=subject_template,
        recipients=[email_to],
        template_body=environment,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name=html_template)
    response = JSONResponse(status_code=200, content={"message": "email has been sent"})

    logging.info(f"send email result: {response}")


async def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    template_str = "test_email.html"
    await send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


async def send_reset_password_email(email_to: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email_to}"
    template_str = "reset_password.html"
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    await send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


# async def send_new_account_email(email_to: str, username: str, password: str) -> None:
# TODO remove sending password in email right?
async def send_new_account_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {email_to}"
    template_str = "new_account.html"
    link = settings.SERVER_HOST
    await send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email_to,
            # TODO do we want usernames AND emails?
            "email": email_to,
            "link": link,
        },
    )

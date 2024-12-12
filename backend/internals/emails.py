from http.cookiejar import debug
from pathlib import Path

from devtools import debug
from fastapi import Depends
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List, Dict, Any, Annotated

from backend.config import Settings, get_settings


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]


def conf () -> ConnectionConfig:
    settings = get_settings()

    return ConnectionConfig(
        MAIL_USERNAME = settings.mail_username,
        MAIL_PASSWORD = settings.mail_password,
        MAIL_FROM = settings.admin_email,
        MAIL_PORT = 587,
        MAIL_SERVER = settings.mail_server,
        MAIL_STARTTLS = True,
        MAIL_SSL_TLS = False,
        TEMPLATE_FOLDER = Path(__file__).parent.parent / 'templates',

        # if no indicated SUPPRESS_SEND defaults to 0 (false) as below
        SUPPRESS_SEND=1
    )


async def send_with_template(email: EmailSchema):

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.email,
        template_body=email.body,
        subtype=MessageType.html,
        )

    fm = FastMail(conf())
    with fm.record_messages() as outbox:
        await fm.send_message(message, template_name="email_template.html")
        mail = outbox[0]
        debug(outbox)
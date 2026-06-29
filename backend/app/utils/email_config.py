from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="rutuja@gmail.com",
    MAIL_PASSWORD="abcd efgh ijkl mnop",  # Gmail App Password
    MAIL_FROM="rutuja@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)
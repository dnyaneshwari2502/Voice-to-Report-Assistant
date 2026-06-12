from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

TOKEN_FILE = "token_voice_report.json"


def send_email(recipient_email, manager_email, subject, body):

    creds = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        SCOPES
    )

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    message = MIMEText(body)

    message["to"] = recipient_email
    message["cc"] = manager_email
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw_message}
    ).execute()
import os
import smtplib
import sys
from dataclasses import dataclass
from email.message import EmailMessage

from dotenv import load_dotenv
from validate_email import validate_email

load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("PASSWORD")


@dataclass
class Email:
    first_name: str
    last_name: str
    subject: str
    to: str
    message: str

    def isValidEmail(self) -> bool:
        valid = validate_email(
            email_address=self.to,
            check_format=True,
            check_blacklist=True,
            check_smtp=True,
            smtp_from_address=EMAIL_ADDRESS
        )
        return valid

    def sendEmail(self):
        msg = EmailMessage()
        msg['Subject'] = self.subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = self.to
        msg.set_content(self.message)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, PASSWORD)
            smtp.send_message(msg)
        print("Email Sent")
        sys.exit(1)


def main():
    while True:
        full_name = input("Enter the full name: ")
        subject = input("Enter the subject: ")
        email_address = input("Enter an email address: ")
        message = input("Enter your message: ")

        first_name = full_name.split()[0].capitalize()
        last_name = full_name.split()[-1].capitalize()

        test_email = Email(first_name=first_name,
                           last_name=last_name,
                           subject=subject,
                           to=email_address,
                           message=message)
        if test_email.isValidEmail():
            test_email.sendEmail()
        else:
            print("Invalid Email")


if __name__ == "__main__":
    print("Checking emails")
    main()

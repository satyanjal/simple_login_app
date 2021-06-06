import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from login_app import settings
from simple_login_app.models import User


def datetime_now():
    return datetime.datetime.now()


def log_error_traceback(e, traceback):
    return f'\nError- {str(e)}\nTraceback- {str(traceback.format_exc())}'


def trigger_client_login_request_mail(user):
    # create message object instance
    msg = MIMEMultipart()

    message = f"Please approve Login request for the {user.firstname}"

    # setup the parameters of the message
    admins = User.get_all_admin_user()
    for admin in admins:
        password = settings.MAIL_PASSWORD
        msg['From'] = settings.APP_EMAIL
        msg['To'] = admin.email
        msg['Subject'] = f"Approve Login Request for {user.firstname}"

        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

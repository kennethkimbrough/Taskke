# email_config.py
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
FROM_EMAIL = 'your_email@gmail.com'
PASSWORD = 'your_password'

# email_notifier.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template

from email_config import SMTP_SERVER, SMTP_PORT, FROM_EMAIL, PASSWORD

def send_email_notification(user, task):
    # Create a text message
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = user.email
    msg['Subject'] = 'New Task Assigned: {}'.format(task.name)

    # Render the email template
    template = Template(open('email_template.html').read())
    body = template.render(user=user, task=task)
    msg.attach(MIMEText(body, 'html'))

    # Send the email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(FROM_EMAIL, PASSWORD)
    server.sendmail(FROM_EMAIL, user.email, msg.as_string())
    server.quit()

    print('Email sent to {}'.format(user.email))




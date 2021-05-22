import smtplib
from email.message import EmailMessage

# your email username
EMAIL_ADDRESS = ''
# your email password
EMAIL_PASSWORD = ''

def sendEmail(name, url):
    msg = EmailMessage()
    msg['Subject'] = f'"{name}" is available! (automated email)'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ''

    msg.set_content('This is a plain text email')

    msg.add_alternative(f"""\
    <!DOCTYPE html>
    <html>
        <body>
            <h1 style><a href="{url}">"{name}" is available!</a></h1>
        </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
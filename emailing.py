import smtplib, os, ssl
from email.message import EmailMessage
import imghdr

SENDER = "meetapple191@gmail.com"
PASSWORD = os.getenv("py_web")
RECEIVER = "meetsiddhapura@gmail.com"
HOST = "smtp.gmail.com"
PORT = 587

def send_email(image_path):
    print("Email sending started")
    email_message=EmailMessage()
    email_message["Subject"]="New Customer has entered!!"
    email_message.set_content("Hi, Can you assist the new customer")

    with open(image_path,"rb") as file:
        content=file.read()
    email_message.add_attachment(content,maintype="image", subtype=imghdr.what(None,content))

    gmail=smtplib.SMTP(HOST,PORT)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER,PASSWORD)
    gmail.sendmail(SENDER,RECEIVER,email_message.as_string())
    gmail.quit()
    print("Email sent ")
if __name__=="__main__":
    send_email(image_path="images/10.png")
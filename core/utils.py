from django.core.mail import EmailMessage

def send_mail(data):
    email = EmailMessage(
        subject = data["subject"],
        body = data["body"],
        to = [data["receiver"]]
    )
    email.send()
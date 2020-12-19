from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template


def send_email_attachment(title, description, start_time, end_time, send_to, message):
    message = EmailMultiAlternatives(subject=title, body=description,from_email=request.user.email, to=[send_to])
    html_templ = get_template("cal/email.html").render({'title':title, 'description': description, "start_time":start_time, "end_time":end_time, "send_to":send_to, 'message':message,})
    message.attach_alternative(html_templ, "text/html")
    message.send()
    print("email sent")
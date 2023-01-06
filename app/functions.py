from django.conf import settings
# from django.core.mail import send_mail

def check_price(course):
    if course.discount:
        return course.get_total
    else:
        return course.price


# def send_message():
#     subject='Skola Registration'
#     message='Thank you for Registration'
#     email_from=settings.EMAIL_HOST
#     send_mail(
#         subject , message , email_from , ['mahmoudateff07@gmail.com']
#     )

# send_message()
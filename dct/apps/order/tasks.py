from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from apps.order.services.ReportGenerator import report_generate


@shared_task
def send_workstatus_complete_email_task(
    user_email,
    car=None,
    total_price=None
):
    name = "Пользователь"
    subject = f'Изменение статуса работы для {name}!'
    message = f'Здравствуйте, {name}! Ваша машина {car} готова.'\
        f'Сумма к оплате: {total_price}'

    try:
        generate_report_task.delay(5)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        return f"email sent to {user_email}"
    except Exception as e:
        return f"Failed to send complete email to {user_email}: {str(e)}"


@shared_task
def generate_report_task(a: int):
    report_generate(a)

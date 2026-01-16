from celery import shared_task, current_app, Celery
from celery.schedules import crontab
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject="Book Loaned Successfully",
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans():
    enddate = datetime.now() - timedelta(days=15)
    loans = Loan.objects.filter(is_returned=False, due_date__lte=enddate)
    try:
        for loan in loans:
            member_email = loan.member.user.email
            book_title = loan.book.title
            send_mail(
                subject="Book Loaned Successfully",
                message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[member_email],
                fail_silently=False,
            )
    except Loan.DoesNotExist:
        pass


@current_app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(
        crontab(day_of_month=15),
        check_overdue_loans(),
        name="add every 15 days",
    )

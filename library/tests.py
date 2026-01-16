from django.test import TestCase
from .models import Book, Author, Member, Loan
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

# Create your tests here.


class TestLoanTask(TestCase):

    def setUp(self):
        self._user = get_user_model().objects.create(username="testuser")

        self._author = Author.objects.create(first_name="Jhon", last_name="Doe")
        self._book = Book.objects.create(
            title="Test title 01",
            author=self._author,
            isbn="123",
            genre=Book.GENRE_CHOICES[0][0],
        )
        self._member = Member.objects.create(user=self._user)
        self._loan = Loan.objects.create(
            book=self._book,
            member=self._member,
        )

    def test_loan_due_date_filter_should_return_zero(self):
        enddate = datetime.now() - timedelta(days=15)
        loans = Loan.objects.filter(is_returned=False, due_date__lte=enddate)
        self.assertEqual(len(loans), 0)

    def test_loan_due_date_filter_should_return_one(self):
        loan = Loan.objects.create(
            book=self._book,
            member=self._member,
        )
        loan.due_date = datetime.now()
        loan.save()
        enddate = datetime.now()
        loans = Loan.objects.filter(is_returned=False, due_date__lte=enddate)
        self.assertEqual(len(loans), 1)

    def test_extend_loan_due_date(self):
        self.client.force_login(self._user)
        self._loan.due_date = datetime.now()
        self._loan.save()
        response = self.client.post(
            f"/api/loans/{self._loan.id}/extend_due_date/", data={"additional_days": 7}
        )
        loan = response.json()
        self.assertEqual(
            loan["due_date"], (datetime.now() + timedelta(days=7)).date().isoformat()
        )

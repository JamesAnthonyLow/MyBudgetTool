import pytest
import csv
import datetime
from models import (
    Transactions,
    AmexCreditCardActivity,
    ChaseBankAccountActivity,
    ChaseBankAccountActivityType,
    ChaseBankAccountActivityDetails,
    ChaseCreditCardActivity,
)


@pytest.mark.parametrize(
    "file,expected",
    [
        ("tests/amex.csv", AmexCreditCardActivity),
        ("tests/chase_bank_account.csv", ChaseBankAccountActivity),
        ("tests/chase_credit_card.csv", ChaseCreditCardActivity),
    ],
)
def test_match_transaction_class(file, expected):
    with open(file) as csvfile:
        assert Transactions.match_transaction_class(csvfile) == expected


def test_parse_csvs():
    transactions = Transactions.from_csvs("tests/")
    assert len(transactions.transactions) == 20
    assert transactions == Transactions(
        transactions=[
            ChaseCreditCardActivity(
                date=datetime.date(2022, 1, 25),
                description="Hello World6",
                amount=-96.0,
                category="Entertainment",
                post_date=datetime.date(2022, 1, 27),
                type="Sale",
                memo="",
            ),
            ChaseCreditCardActivity(
                date=datetime.date(2022, 1, 27),
                description="Hello World1",
                amount=-10.0,
                category="Personal",
                post_date=datetime.date(2022, 1, 30),
                type="Sale",
                memo="",
            ),
            ChaseCreditCardActivity(
                date=datetime.date(2022, 1, 27),
                description="Hello World4",
                amount=-164.0,
                category="Personal",
                post_date=datetime.date(2022, 1, 28),
                type="Sale",
                memo="",
            ),
            ChaseCreditCardActivity(
                date=datetime.date(2022, 1, 28),
                description="Hello World3",
                amount=-25.99,
                category="Shopping",
                post_date=datetime.date(2022, 1, 30),
                type="Sale",
                memo="",
            ),
            ChaseCreditCardActivity(
                date=datetime.date(2022, 1, 28),
                description="Hello World5",
                amount=-86.0,
                category="Groceries",
                post_date=datetime.date(2022, 1, 28),
                type="Sale",
                memo="",
            ),
            ChaseCreditCardActivity(
                date=datetime.date(2022, 1, 30),
                description="Hello World2",
                amount=-200.0,
                category="Professional Services",
                post_date=datetime.date(2022, 1, 30),
                type="Sale",
                memo="",
            ),
            AmexCreditCardActivity(
                date=datetime.date(2022, 12, 21),
                description="Hello World9",
                amount=27.78,
                category=None,
            ),
            AmexCreditCardActivity(
                date=datetime.date(2022, 12, 22),
                description="Hello World6",
                amount=5.0,
                category=None,
            ),
            AmexCreditCardActivity(
                date=datetime.date(2022, 12, 22),
                description="Hello World7",
                amount=9.99,
                category=None,
            ),
            AmexCreditCardActivity(
                date=datetime.date(2022, 12, 22),
                description="Hello World8",
                amount=10.84,
                category=None,
            ),
            AmexCreditCardActivity(
                date=datetime.date(2022, 12, 23),
                description="Hello World5",
                amount=21.76,
                category=None,
            ),
            AmexCreditCardActivity(
                date=datetime.date(2022, 12, 24),
                description="Hello World4",
                amount=10.99,
                category=None,
            ),
            AmexCreditCardActivity(
                date=datetime.date(2022, 12, 29),
                description="Hello World3",
                amount=15.99,
                category=None,
            ),
            AmexCreditCardActivity(
                date=datetime.date(2022, 12, 30),
                description="Hello World2",
                amount=22.94,
                category=None,
            ),
            AmexCreditCardActivity(
                date=datetime.date(2022, 12, 31),
                description="Hello World1",
                amount=27.49,
                category=None,
            ),
            ChaseBankAccountActivity(
                date=datetime.date(2023, 2, 2),
                description="Hello World5",
                amount=-1096.18,
                category=None,
                details=ChaseBankAccountActivityDetails.DEBIT,
                type=ChaseBankAccountActivityType.ACH_DEBIT,
                balance=20602.22,
                check_or_slip_no="",
            ),
            ChaseBankAccountActivity(
                date=datetime.date(2023, 2, 15),
                description="Hello World3",
                amount=-438.71,
                category=None,
                details=ChaseBankAccountActivityDetails.DEBIT,
                type=ChaseBankAccountActivityType.ACH_DEBIT,
                balance=12667.19,
                check_or_slip_no="",
            ),
            ChaseBankAccountActivity(
                date=datetime.date(2023, 2, 15),
                description="Hello World4",
                amount=-600.0,
                category=None,
                details=ChaseBankAccountActivityDetails.DEBIT,
                type=ChaseBankAccountActivityType.ACH_DEBIT,
                balance=13105.9,
                check_or_slip_no="",
            ),
            ChaseBankAccountActivity(
                date=datetime.date(2023, 2, 21),
                description="Hello World2",
                amount=-61.19,
                category=None,
                details=ChaseBankAccountActivityDetails.DEBIT,
                type=ChaseBankAccountActivityType.ACH_DEBIT,
                balance=12406.0,
                check_or_slip_no="",
            ),
            ChaseBankAccountActivity(
                date=datetime.date(2023, 2, 22),
                description="Hello World1",
                amount=-600.0,
                category=None,
                details=ChaseBankAccountActivityDetails.DEBIT,
                type=ChaseBankAccountActivityType.ACH_DEBIT,
                balance=11806.0,
                check_or_slip_no="",
            ),
        ]
    )

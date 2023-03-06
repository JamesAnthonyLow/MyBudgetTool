import datetime

from models import AmexCreditCardActivity


def test_parse_csv():
    rows = AmexCreditCardActivity.from_csv("tests/amex.csv")
    assert rows == [
        AmexCreditCardActivity(
            date=datetime.date(2022, 12, 31), description="Hello World1", amount=27.49
        ),
        AmexCreditCardActivity(
            date=datetime.date(2022, 12, 30), description="Hello World2", amount=22.94
        ),
        AmexCreditCardActivity(
            date=datetime.date(2022, 12, 29), description="Hello World3", amount=15.99
        ),
        AmexCreditCardActivity(
            date=datetime.date(2022, 12, 24), description="Hello World4", amount=10.99
        ),
        AmexCreditCardActivity(
            date=datetime.date(2022, 12, 23), description="Hello World5", amount=21.76
        ),
        AmexCreditCardActivity(
            date=datetime.date(2022, 12, 22), description="Hello World6", amount=5.0
        ),
        AmexCreditCardActivity(
            date=datetime.date(2022, 12, 22), description="Hello World7", amount=9.99
        ),
        AmexCreditCardActivity(
            date=datetime.date(2022, 12, 22), description="Hello World8", amount=10.84
        ),
        AmexCreditCardActivity(
            date=datetime.date(2022, 12, 21), description="Hello World9", amount=27.78
        ),
    ]

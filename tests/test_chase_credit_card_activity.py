import datetime

from models import ChaseCreditCardActivity


def test_parse_csv():
    with open("tests/chase_credit_card.csv") as csv:
        rows = ChaseCreditCardActivity.from_csv(csv)
        assert len(rows) == 6
        assert rows == [
            ChaseCreditCardActivity(
                date=datetime.date(2022, 1, 27),
                post_date=datetime.date(2022, 1, 30),
                description="Hello World1",
                category="Personal",
                type="Sale",
                amount=-10.0,
                memo="",
            ),
            ChaseCreditCardActivity(
                date=datetime.date(2022, 1, 30),
                post_date=datetime.date(2022, 1, 30),
                description="Hello World2",
                category="Professional Services",
                type="Sale",
                amount=-200.0,
                memo="",
            ),
            ChaseCreditCardActivity(
                date=datetime.date(2022, 1, 28),
                post_date=datetime.date(2022, 1, 30),
                description="Hello World3",
                category="Shopping",
                type="Sale",
                amount=-25.99,
                memo="",
            ),
            ChaseCreditCardActivity(
                date=datetime.date(2022, 1, 27),
                post_date=datetime.date(2022, 1, 28),
                description="Hello World4",
                category="Personal",
                type="Sale",
                amount=-164.0,
                memo="",
            ),
            ChaseCreditCardActivity(
                date=datetime.date(2022, 1, 28),
                post_date=datetime.date(2022, 1, 28),
                description="Hello World5",
                category="Groceries",
                type="Sale",
                amount=-86.0,
                memo="",
            ),
            ChaseCreditCardActivity(
                date=datetime.date(2022, 1, 25),
                post_date=datetime.date(2022, 1, 27),
                description="Hello World6",
                category="Entertainment",
                type="Sale",
                amount=-96.0,
                memo="",
            ),
        ]

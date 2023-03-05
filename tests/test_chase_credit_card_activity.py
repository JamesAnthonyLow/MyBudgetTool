import datetime
from models import ChaseCreditCardActivity


def test_parse_csv():
    rows = ChaseCreditCardActivity.from_csv("tests/chase_credit_card.csv")
    assert rows == [
        ChaseCreditCardActivity(
            transaction_date=datetime.date(2022, 1, 27),
            post_date=datetime.date(2022, 1, 30),
            description="ACT ASPHALT GREEN",
            category="Personal",
            type="Sale",
            amount=-10.0,
            memo=None,
        ),
        ChaseCreditCardActivity(
            transaction_date=datetime.date(2022, 1, 30),
            post_date=datetime.date(2022, 1, 30),
            description="PAYPAL *JOSEPH.WISE.MD",
            category="Professional Services",
            type="Sale",
            amount=-200.0,
            memo=None,
        ),
        ChaseCreditCardActivity(
            transaction_date=datetime.date(2022, 1, 28),
            post_date=datetime.date(2022, 1, 30),
            description="PAYPAL *PETKITNETWO PE",
            category="Shopping",
            type="Sale",
            amount=-25.99,
            memo=None,
        ),
        ChaseCreditCardActivity(
            transaction_date=datetime.date(2022, 1, 27),
            post_date=datetime.date(2022, 1, 28),
            description="BATTERY PARK VETERINARY H",
            category="Personal",
            type="Sale",
            amount=-164.0,
            memo=None,
        ),
        ChaseCreditCardActivity(
            transaction_date=datetime.date(2022, 1, 28),
            post_date=datetime.date(2022, 1, 28),
            description="PAYPAL *TRADECOFFEE",
            category="Groceries",
            type="Sale",
            amount=-86.0,
            memo=None,
        ),
        ChaseCreditCardActivity(
            transaction_date=datetime.date(2022, 1, 25),
            post_date=datetime.date(2022, 1, 27),
            description="BLUE MOUNTAIN RESORT- E",
            category="Entertainment",
            type="Sale",
            amount=-96.0,
            memo=None,
        ),
    ]

import datetime

from models import (ChaseBankAccountActivity, ChaseBankAccountActivityDetails,
                    ChaseBankAccountActivityType)


def test_parse_csv():
    rows = ChaseBankAccountActivity.from_csv("tests/chase_bank_account.csv")
    assert rows == [
        ChaseBankAccountActivity(
            details=ChaseBankAccountActivityDetails.DEBIT,
            posting_date=datetime.date(2023, 2, 22),
            description="Hello World1",
            amount=-600.0,
            type=ChaseBankAccountActivityType.ACH_DEBIT,
            balance=11806.0,
            check_or_slip_no=None,
        ),
        ChaseBankAccountActivity(
            details=ChaseBankAccountActivityDetails.DEBIT,
            posting_date=datetime.date(2023, 2, 21),
            description="Hello World2",
            amount=-61.19,
            type=ChaseBankAccountActivityType.ACH_DEBIT,
            balance=12406.0,
            check_or_slip_no=None,
        ),
        ChaseBankAccountActivity(
            details=ChaseBankAccountActivityDetails.DEBIT,
            posting_date=datetime.date(2023, 2, 15),
            description="Hello World3",
            amount=-438.71,
            type=ChaseBankAccountActivityType.ACH_DEBIT,
            balance=12667.19,
            check_or_slip_no=None,
        ),
        ChaseBankAccountActivity(
            details=ChaseBankAccountActivityDetails.DEBIT,
            posting_date=datetime.date(2023, 2, 15),
            description="Hello World4",
            amount=-600.0,
            type=ChaseBankAccountActivityType.ACH_DEBIT,
            balance=13105.9,
            check_or_slip_no=None,
        ),
        ChaseBankAccountActivity(
            details=ChaseBankAccountActivityDetails.DEBIT,
            posting_date=datetime.date(2023, 2, 2),
            description="Hello World5",
            amount=-1096.18,
            type=ChaseBankAccountActivityType.ACH_DEBIT,
            balance=20602.22,
            check_or_slip_no=None,
        ),
    ]

import csv
import datetime
import enum
import typing

import pydantic


class ChaseBankAccountDetails(enum.Enum):
    CHECK = "CHECK"
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    DSLIP = "DSLIP"


class ChaseBankAccountType(enum.Enum):
    ACCT_XFER = "ACCT_XFER"
    ACH_CREDIT = "ACH_CREDIT"
    ACH_DEBIT = "ACH_DEBIT"
    ATM = "ATM"
    BILLPAY = "BILLPAY"
    CHECK_DEPOSIT = "CHECK_DEPOSIT"
    CHECK_PAID = "CHECK_PAID"
    DEBIT_CARD = "DEBIT_CARD"
    DEPOSIT_RETURN = "DEPOSIT_RETURN"
    FEE_TRANSACTION = "FEE_TRANSACTION"
    MISC_CREDIT = "MISC_CREDIT"
    MISC_DEBIT = "MISC_DEBIT"
    QUICKPAY_CREDIT = "QUICKPAY_CREDIT"
    QUICKPAY_DEBIT = "QUICKPAY_DEBIT"
    REFUND_TRANSACTION = "REFUND_TRANSACTION"


class ChaseBankAccount(pydantic.BaseModel):
    details: ChaseBankAccountDetails
    posting_date: datetime.date
    description: str
    amount: float
    type: ChaseBankAccountType
    balance: float
    check_or_slip_no: typing.Optional[str]

    @pydantic.validator("posting_date", pre=True)
    def parse_birthdate(cls, value: typing.Union[str, datetime.date]) -> datetime.date:
        if isinstance(value, str):
            return datetime.datetime.strptime(value, "%m/%d/%Y").date()
        else:
            return value

    @classmethod
    def from_csv(cls, filename: str) -> typing.List["ChaseBankAccount"]:
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)

            def _from_row(row: typing.Dict[str, typing.Any]) -> "ChaseBankAccount":
                try:
                    return cls(
                        details=row["Details"],
                        posting_date=row["Posting Date"],
                        description=row["Description"],
                        amount=row["Amount"],
                        type=row["Type"],
                        balance=row["Balance"],
                        check_or_slip_no=row["Check or Slip #"],
                    )
                except pydantic.ValidationError as e:
                    e.add_note(f"{row}")
                    raise e

            return [_from_row(row) for row in reader]

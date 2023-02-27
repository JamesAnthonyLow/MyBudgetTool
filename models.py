import csv
import datetime
import enum
import typing

import pydantic


class ChaseBankAccountActivityDetails(enum.Enum):
    CHECK = "CHECK"
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    DSLIP = "DSLIP"


class ChaseBankAccountActivityType(enum.Enum):
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


class ChaseDate(datetime.date):
    @classmethod
    def __get_validators__(cls):
        def _parse_date(value) -> datetime.date:
            if isinstance(value, str):
                return datetime.datetime.strptime(value, "%m/%d/%Y").date()
            else:
                return value

        yield _parse_date


class ChaseBankAccountActivity(pydantic.BaseModel):
    details: ChaseBankAccountActivityDetails
    posting_date: ChaseDate
    description: str
    amount: float
    type: ChaseBankAccountActivityType
    balance: float
    check_or_slip_no: typing.Optional[str]

    @classmethod
    def from_csv(cls, filename: str) -> typing.List["ChaseBankAccountActivity"]:
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)

            def _from_row(
                row: typing.Dict[str, typing.Any]
            ) -> "ChaseBankAccountActivity":
                try:
                    return cls(
                        details=row["Details"],
                        posting_date=row["Posting Date"],
                        description=row["Description"],
                        amount=row["Amount"],
                        type=row["Type"],
                        balance=row["Balance"],
                        check_or_slip_no=row["Check or Slip #"]
                        if row["Check or Slip #"] != ""
                        else None,
                    )
                except pydantic.ValidationError as e:
                    e.add_note(f"{row}")
                    raise e

            return [_from_row(row) for row in reader]


class ChaseCreditCardActivity(pydantic.BaseModel):
    transaction_date: ChaseDate
    post_date: ChaseDate
    description: str
    category: str
    type: str
    amount: float
    memo: typing.Optional[str]

    @pydantic.validator("transaction_date", pre=True)
    def parse_transaction_date(
        cls, value: typing.Union[str, datetime.date]
    ) -> datetime.date:
        if isinstance(value, str):
            return datetime.datetime.strptime(value, "%m/%d/%Y").date()
        else:
            return value

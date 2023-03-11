import abc
import csv
import datetime
import enum
import os
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


class FormattedDate(datetime.date):
    @classmethod
    def __get_validators__(cls):
        def _parse_date(value) -> datetime.date:
            if isinstance(value, str):
                return datetime.datetime.strptime(value, "%m/%d/%Y").date()
            else:
                return value

        yield _parse_date


class CsvMixin(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def __row_to_kwargs__(
        cls, row: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        return {}

    @classmethod
    def from_csv_exn(cls, filename: str) -> typing.List[typing.Any]:
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)

            def _from_row(row: typing.Dict[str, typing.Any]) -> typing.Any:
                try:
                    return cls(**cls.__row_to_kwargs__(row))
                except pydantic.ValidationError as e:
                    e.add_note(f"{row}")
                    raise e

            return [_from_row(row) for row in reader]

    @classmethod
    def from_csv(cls, filename: str) -> typing.Optional[typing.List[typing.Any]]:
        try:
            return cls.from_csv_exn(filename)
        except pydantic.ValidationError:
            return None


class Transaction(pydantic.BaseModel, CsvMixin):
    date: FormattedDate
    description: str
    amount: float
    category: typing.Optional[str] = None


class ChaseBankAccountActivity(Transaction):
    details: ChaseBankAccountActivityDetails
    date: FormattedDate
    description: str
    amount: float
    type: ChaseBankAccountActivityType
    balance: float
    check_or_slip_no: typing.Optional[str]

    @classmethod
    def __row_to_kwargs__(
        cls, row: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        return {
            "details": row["Details"],
            "date": row["Posting Date"],
            "description": row["Description"],
            "amount": row["Amount"],
            "type": row["Type"],
            "balance": row["Balance"],
            "check_or_slip_no": row["Check or Slip #"]
            if row["Check or Slip #"] != ""
            else None,
        }


class ChaseCreditCardActivity(Transaction):
    date: FormattedDate
    post_date: FormattedDate
    description: str
    type: str
    amount: float
    memo: typing.Optional[str]

    @classmethod
    def __row_to_kwargs__(
        cls, row: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        return {
            "date": row["Transaction Date"],
            "post_date": row["Post Date"],
            "description": row["Description"],
            "category": row["Category"],
            "type": row["Type"],
            "amount": row["Amount"],
            "memo": row["Memo"] if row["Memo"] != "" else None,
        }


class AmexCreditCardActivity(Transaction):
    date: FormattedDate
    description: str
    amount: float

    @classmethod
    def __row_to_kwargs__(
        cls, row: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        return {
            "date": row["Date"],
            "description": row["Description"],
            "amount": row["Amount"],
        }


class NoEntriesInCSV(Exception):
    ...


class Transactions(pydantic.BaseModel):
    __root__: typing.List[Transaction]

    @classmethod
    def from_csvs(cls, path: str) -> "Transactions":
        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a directory")

        csv_files = [
            filename
            for filename in os.listdir(path)
            if filename.endswith(".csv") or filename.endswith(".CSV")
        ]

        transactions: typing.List[Transaction] = []
        for csv in csv_files:
            parsed_transactions = next(
                (
                    transaction.from_csv(csv)
                    for transaction in [
                        ChaseBankAccountActivity,
                        ChaseCreditCardActivity,
                        AmexCreditCardActivity,
                    ]
                ),
                None,
            )
            if parsed_transactions is None:
                raise NoEntriesInCSV(f"{csv}")
            transactions.extend(parsed_transactions)

        return cls.parse_obj(sorted(transactions, key=lambda r: r.date))

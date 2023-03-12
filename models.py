import abc
import csv
import datetime
import enum
import io
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
    def headers(cls) -> typing.Dict[str, str]:
        return {}

    @classmethod
    def from_csv(cls, csvfile: io.TextIOWrapper) -> typing.List[typing.Any]:
        reader = csv.DictReader(csvfile)

        def _from_row(row: typing.Dict[str, typing.Any]) -> typing.Any:
            try:
                kwargs = {alias: row[column] for column, alias in cls.headers().items()}
                return cls(**kwargs)
            except Exception as e:
                e.add_note(f"{row}")
                raise e

        return [_from_row(row) for row in reader]


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
    def headers(cls) -> typing.Dict[str, str]:
        return {
            "Details": "details",
            "Posting Date": "date",
            "Description": "description",
            "Amount": "amount",
            "Type": "type",
            "Balance": "balance",
            "Check or Slip #": "check_or_slip_no",
        }


class ChaseCreditCardActivity(Transaction):
    date: FormattedDate
    post_date: FormattedDate
    description: str
    type: str
    amount: float
    memo: typing.Optional[str]

    @classmethod
    def headers(cls) -> typing.Dict[str, str]:
        return {
            "Transaction Date": "date",
            "Post Date": "post_date",
            "Description": "description",
            "Category": "category",
            "Type": "type",
            "Amount": "amount",
            "Memo": "memo",
        }


class AmexCreditCardActivity(Transaction):
    date: FormattedDate
    description: str
    amount: float

    @classmethod
    def headers(cls) -> typing.Dict[str, str]:
        return {
            "Date": "date",
            "Description": "description",
            "Amount": "amount",
        }


class Transactions(pydantic.BaseModel):
    transactions: typing.List[Transaction]

    @classmethod
    def match_transaction_class(
        cls,
        file: io.TextIOWrapper,
    ) -> typing.Optional[type[typing.Any]]:
        reader = csv.DictReader(file)
        columns = set((key for key in next(reader).keys() if key is not None))
        file.seek(0)
        all = [
            ChaseBankAccountActivity,
            ChaseCreditCardActivity,
            AmexCreditCardActivity,
        ]

        def _is_match(m: type[typing.Any]) -> bool:
            headers = set(m.headers().keys())
            return headers == columns

        return next((m for m in all if _is_match(m)), None)

    @classmethod
    def from_csvs(cls, path: str) -> "Transactions":
        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a directory")

        csv_files = [
            f"{path}/{filename}"
            for filename in os.listdir(path)
            if filename.endswith(".csv") or filename.endswith(".CSV")
        ]

        transactions: typing.List[Transaction] = []
        for file in csv_files:
            with open(file) as csvfile:
                transaction_class = cls.match_transaction_class(csvfile)
                if transaction_class is None:
                    raise ValueError(f"CSV file headers are invalid: {file}")
                transactions.extend(transaction_class.from_csv(csvfile))

        return cls(transactions=sorted(transactions, key=lambda r: r.date))

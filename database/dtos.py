from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserDTO:
    id: int
    username: str | None
    name: str | None
    balance: float
    created_at: datetime


@dataclass
class ImageUploadDTO:
    id: int
    user_id: int
    uploaded_at: datetime


@dataclass
class TransactionDTO:
    id: int
    user_id: int
    amount: float
    transaction_type: str
    created_at: datetime

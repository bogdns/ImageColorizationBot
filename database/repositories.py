import sqlalchemy

from database.dtos import UserDTO
from database.models import User


class UserRepository:
    def __init__(self, session_maker):
        self._session = session_maker

    def create(self, dto: UserDTO) -> None:
        with self._session() as session:
            new_instance: User = User(
                id=dto.id,
                username=dto.username,
                name=dto.name,
                balance=dto.balance,
                created_at=dto.created_at)

            session.add(new_instance)
            session.commit()

    def get_user_by_id(self, user_id: int) -> UserDTO:
        with self._session() as session:
            user = session.get(User, user_id)
            return user.map_to_dto() if user is not None else None

    def update_user(self, user: UserDTO) -> None:
        with self._session() as session:
            query = sqlalchemy.update(User).where(User.id == user.id).values(
                id=user.id,
                username=user.username,
                name=user.name,
                balance=user.balance
            ).execution_options(synchronize_session='fetch')

            session.execute(query)
            session.commit()

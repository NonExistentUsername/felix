from .base_class import Base
from .session import database_session


def init_database() -> None:
    from .base_class import Base
    from .session import engine

    Base.metadata.create_all(bind=engine)

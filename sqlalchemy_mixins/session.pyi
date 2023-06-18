from typing import Optional

from sqlalchemy.orm import Session, Query

from sqlalchemy_mixins.utils import classproperty



class SessionMixin:
    _session: Optional[Session]

    @classmethod
    def set_engine(cls, session: Session) -> None: ...

    @classmethod
    def scoped_session(cls) -> Session: ...

    @classmethod
    def session_scope(cls) -> Session: ...

    @classproperty
    def query(cls) -> Query: ...
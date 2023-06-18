from contextlib import contextmanager

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker, Query

from .utils import classproperty


class NoSessionError(RuntimeError):
    pass


class SessionMixin:
    _session = None

    @classmethod
    def set_engine(cls, engine):
        """
        :type engine: Engine
        """
        cls._engine = engine

    @classmethod
    def scoped_session(cls):
        """
        Provide a transactional scope around a series of operations
        :rtype: scoped_session | Session
        """
        _session = scoped_session(sessionmaker(bind=cls._engine))
        return _session

    @classmethod
    @contextmanager
    def session_scope(cls, *args, **kwargs):
        """
        Provide a transactional scope around a series of operations
        :rtype: scoped_session | Session
        """

        _session_maker = sessionmaker(bind=cls._engine)
        _session = _session_maker()

        try:
            yield _session
            _session.commit()
        except Exception:
            _session.rollback()
            raise
        finally:
            _session.close()

    @classproperty
    def query(cls):
        """
        :rtype: Query
        """
        with cls.session_scope() as session:
            return session.query(cls)

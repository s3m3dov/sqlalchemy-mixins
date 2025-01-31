from .inspection import InspectionMixin
from .session import SessionMixin
from .utils import classproperty


class ModelNotFoundError(ValueError):
    pass


class ActiveRecordMixin(InspectionMixin, SessionMixin):
    __abstract__ = True

    @classproperty
    def settable_attributes(cls):
        return cls.columns + cls.hybrid_properties + cls.settable_relations

    def fill(self, **kwargs):
        for name in kwargs.keys():
            if name in self.settable_attributes:
                setattr(self, name, kwargs[name])
            else:
                raise KeyError("Attribute '{}' doesn't exist".format(name))

        return self

    def save(self):
        """Saves the updated model to the current entity db."""
        session = self.scoped_session()
        try:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @classmethod
    def create(cls, **kwargs):
        """Create and persist a new record for the model
        :param kwargs: attributes for the record
        :return: the new model instance
        """
        return cls().fill(**kwargs).save()

    def update(self, **kwargs):
        """Same as :meth:`fill` method but persists changes to database."""
        return self.fill(**kwargs).save()

    def delete(self):
        """Removes the model from the current entity session and mark for deletion."""
        with self.session_scope() as session:
            self.session.delete(self)

    @classmethod
    def destroy(cls, *ids):
        """Delete the records with the given ids
        :type ids: list
        :param ids: primary key ids of records
        """
        with cls.session_scope() as session:
            for pk in ids:
                obj = cls.find(pk)
                if obj:
                    obj.delete()
            session.flush()

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def first(cls):
        return cls.query.first()

    @classmethod
    def find(cls, id_):
        """Find record by the id
        :param id_: the primary key
        """
        return cls.query.get(id_)

    @classmethod
    def find_or_fail(cls, id_):
        # assume that query has custom get_or_fail method
        result = cls.find(id_)
        if result:
            return result
        else:
            raise ModelNotFoundError(
                "{} with id '{}' was not found".format(cls.__name__, id_)
            )

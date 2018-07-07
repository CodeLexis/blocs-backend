from datetime import datetime

from flask import current_app
import shortuuid
from sqlalchemy.ext.declarative import declared_attr

from application.core.constants import STATUSES, PROGRAMMING_LANGUAGES
from application.core import db


AMOUNT_FIELD = db.DECIMAL(12, 2)


def get_pagination_meta(paginated_query):
    return {
        'pagination': {
            'previous_page': (paginated_query.prev_num if
                              paginated_query.has_prev else None),
            'next_page': (paginated_query.next_num if
                          paginated_query.has_next else None),
            'num_items': paginated_query.total,
            'num_pages': paginated_query.pages,
            'has_next_page': paginated_query.has_next,
            'has_previous_page': paginated_query.has_prev
        }
    }


# def paginate_query(query, per_page=5, page=1):
def prep_paginate_query(query, per_page=None, page=None):
    app = current_app
    page = int(page or app.config['PAGINATION_DEFAULT_PAGE'])
    per_page = int(min((per_page or app.config['PAGINATION_DEFAULT_PER_PAGE']),
                       app.config['PAGINATION_DEFAULT_PER_PAGE']))

    return query.paginate(int(page), int(per_page), error_out=False)


class HasStatus(object):
    @declared_attr
    def status_id(cls):
        return db.Column(
            db.Integer, db.ForeignKey('statuses.id'), 
            default=STATUSES.index('active')+1)


class HasUID(object):
    @declared_attr
    def uid(cls):
        return db.Column(db.String(64), default=shortuuid.uuid)


class LookUp(object):
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))
    

class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.now)
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64))

    @classmethod
    def save(self):
        self.uid = shortuuid.uuid()
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        db.session.commit()

    @classmethod
    def get(self, **kwargs):
        return self.query.filter_by(**kwargs).first()

    @classmethod
    def query_for_active(cls, _desc=False, **kwargs):
        query = cls.query.filter_by(status_id=STATUSES.index('active'),
                                    **kwargs)

        if _desc:
            query.order_by(cls.id.desc())

        return query.all()


class Article(BaseModel, HasUID):
    __tablename__ = 'articles'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Bloc(BaseModel, HasUID, LookUp):
    __tablename__ = 'blocs'


class BlocMembership(BaseModel):
    __tablename__ = 'bloc_memberships'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'))

    user = db.relationship(
        'User', backref=db.backref('bloc_memberships', uselist=True),
        uselist=False)
    bloc = db.relationship(
        'Bloc', backref=db.backref('bloc_memberships', uselist=True),
        uselist=False)


class BlocTag(BaseModel, LookUp):
    __tablename__ = 'bloc_tags'

    description = None
    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'))

    bloc = db.relationship(
        'Bloc', backref=db.backref('bloc_tags', uselist=True),
        uselist=False)


class Course(BaseModel, HasUID):
    __tablename__ = 'courses'

    source_category = db.Column(
        db.Enum(
            'SOCIAL MEDIA', 'ONLINE SCHOOL', name='course_source_categories')
    )
    source = db.Column(
        db.Enum('FACEBOOK', 'UDACITY', name='course_sources')
    )


class Event(BaseModel, HasUID):
    __tablename__ = 'events'

    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'))
    title = db.Column(db.String(128))
    description = db.Column(db.TEXT)
    venue = db.Column(db.String(64))
    datetime = db.Column(db.DateTime)

    bloc = db.relationship(
        'Bloc', backref=db.backref('events', uselist=True),
        uselist=False)


class Job(BaseModel, HasUID):
    __tablename__ = 'jobs'

    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'))
    title = db.Column(db.String(128))
    location = db.Column(db.String(128))
    description = db.Column(db.TEXT)
    salary_amount = db.Column(AMOUNT_FIELD)
    salary_interval = db.Column(db.String(128))
    duration = db.Column(
        db.Enum('SHORT TERM', 'FULL-TIME', 'PART-TIME', name=''))

    bloc = db.relationship(
        'Bloc', backref=db.backref('jobs', uselist=True), uselist=False)


class Post(BaseModel, HasUID):
    __tablename__ = 'posts'

    title = db.Column(db.String(64))
    body = db.Column(db.TEXT)
    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    bloc = db.relationship(
        'Bloc', backref=db.backref('posts', uselist=True),
        uselist=False)

    user = db.relationship(
        'User', backref=db.backref('posts', uselist=True),
        uselist=False)


class Project(BaseModel, HasUID):
    __tablename__  = 'projects'

    title = db.Column(db.String(64))
    description = db.Column(db.TEXT)
    url = db.Column(db.String(256))
    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    bloc = db.relationship(
        'Bloc', backref=db.backref('projects', uselist=True),
        uselist=False)

    user = db.relationship(
        'User', backref=db.backref('projects', uselist=True),
        uselist=False)


class School(BaseModel, HasUID):
    __tablename__ = 'schools'

    name = db.Column(db.String(64))
    category = db.Column(db.Enum(*PROGRAMMING_LANGUAGES))


class Skill(BaseModel, HasUID, LookUp):
    __tablename__ = 'skills'

    description = None
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship(
        'User', backref=db.backref('users', uselist=True),
        uselist=True)


class SoftwareBranch(BaseModel, LookUp):
    __tablename__ = 'software_branches'

    description = None


class UserSoftwareBranch(BaseModel, LookUp):
    __tablename__ = 'user_software_branches'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    software_branch_id = db.Column(
        db.Integer, db.ForeignKey('software_branches.id'))


class Status(BaseModel, LookUp):
    __tablename__ = 'statuses'


class User(BaseModel, HasUID):
    __tablename__  = 'users'

    username = db.Column(db.String(64))
    external_app_uid = db.Column(db.String(64))
    bio = db.Column(db.String(128))
    location = db.Column(db.String(64))
    blocs_platform = db.Column(db.String(16))

    def as_json(self):
        return {
            'username': self.username,
            'bio': self.bio,
            'location': self.location
        }


class ProjectAuthor(BaseModel, HasUID):
    __tablename__  = 'project_authors'
    
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    bloc = db.relationship(
        'Bloc', backref=db.backref('project_authors', uselist=True),
        uselist=False)

    user = db.relationship(
        'User', backref=db.backref('project_authors', uselist=True),
        uselist=False)

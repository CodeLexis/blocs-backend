from datetime import datetime

from flask import current_app
import shortuuid
from sqlalchemy.ext.declarative import declared_attr

from application.core import db
from application.core.constants import (PAGINATE_DEFAULT_PER_PAGE,
    PROGRAMMING_LANGUAGES, STATUSES, TIMEZONES)
from application.core.utils.helpers import generate_random_bloc_color


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

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    uid = db.Column(db.String(64))

    def save(self):
        self.uid = shortuuid.uuid()
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        db.session.commit()

    @classmethod
    def get(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def query_for_active(cls, _desc=False, **kwargs):
        query = cls.query.filter_by(status_id=STATUSES.index('active'),
                                    **kwargs)

        if _desc:
            query.order_by(cls.id.desc())

        return query.all()


class Bloc(BaseModel, HasUID, LookUp):
    __tablename__ = 'blocs'

    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))

    is_private = db.Column(db.Boolean, default=False)
    is_default = db.Column(db.Boolean, default=True)
    invite_code = db.Column(db.String(6))
    theme_color = db.Column(db.String(8), default=generate_random_bloc_color)

    location = db.relationship('Location', backref=db.backref('blocs'))

    @property
    def latest_feeds(self):
        bloc_feeds = BlocFeed.query.filter_by(
            bloc_id=self.id
        ).order_by(
            BlocFeed.id.desc()
        ).limit(PAGINATE_DEFAULT_PER_PAGE)

        return [bloc_feed.feed for bloc_feed in bloc_feeds]

    def generate_invite_code(self):
        raise NotImplementedError

    def set_invite_code(self, _code=None):
        if _code is not None:
            _code = self.generate_invite_code()

        self.invite_code = _code


class BlocFeed(BaseModel):
    __tablename__ = 'bloc_feeds'

    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))
    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'))

    feed = db.relationship(
        'User', backref=db.backref('bloc_memberships', uselist=True),
        uselist=False)
    bloc = db.relationship(
        'Bloc', backref=db.backref('bloc_memberships', uselist=True),
        uselist=False)


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


class BlocsPlatform(BaseModel, LookUp, HasStatus):
    __tablename__ = 'blocs_platforms'

    description = None


class BlocTag(BaseModel, LookUp):
    __tablename__ = 'bloc_tags'

    description = None
    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'))

    bloc = db.relationship(
        'Bloc', backref=db.backref('bloc_tags', uselist=True),
        uselist=False)


class Conversation(BaseModel):
    __tablename__ = 'conversations'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship(
        'User', backref=db.backref('conversations', uselist=True),
        lazy='joined')


class CourseSchedule(BaseModel):
    __tablename__ = 'course_schedules'

    time = db.Column(db.String(12))
    days_of_week = db.Column(db.TEXT)
    timezone = db.Column(db.Enum(*TIMEZONES))

    course_id = db.Column(db.Integer, db.ForeignKey('course_schedules.id'))

    course = db.relationship(
        'Course', backref=db.backref('course_schedules', uselist=True),
        lazy='joined'
    )


class Course(BaseModel, HasUID):
    __tablename__ = 'courses'

    title = db.Column(db.String(128))
    description = db.Column(db.TEXT)
    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'))
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_schedule_id = db.Column(
        db.Integer, db.ForeignKey('course_schedules.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    time = db.Column(db.String(6))
    days_of_week = db.Column(db.TEXT)
    timezone = db.String(6)
    thumbnail = db.Column(db.TEXT)

    source_category = db.Column(
        db.Enum(
            'SOCIAL MEDIA', 'ONLINE SCHOOL', name='course_source_categories')
    )
    source = db.Column(
        db.Enum('FACEBOOK', 'UDACITY', name='course_sources')
    )

    created_by = db.relationship(
        'User', backref=db.backref('courses', uselist=True))

    bloc = db.relationship(
        'Bloc', backref=db.backref('courses'))


    def as_json(self):
        return {
            'title': self.title,
            'description': self.description,
            'created_by': self.created_by.as_json()
        }


class CourseContent(BaseModel):
    __tablename__ = 'course_contents'

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    image = db.Column(db.TEXT)
    video = db.Column(db.TEXT)
    body = db.Column(db.TEXT)


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


class Feed(BaseModel, HasUID):
    __tablename__ = 'feeds'

    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    external_app_uid = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.now)
    message = db.Column(db.TEXT)

    created_by = db.relationship('User', )


class Job(BaseModel, HasUID):
    __tablename__ = 'jobs'

    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'))
    title = db.Column(db.String(128))
    location = db.Column(db.String(128))
    description = db.Column(db.TEXT)
    min_salary = db.Column(AMOUNT_FIELD)
    max_salary = db.Column(AMOUNT_FIELD)
    salary_interval = db.Column(db.String(128))
    duration = db.Column(
        db.Enum('SHORT TERM', 'FULL-TIME', 'PART-TIME', name='job_durations'))

    bloc = db.relationship(
        'Bloc', backref=db.backref('jobs', uselist=True), uselist=False)


class Location(BaseModel):
    __tablename__ = 'locations'

    title = db.Column(db.String(128))
    coordinates = db.Column(db.String(50))
    address = db.Column(db.String(128))
    country = db.Column(db.String(32))
    state = db.Column(db.String(32))
    town = db.Column(db.String(32))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship(
        'User', backref=db.backref('locations', uselist=True),
        uselist=False)


class Message(BaseModel):
    __tablename__ = 'messages'

    conversation_id = db.Column(db.Integer,
                                db.ForeignKey('conversations.id'))
    origin = db.Column(db.Enum('RECEIVED', 'SENT', name='origin'))
    content = db.Column(db.TEXT)

    conversation = db.relationship(
        'Conversation', backref=db.backref('messages', uselist=True), lazy='joined')


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


class ProjectAuthor(BaseModel, HasUID):
    __tablename__  = 'project_authors'

    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    bloc = db.relationship(
        'Bloc', backref=db.backref('project_authors', uselist=True),
        uselist=False)

    user = db.relationship(
        'User', backref=db.backref('project_authors', uselist=True),
        uselist=False)


class School(BaseModel, HasUID):
    __tablename__ = 'schools'

    name = db.Column(db.String(64))


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
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    external_app_uid = db.Column(db.String(64))
    avatar_url = db.Column(db.TEXT)
    bio = db.Column(db.String(128))
    blocs_platform_id = db.Column(
        db.Integer, db.ForeignKey('blocs_platforms.id'))

    @property
    def location(self):
        return self.locations[-1]

    @property
    def blocs(self):
        all_users_blocs = []

        for membership in self.bloc_memberships:
            all_users_blocs.append(membership.bloc)

        return all_users_blocs

    @property
    def has_bloc(self):
        return bool(self.bloc_memberships)

    def as_json(self):
        return {
            'username': self.username,
            'bio': self.bio,
            'location': self.location
        }

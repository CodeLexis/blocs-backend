from flask import g
from flask import Blueprint
from flask.views import MethodView

from application.core.utils.request_response_helpers import (
    api_success_response, current_request_data, get_request_pagination_params)
from application.authentication import login_required
from application.blocs import (get_blocs, get_bloc_members, add_user_to_bloc,
    create_bloc)
from application.events import create_event, get_events_for_bloc
from application.jobs import create_job, get_jobs_for_bloc
from application.posts import get_bloc_posts, add_bloc_post
from application.projects import get_bloc_projects, create_bloc_project
from application.modules.api import api_blueprint


blocs_blueprint = Blueprint(
    'blocs_blueprint', __name__, url_prefix='/api/v1.0/blocs')


class Blocs(MethodView):
    def get(self):
        """Get all blocs"""
        data = current_request_data()

        name = data.get('name')
        tags = data.get('tags')

        blocs = get_blocs(name=name, tags=tags)

        return api_success_response(response_data=blocs)

    @login_required
    def post(self):
        """Create a bloc"""
        data = current_request_data()

        name = data['name']
        description = data['description']
        tags = data['tags']

        create_bloc(name, description, tags)

        return api_success_response(response_data=None, code=201)


class BlocCourses(MethodView):
    def get(self, bloc_uid):
        """Get a list of the projects by the members of a Bloc"""

        projects, meta = get_bloc_projects(
            bloc_uid, **get_request_pagination_params())

        return api_success_response(response_data=projects, response_meta=meta)

    @login_required
    def post(self, bloc_uid):
        """Add a project to a Bloc"""
        data = current_request_data()

        title = data['title']
        description = data['description']
        url = data['url']

        create_bloc_project(title, description, url)

        return api_success_response(response_data=None, code=201)


class BlocEvents(MethodView):
    def get(self, bloc_uid):
        events = get_events_for_bloc(
            bloc_uid, **get_request_pagination_params())

        data = [event.as_json() for event in events]

        return api_success_response(response_data=data, code=201)

    @login_required
    def post(self, bloc_uid):
        """Add an event to a Bloc"""
        data = current_request_data()

        # validators.validate_event_creation_params()

        title = data['title']
        description = data['description']
        venue = data['venue']
        datetime = data['datetime']

        create_event(bloc_uid, title, description, venue, datetime)

        return api_success_response(response_data=None, code=201)


class BlocJobs(MethodView):
    def get(self, bloc_uid):
        jobs = get_jobs_for_bloc(
            bloc_uid, **get_request_pagination_params())

        data = [job.as_json() for job in jobs]

        return api_success_response(response_data=data, code=201)

    @login_required
    def post(self, bloc_uid):
        data = current_request_data()

        title = data['title']
        description = data['description']
        salary_amount = data['salary_amount']
        salary_interval = data['salary_interval']
        duration = data['duration']
        location = data['location']
        weblink = data['weblink']

        create_job(
            bloc_uid, title, description, salary_amount, salary_interval,
            duration, location, weblink)

        return api_success_response(response_data=None, code=201)


class BlocMembers(MethodView):
    def get(self, bloc_uid):
        """Get the members of a Bloc"""

        get_bloc_members(bloc_uid, **get_request_pagination_params())

    @login_required
    def post(self, bloc_uid):
        """Add someone to a bloc"""
        data = current_request_data()

        user_uid = data['user_uid']

        add_user_to_bloc(bloc_uid, user_uid)

        return api_success_response(response_data=None, code=201)


class BlocNews(MethodView):
    def get(self):
        """Get the news of a Bloc"""

    @login_required
    def post(self):
        """Add news to a Bloc.. PAID ADS"""


class BlocFeeds(MethodView):
    def get(self, bloc_uid):
        """Get the posts in a Bloc"""

        get_bloc_posts(bloc_uid, **get_request_pagination_params())

    @login_required
    def post(self, bloc_uid):
        """Add a message to Bloc"""
        data = current_request_data()

        title = data['title']
        body = data['body']
        attachment_uids = data['attachment_uids']

        add_bloc_post(g.user.uid, bloc_uid, title, body, attachment_uids)


class BlocProjects(MethodView):
    def get(self, bloc_uid):
        """Get a list of the projects by the members of a Bloc"""

        projects, meta = get_bloc_projects(
            bloc_uid, **get_request_pagination_params())

        return api_success_response(response_data=projects, response_meta=meta)

    @login_required
    def post(self, bloc_uid):
        """Add a project to a Bloc"""
        data = current_request_data()

        title = data['title']
        description = data['description']
        url = data['url']

        create_bloc_project(title, description, url)

        return api_success_response(response_data=None, code=201)


mappings = [
    ('/blocs', Blocs, 'blocs'),
    ('/blocs/<bloc_uid>/projects', BlocProjects, 'bloc_projects'),
    ('/blocs/<bloc_uid>/feeds', BlocFeeds, 'bloc_feeds'),
    ('/blocs/<bloc_uid>/members', BlocMembers, 'bloc_members'),
    ('/blocs/<bloc_uid>/events', BlocEvents, 'bloc_events'),
    ('/blocs/<bloc_uid>/jobs', BlocJobs, 'bloc_jobs'),
]

for url in mappings:
    path, view, name = url

    blocs_blueprint.add_url_rule(path, view_func=view.as_view(name))

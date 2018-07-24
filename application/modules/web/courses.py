from dateutil import parser as date_parser

from flask import redirect, session, url_for
import requests

from application.core.utils.request_response_helpers import (
    get_request_pagination_params)
from application.core.models import Bloc, Course, User
from application.core.models import prep_paginate_query, get_pagination_meta
from application.courses import create_course
from . import Response
from . import render_template, request, web_blueprint


@web_blueprint.route('/create-course', methods=['GET', 'POST'])
def render_course_creation_page():
    if request.method == 'GET':
        user_id = request.args.get('user_id')

        user = User.get(id=user_id)

        if user.access_token:
            dest_url = url_for(
                'web_blueprint.render_course_creation_page', user_id=user_id)

            return redirect(
                url_for('web_blueprint.oauth_login_request', app='Facebook',
                    motive='all courses are taken over Facebook Live',
                    destination=dest_url,
                    login_url=url_for('web_blueprint.oauth_facebook',
                                      user_id=user_id)
                )
            )

        context = {
            'user_id': user_id,
            'blocs': [bloc.as_json() for bloc in user.blocs],
            'timezones': ['GMT', 'PST', 'CAT'],
            'days_of_week': [
                'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                'Saturday', 'Sunday']
        }

        return render_template('courses/create.html', **context)

    elif request.method == 'POST':
        request_data = request.form

        title = request_data['title']
        bloc = request_data['bloc_name']
        description = request_data['description']
        time = request_data['time']
        days_of_week = request_data['days_of_week']
        timezone = request_data['timezone']
        start_day = request_data['start_day']
        start_month = request_data['start_month']
        start_year = request_data['start_year']
        end_day = request_data['end_day']
        end_month = request_data['end_month']
        end_year = request_data['end_year']
        user_id = request_data['user_id']
        thumbnail = None  # request_data['thumbnail']

        start_date = date_parser.parse(
            '{} {} {}'.format(start_day, start_month, start_year))
        end_date = date_parser.parse(
            '{} {} {}'.format(end_day, end_month, end_year))

        bloc = Bloc.get(name=bloc)

        create_course(
            title=title, description=description, time=time,
            days_of_week=days_of_week, timezone=timezone,
            start_date=start_date, end_date=end_date,
            bloc=bloc, thumbnail=thumbnail, user_id=user_id
        )

        context = {'scope': 'course'}

        return render_template('success.html', **context)


@web_blueprint.route('/courses/<int:course_id>/thubmnail')
def render_course_thumbnail(course_id):
    course = Course.get(id=course_id)

    user_avatar = requests.get(course.created_by.clean_avatar_url).content

    thumbnail_bytes = getattr(course, 'thumbnail', None)

    response = Response(thumbnail_bytes or user_avatar)
    response.mimetype = 'image'

    return response


@web_blueprint.route('/courses/<int:id>/details')
def render_course_details(id):
    course = Course.get(id=id)

    return render_template(
        'courses/details.html', )


@web_blueprint.route('/courses/<int:course_id>/students')
def render_all_course_students(course_id):
    course_students = Course.query.filter_by(course_id=course_id)

    page = (
        prep_paginate_query(course_students, **get_request_pagination_params())
    )

    meta = get_pagination_meta(page)

    users = [course_student.user.as_json() for course_student in page.items]

    return render_template('users_list.html', users=users, meta=meta)


@web_blueprint.route('/abcd')
def render_():
    return render_template('oauth/login_request.html')

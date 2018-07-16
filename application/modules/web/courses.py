from application.core.utils.contexts import current_request_data
from application.core.models import Course, User
from application.courses import create_course
from . import Response
from . import render_template, request, web_blueprint


@web_blueprint.route('/create-course', methods=['GET', 'POST'])
def render_course_creation_page():
    if request.method == 'GET':
        user_id = request.args.get('user_id')

        user = User.get(id=user_id)

        context = {
            'user_id': user_id,
            'blocs': [bloc.as_json() for bloc in user.blocs]
        }

        return render_template('courses/create.html', **context)

    elif request.method == 'POST':
        request_data = current_request_data()

        title = request_data['title']
        bloc = request_data['bloc']
        description = request_data['description']
        time = request_data['time']
        days_of_week = request_data['days_of_week']
        timezone = request_data['timezone']
        start_date = request_data['start_date']
        end_date = request_data['end_date']
        thumbnail = request_data['thumbnail']

        create_course(
            title=title, description=description, time=time,
            days_of_week=days_of_week, timezone=timezone,
            start_date=start_date, end_date=end_date,
            bloc=bloc, thumbnail=thumbnail
        )

        context = {'scope': 'course'}

        return render_template('success.html', **context)


@web_blueprint.route('/courses/<int:id>/thumbnail')
def render_course_thumbnail(id):
    course = Course.get(id=id)

    response = Response(course.thumbnail)
    response.mimetype = 'image'

    return response


@web_blueprint.route('/courses/<int:id>/details')
def render_course_details(id):
    course = Course.get(id=id)

    return render_template(
        'courses/details.html', )

from flask import Response
import requests

from application.core.constants import APP_COLORS, SALARY_INTERVALS
from application.core.models import Bloc, Job, User
from application.jobs import create_job
from . import render_template, request, web_blueprint


@web_blueprint.route('/create-job', methods=['GET', 'POST'])
def render_job_creation_page():
    if request.method == 'GET':
        user_id = request.args.get('user_id')

        user = User.get(id=user_id)

        context = {
            'user_id': user_id,
            'blocs': [bloc.as_json() for bloc in user.blocs],
            'currencies': eval(
                open('static/assets/world_currencies.txt', 'rb').read()
            ),
            'salary_intervals': SALARY_INTERVALS,
            'job_durations': ['SHORT TERM', 'FULL-TIME', 'PART-TIME']
        }

        return render_template('jobs/create.html', **context)

    elif request.method == 'POST':
        title = request.form['title']
        bloc_name = request.form['bloc_name']
        description = request.form['description']
        location = request.form['location']
        duration = request.form['duration']
        min_salary = request.form['min_salary']
        max_salary = request.form['max_salary']
        salary_currency = request.form['salary_currency']
        user_id = request.form['user_id']
        salary_interval = request.form['salary_interval']

        bloc = Bloc.get(name=bloc_name)

        create_job(
            bloc=bloc, title=title, description=description,
            duration=duration, location=location, min_salary=min_salary,
            max_salary=max_salary, salary_interval=salary_interval,
            user_id=user_id, salary_currency=salary_currency
        )

        context = {'scope': 'job'}

        return render_template('success.html', **context)


@web_blueprint.route('/jobs/<int:id>')
def render_job_details_page(id):
    raise NotImplementedError


@web_blueprint.route('/jobs/<int:job_id>/thumbnail')
def render_job_thumbnail(job_id):
    job = Job.get(id=job_id)

    user_avatar = requests.get(job.created_by.clean_avatar_url).content

    thumbnail_bytes = getattr(job, 'thumbnail', None)

    response = Response(thumbnail_bytes or user_avatar)
    response.mimetype = 'image'

    return response


@web_blueprint.route('/jobs/<int:job_id>/applications')
def render_job_application_page(job_id):
    raise NotImplementedError

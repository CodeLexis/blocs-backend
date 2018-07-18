from flask import Response

from application.core.constants import SALARY_INTERVALS
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
        salary_interval = request.form['salary_interval']

        bloc = Bloc.get(name=bloc_name)

        create_job(
            bloc=bloc, title=title, description=description,
            duration=duration, location=location, min_salary=min_salary,
            max_salary=max_salary, salary_interval=salary_interval,
        )

        context = {'scope': 'job'}

        return render_template('success.html', **context)


@web_blueprint.route('/jobs/<int:id>')
def render_job_details_page(id):
    return


@web_blueprint.route('/jobs/<int:id>/thumbnail')
def render_job_thumbnail(id):
    job = Job.get(id=id)

    response = Response(job.thumbnail)
    response.mimetype = 'image'

    return response

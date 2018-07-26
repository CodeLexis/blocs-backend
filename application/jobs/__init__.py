from application.core import errors
from application.core.models import Bloc, Job
from application.core.models import (prep_paginate_query, get_pagination_meta)


def create_job(bloc, user_id, title, description, min_salary, max_salary,
               salary_currency, salary_interval, duration, location):

    job = Job(
        bloc_id=bloc.id, title=title, description=description,
        min_salary=min_salary, max_salary=max_salary,
        salary_interval=salary_interval, duration=duration,
        created_by_id=user_id, salary_currency=salary_currency,
        location=location)

    job.save()

    return job


def get_jobs_for_bloc(bloc_uid, page, per_page):
    bloc = Bloc.get(uid=bloc_uid)
    if bloc is None:
        raise errors.ResourceNotFound('Bloc not found')

    jobs_query = Job.query_for_active(bloc_id=bloc.id).order(bloc.id.desc())

    page = prep_paginate_query(jobs_query, page=page, per_page=per_page)
    meta = get_pagination_meta(page)

    return page.items, meta

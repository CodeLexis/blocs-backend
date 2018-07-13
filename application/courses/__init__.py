from flask import g

from application.core.models import Bloc, Course


def create_course(
        title, description, bloc, time, days_of_week, timezone, start_date,
        end_date):

    bloc_orm = Bloc.get(name=bloc)

    course = Course(
        title=title, description=description,
        created_by_id=g.user.id,
        start_date=start_date,
        end_date=end_date,
        time=time,
        days_of_week=days_of_week,
        timezone=timezone,
        bloc_id=bloc_orm.id
    )

    course.save()

    return course

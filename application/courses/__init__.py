from flask import g

from application.core.models import Bloc, Course


def create_course(
        title, description, bloc, user_id, time, days_of_week, timezone,
        start_date, end_date, thumbnail):

    course = Course(
        title=title, description=description,
        created_by_id=user_id,
        start_date=start_date,
        end_date=end_date,
        time=time,
        days_of_week=days_of_week,
        timezone=timezone,
        bloc_id=bloc.id,
        thumbnail=thumbnail
    )

    course.save()

    return course

#!/usr/bin/env python
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from application.core.constants import DEFAULT_BLOCS
from application.core.models import (
    Bloc, BlocMembership, BlocsPlatform, Status, User)
from app_setup import application, db


manager = Manager(application)
migrate = Migrate(application, db, directory='remote_migrations')

manager.add_command('db', MigrateCommand)


@manager.command
def pump_status_table():
    status_modes_and_ids = (
        'Active', 'Pending', 'Disabled', 'Failed', 'Deleted'
    )

    for status in status_modes_and_ids:
        if Status.get(name=status) is not None:
            continue

        status = Status(name=status)
        status.save()

    # change the last one, which is 'Deleted'
    status.update(id=99)


@manager.command
def pump_blocs_platform_table():
    blocs_platforms = ['Facebook Bot']

    for platform in blocs_platforms:
        if BlocsPlatform.get(name=platform) is not None:
            continue

        BlocsPlatform(name=platform).save()
        # BlocsPlatform(name=platform).save()


@manager.command
def pump_blocs_table():
    for bloc in Bloc.query.all():
        print(bloc.name)

    for bloc in DEFAULT_BLOCS:
        existing_bloc = Bloc.get(name='{} Bloc'.format(bloc))
        if existing_bloc is not None:
            existing_bloc.update(is_default=True)

        Bloc(name='{} Bloc'.format(bloc), is_default=True).save()


@manager.command
def create_dummy_user():
    user = User(
        first_name='First',
        last_name='Last',
        external_app_uid='12345',
        blocs_platform_id=1,
    )

    user.save()


@manager.command
def add_dummy_user_to_bloc():
    user = User.query_for_active()[0]
    bloc = Bloc.query_for_active()[0]

    BlocMembership(user_id=user.id, bloc_id=bloc.id).save()


@manager.command
def run_all_commands():
    print('status')
    pump_status_table()
    print('blocs platforms')
    pump_blocs_platform_table()
    print('blocs')
    pump_blocs_table()


if __name__ == "__main__":
    manager.run()

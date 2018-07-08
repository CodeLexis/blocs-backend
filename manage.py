#!/usr/bin/env python
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from application.core.models import BlocsPlatform, Status
from app_setup import application, db


manager = Manager(application)
migrate = Migrate(application, db)

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
def run_all_commands():
    print('status')
    pump_status_table()
    print('blocs platforms')
    pump_blocs_platform_table()


if __name__ == "__main__":
    manager.run()

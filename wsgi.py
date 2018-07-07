# #!/usr/bin/env python
from app_setup import application, celery  # , configuration_mode


if __name__ == '__main__':
    application.run(
        host=application.config['HOST_IP'],
        port=application.config['HOST_PORT']
    )

import logging

# logging.basicConfig(level=logging.DEBUG,\
#                     format='[%(levelname)s] [%(name)s] [%(threadName)s] [%(module)s]\n%(message)s\n')

from laboratorium import create_app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

from flask_script import Command, Option
import sys


class GunicornServer(Command):
    description = 'Run the app within Gunicorn'

    def __init__(self, host='127.0.0.1', port=8000, workers=4, **options):
        self.port = port
        self.host = host
        self.workers = workers
        self.server_options = options

    def get_options(self):
        return (
            Option('-H', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('-w', '--workers',
                   dest='workers',
                   type=int,
                   default=self.workers),
            Option('--gunicorn-config',
                   dest='config',
                   type=str,
                   required=True),
        )

    def handle(self, app, host, port, workers, config):
        from gunicorn import version_info

        from ConfigParser import ConfigParser
        gc = ConfigParser()
        gc.read(config)
        section = 'default'
        bind = "%s:%s" % (host, str(port))
        workers = gc.get(section, 'workers')
        pidfile = gc.get(section, 'pidfile')
        loglevel = gc.get(section, 'loglevel')

        if version_info < (0, 9, 0):
            raise RuntimeError("Unsupported gunicorn version! Required > 0.9.0")
        else:
            from gunicorn.app.base import Application

            class FlaskApplication(Application):
                def init(self, parser, opts, args):
                    return {
                        'bind': bind,
                        'workers': workers,
                        'pidfile': pidfile,
                        'loglevel': loglevel,
                    }

                def load(self):
                    return app

            # Hacky! Do not pass any cmdline options to gunicorn!
            sys.argv = sys.argv[:2]

            print "Logging to stderr with loglevel '%s'" % loglevel
            print "Starting gunicorn..."
            FlaskApplication().run()

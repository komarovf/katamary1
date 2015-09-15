#!/usr/bin/env python
import os
from nagbook import create_app, db
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand

nagbook = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(nagbook)
migrate = Migrate(nagbook, db)

manager.add_command("runserver", Server(host="0.0.0.0", port=8080))

print


def make_shell_context():
    return dict(treschat=nagbook, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()

from app.app import create_app, db
from app.models import User

from app import fake

app = create_app('test')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, fake=fake)

@app.cli.command()
def test():
 """Run the unit tests."""
 import unittest
 tests = unittest.TestLoader().discover('tests')
 unittest.TextTestRunner(verbosity=2).run(tests)

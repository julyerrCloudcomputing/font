
import os

from app import create_app
from app import db
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
manager=Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    manager.run()

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import create_app
from app.models import db
from flask_cors import CORS

app = create_app("../config.py")
CORS(app, resources={r"/*": {"origins": "*"}}, allowed_headers="Authorization", supports_credentials=True)
manager = Manager(app)
migrate = Migrate(app, db)
# migrate.init_app(app, db)
manager.add_command("db", MigrateCommand)
if __name__ == '__main__':
    manager.run()
    

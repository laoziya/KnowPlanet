from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://qt:123456@192.168.220.110:3306/KnowPlanet?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/test-db')
def test_db():
    result = db.engine.execute('SELECT 1')
    return f'Database connection successful! Result: {result.scalar()}'

app.debug = True
app.run()
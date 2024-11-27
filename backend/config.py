import pytz

# MySQL database URI
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost:3306/flask_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Singapore timezone
SGT = pytz.timezone('Asia/Singapore')

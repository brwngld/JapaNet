from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/japanet'
db = SQLAlchemy(app)

# Define all your models here


if __name__ == "__main__":
    # Print all the tables in the database
   with app.app_context():
        metadata = db.MetaData()
        metadata.reflect(bind=db.engine)
        for table_name in metadata.tables:
            print(table_name)
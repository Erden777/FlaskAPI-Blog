from flask import g, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import BindMetaMixin, Model
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from utils.file_utils import import_modules
from flask_migrate import Migrate


class NoNameMeta(BindMetaMixin, DeclarativeMeta):
    pass

db = SQLAlchemy(model_class=declarative_base(cls=Model, metaclass=NoNameMeta, name='Model'), session_options={"autoflush": False})


def compose_url(databases, schema="default"):
    url = ""
    if schema in databases:
        db_settings = databases[schema]
        db_host = db_settings["DATABASE_HOST"]
        db_port = db_settings["DATABASE_PORT"]
        db_user = db_settings["DATABASE_USER"]
        db_password = db_settings["DATABASE_PASSWORD"]
        db_name = db_settings["DATABASE_NAME"]
        url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    return url

def db_init(app=current_app, **kwargs):
    db_settings = app.config['DATABASES']
    app.config['SQLALCHEMY_DATABASE_URI'] = compose_url(db_settings)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    exclude_models = []

    # include_models = [
    # ]
    migrate = Migrate(app, db)

    import_modules('models', exclude_models)

    @app.teardown_appcontext
    def close_db(exception=None):
        if exception:
            raise exception

        db = g.pop('db', None)
        if db is not None:
            db.session.remove()

    create = kwargs.get('create', True)
    if create == True:
        db.create_all(app=app)

def get_db():
    if 'db' not in g:
        g.db = db

    return g.db

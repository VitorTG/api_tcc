from sqlalchemy import event, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
import json

from connectors.secrets_manager_connector import SecretsManagerConnector

from constants import (
    DB_NAME,
    DB_PASSWORD_SECRET_NAME,
    BYPASS_ENDPOINTS,
)


class PasswordCache:
    password = None
    username = None
    db_host = None
    db_port = None


class SessionManager:
    db_host = PasswordCache.db_host
    path = URL.create("postgresql+psycopg2")

    engine = create_engine(path, echo=False, pool_size=5, pool_recycle=60, pool_pre_ping=True)

    session_class = sessionmaker(bind=engine)
    ThreadSession = scoped_session(session_class)

    @staticmethod
    @event.listens_for(engine, "do_connect")
    def receive_do_connect(dialect, conn_rec, cargs, cparams):
        cparams["password"] = PasswordCache.password
        cparams["user"] = PasswordCache.username
        cparams["host"] = PasswordCache.db_host
        cparams["port"] = PasswordCache.db_port
        cparams["dbname"] = DB_NAME

        try:
            connection = psycopg2.connect(*cargs, **cparams)
        except psycopg2.OperationalError:
            password_dict = json.loads(SecretsManagerConnector.get_secret_by_name(DB_PASSWORD_SECRET_NAME)["secret_string_value"])

            password_value = password_dict["password"]
            PasswordCache.password = password_value
            username_value = password_dict["username"]
            PasswordCache.username = username_value
            db_host_value = password_dict["host"]
            PasswordCache.db_host = db_host_value
            db_port_value = password_dict["port"]
            PasswordCache.db_port = db_port_value

            cparams["password"] = PasswordCache.password
            cparams["user"] = PasswordCache.username
            cparams["host"] = PasswordCache.db_host
            cparams["port"] = PasswordCache.db_port

            connection = psycopg2.connect(*cargs, **cparams)
        return connection

    def process_resource(self, req, resp, resource, params):
        if req.method == "OPTIONS" or req.path in BYPASS_ENDPOINTS:
            return
        req.context.instance.add_session(SessionManager.ThreadSession())

    def process_response(self, req, resp, resource, req_succeeded):
        if req.context.instance.db_session is not None:
            if not req_succeeded:
                req.context.instance.db_session.rollback()
            req.context.instance.db_session.close()

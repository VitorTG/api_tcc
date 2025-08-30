import subprocess
from os import environ


class DbUtils:
    @staticmethod
    def rollback():
        query = "DROP SCHEMA public CASCADE;"
        subprocess.run(
            [
                "/usr/bin/psql",
                "-h",
                environ["SERVER_LOCALHOST"],
                "-U",
                "my_user",
                "-p",
                "5432",
                "my_db",
                "--command",
                query,
            ],
            env={"PGPASSWORD": "my_pwd"},
        )
        query = "CREATE SCHEMA public;"
        subprocess.run(
            [
                "/usr/bin/psql",
                "-h",
                environ["SERVER_LOCALHOST"],
                "-U",
                "my_user",
                "-p",
                "5432",
                "my_db",
                "--command",
                query,
            ],
            env={"PGPASSWORD": "my_pwd"},
        )
        query = "GRANT ALL ON SCHEMA public TO my_user;"
        subprocess.run(
            [
                "/usr/bin/psql",
                "-h",
                environ["SERVER_LOCALHOST"],
                "-U",
                "my_user",
                "-p",
                "5432",
                "my_db",
                "--command",
                query,
            ],
            env={"PGPASSWORD": "my_pwd"},
        )
        query = "GRANT ALL ON SCHEMA public TO public;"
        subprocess.run(
            [
                "/usr/bin/psql",
                "-h",
                environ["SERVER_LOCALHOST"],
                "-U",
                "my_user",
                "-p",
                "5432",
                "my_db",
                "--command",
                query,
            ],
            env={"PGPASSWORD": "my_pwd"},
        )
        subprocess.run(
            [
                "/usr/bin/psql",
                "-h",
                environ["SERVER_LOCALHOST"],
                "-U",
                "my_user",
                "-p",
                "5432",
                "my_db",
                "-f",
                "database/database.sql",
            ],
            env={"PGPASSWORD": "my_pwd"},
        )

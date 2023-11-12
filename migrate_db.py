import glob

import dbapi
from dbapi import close_conn
from dbapi import get_conn


def migrate_database():
    conn = get_conn()
    try:
        for sql_file in glob.glob('migration/*.sql'):
            try:
                print(f'Executing {sql_file}')
                dbapi.dbapi_execute_file(conn, sql_file)
                print(f'Executed {sql_file}')
            except Exception as e:
                print(f'Ignored error from {sql_file}: {str(e)}')
    finally:
        if conn:
            close_conn(conn)


if __name__ == '__main__':
    migrate_database()

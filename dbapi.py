import json
import logging
import os
import uuid

from mysql.connector.pooling import MySQLConnectionPool

g_db_pool = None
g_env = 'ENV' in os.environ and os.environ['ENV'] or 'dev'

SQL_GET_ALL_PRODUCTS = f'SELECT * FROM product'
SQL_GET_PRODUCT = f'SELECT * FROM product WHERE p_id = %s'
SQL_ADD_PRODUCT = f'INSERT INTO product (p_id, p_name, p_unitprice) VALUES (%s, %s, %s)'
SQL_UPDATE_PRODUCT = f'UPDATE product SET p_name = %s, p_unitprice = %s WHERE p_id = %s'
SQL_DELETE_PRODUCT = f'DELETE FROM product WHERE p_id = %s'


def load_config():
    config_json = f'dbconfig-{g_env}.json'
    with open(config_json, 'r') as f:
        config = json.load(f)
    return config


def create_connection_pool(config):
    pool = MySQLConnectionPool(
        pool_name='mypool',
        pool_size=config['pool_size'],
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )
    return pool


def get_conn():
    global g_db_pool
    if g_db_pool is None:
        config = load_config()
        if config:
            g_db_pool = create_connection_pool(config)
        else:
            logging.error('Cannot create connection pool with invalid config!')
    if g_db_pool:
        return g_db_pool.get_connection()
    return None


def close_conn(conn):
    if conn:
        conn.close()


def dbapi_select(conn, query, args=()):
    _conn = conn or get_conn()
    cursor = _conn.cursor()
    cursor.execute(query, args)
    recs = [dict(zip(cursor.column_names, row)) for row in cursor.fetchall()]
    cursor.close()
    if not conn:
        close_conn(_conn)
    return recs


def dbapi_execute(conn, query, args=(), commit=True):
    _conn = conn or get_conn()
    cursor = _conn.cursor()
    cursor.execute(query, args)
    num_affected = cursor.rowcount
    if commit:
        _conn.commit()
    cursor.close()
    if not conn:
        close_conn(_conn)
    return num_affected


def dbapi_execute_file(conn, filename):
    _conn = conn or get_conn()
    with open(filename, 'r') as file:
        content = file.read()
    sqls = content.split(';')
    for sql in sqls:
        if sql.strip() != '':
            dbapi_execute(conn, sql)
            _conn.commit()
    if _conn != conn:
        _conn.close()


def dbapi_get_all_products(conn):
    rows = dbapi_select(conn, SQL_GET_ALL_PRODUCTS)
    return rows


def dbapi_get_product_by_id(conn, p_id):
    args = (p_id,)
    rows = dbapi_select(conn, SQL_GET_PRODUCT, args=args)
    if len(rows) > 0:
        return rows[0]
    return []


def dbapi_add_product(conn, new_product):
    new_id = uuid.uuid4().hex
    args = (new_id, new_product['p_name'], new_product['p_unitprice'],)
    return dbapi_execute(conn, SQL_ADD_PRODUCT, args=args)


def dbapi_update_product(conn, p_id, product):
    args = (product['p_name'], product['p_unitprice'], p_id,)
    return dbapi_execute(conn, SQL_UPDATE_PRODUCT, args=args)


def dbapi_delete_product(conn, p_id):
    args = (p_id,)
    return dbapi_execute(conn, SQL_DELETE_PRODUCT, args=args)

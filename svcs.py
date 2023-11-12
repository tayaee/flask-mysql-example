import dbapi
from dbapi import get_conn


def svc_get_all_products():
    conn = get_conn()
    products = dbapi.dbapi_get_all_products(conn)
    dbapi.close_conn(conn)
    return products


def svc_get_product_by_id(p_id):
    conn = get_conn()
    product = dbapi.dbapi_get_product_by_id(conn, p_id)
    dbapi.close_conn(conn)
    return product


def svc_add_product(new_product):
    conn = get_conn()
    num_affected = dbapi.dbapi_add_product(conn, new_product)
    dbapi.close_conn(conn)
    return num_affected


def svc_update_product(p_id, product):
    conn = get_conn()
    num_affected = dbapi.dbapi_update_product(conn, p_id, product)
    dbapi.close_conn(conn)
    return num_affected


def svc_delete_product(p_id):
    conn = get_conn()
    num_affected = dbapi.dbapi_delete_product(conn, p_id)
    dbapi.close_conn(conn)
    return num_affected

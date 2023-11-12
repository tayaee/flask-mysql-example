import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for

import svcs

app = Flask(__name__)


@app.before_request
def set_session_cookie():
    # TODO: generate session here.
    pass


@app.route('/favicon.ico')
def app_route_favicon_ico():
    path_to_static = os.path.join(app.root_path, 'static')
    return send_from_directory(path_to_static, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    products = svcs.svc_get_all_products()
    return render_template('index.html', products=products)


@app.route('/product/<p_id>', methods=['GET'])
def get_product(p_id):
    products = [svcs.svc_get_product_by_id(p_id)]
    return render_template('index.html', products=products)


@app.route('/product/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        p_name = request.form['p_name']
        p_unitprice = float(request.form['p_unitprice'])
        new_product = {
            'p_name': p_name,
            'p_unitprice': p_unitprice
        }
        svcs.svc_add_product(new_product)
        return redirect(url_for('index'))


@app.route('/product/update/<p_id>', methods=['POST'])
def update_product(p_id):
    if request.method == 'POST':
        p_name = request.form['p_name']
        p_unitprice = float(request.form['p_unitprice'])
        product = {
            'p_id': p_id,
            'p_name': p_name,
            'p_unitprice': p_unitprice
        }
        svcs.svc_update_product(p_id, product)
        return redirect(url_for('index'))


@app.route('/product/delete/<p_id>')
def delete_product(p_id):
    svcs.svc_delete_product(p_id)
    return redirect(url_for('index'))


@app.context_processor
def inject_url_prefix():
    # TODO: make more global variables available in html templates
    return {'app_name': "flask_demo_app"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

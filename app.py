from flask import Flask, render_template, url_for, request
import db
from book import book_bp

app = Flask(__name__)

app.register_blueprint(book_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product_list')
def product_list():
    # cate = request.form.get('cate')
    # product_list = db.select_all_search_merchandise(cate)
    return render_template('product_list.html')

@app.route('/cate_list')
def cate_list():
    # cate = request.form.get('cate')
    # product_list = db.select_all_search_merchandise(cate)
    return render_template('cate_list.html')

@app.route('/search_list')
def search_list():
    return render_template('search_list.html')

if __name__ == '__main__':
    app.run(debug=True)
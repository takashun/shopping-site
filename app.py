from flask import Flask, render_template, url_for, request, redirect, session
import db, string, random
from book import book_bp

app = Flask(__name__)

app.register_blueprint(book_bp)

@app.route('/', methods = ['GET'])
def index():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)

@app.route('/', methods = ['POST'])
def login():
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    if db.login(mail, password):
        return redirect(url_for('product_list'))
    else:
        error = 'ログインに失敗しました。'
        input_data = {
            'mail' : mail,
            'password' : password
        }
        return render_template('index.html', error=error, data=input_data)
    
@app.route('/register')
def register_form():
    return render_template('register_user.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    if user_name == '':
        error = 'ユーザ名が未入力です。'
        return render_template('register_user.html', error=error)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register_user.html', error=error)
    
    count = db.insert_user(user_name, mail, password)
    
    if count == 1:
        msg = '登録が完了しました。'
        return render_template('index.html', msg=msg)
    else:
        error = '登録に失敗しました。'
        return render_template('register_user.html', error=error)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/product_list')
def product_list():
    product_list = db.select_all_merchandise()
    return render_template('product_list.html', product_list=product_list)

@app.route('/cate_list', methods=['GET'])
def cate_list():
    cate = request.args.get('cate')
    product_list = db.select_all_cate_merchandise(cate)
    return render_template('product_list.html', product_list=product_list)

@app.route('/search_list', methods=['POST'])
def search_list():
    key = request.form.get('search')
    product_list = db.select_all_search_merchandise(key)
    return render_template('search_list.html', product_list=product_list)

@app.route('/register_merchandise')
def register_merchandise():
    return render_template('register_merchandise.html')

@app.route('/merchandise_exe', methods=['POST'])
def merchandise_exe():
    name = request.form.get('name')
    price = request.form.get('price')
    cate = request.form.get('cate')
    
    count = db.register_merchandise(name, price, cate)
    if count == 1:
        msg = '登録が完了しました。'
        return render_template('register_merchandise.html', msg=msg)
    else:
        error = '登録に失敗しました。'
        return render_template('register_merchandise.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, url_for, request, redirect, session
import db, string, random
from book import book_bp

app = Flask(__name__)
app.secret_key=''.join(random.choices(string.ascii_letters, k=256))

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
        user_id = db.select_user_id(mail)
        user_id = user_id[0]
        session['user'] = user_id
        print(user_id)
        if user_id == (1,):
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('product_list'))
    else:
        error = 'ログインに失敗しました。'
        input_data = {
            'mail' : mail,
            'password' : password
        }
        return render_template('index.html', error=error, data=input_data)
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/register')
def register_form():
    return render_template('register_user.html')

    
@app.route('/register_exe', methods=['POST'])
def register_exe():
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register_user.html', error=error)
    
    count = db.insert_user(mail, password)
    if count == 1:
        msg = '登録が完了しました。'
        return render_template('index.html', msg=msg)
    else:
        error = '登録に失敗しました。'
        return render_template('register_user.html', error=error)

@app.route('/product_list')
def product_list():
    if 'user' in session:
        product_list = db.select_all_merchandise()
        return render_template('product_list.html', product_list=product_list)
    else:
        return redirect(url_for('index'))

@app.route('/cate_list', methods=['GET'])
def cate_list():
    if 'user' in session:
        cate = request.args.get('cate')
        product_list = db.select_all_cate_merchandise(cate)
        return render_template('product_list.html', product_list=product_list)
    else:
        return redirect(url_for('index'))

@app.route('/search_list', methods=['POST'])
def search_list():
    if 'user' in session:
        key = request.form.get('search')
        product_list = db.select_all_search_merchandise(key)
        return render_template('search_list.html', product_list=product_list)
    else:
        return redirect(url_for('index'))
    
@app.route('/merchandise_detail', methods=['GET'])
def merchandise_detail():
    if 'user' in session:
        name = request.args.get('name')
        merchandise = db.merchandise_detail(name)
        return render_template('merchandise_detail.html', merchandise=merchandise)
    else:
        return redirect(url_for('index'))

@app.route('/register_merchandise')
def register_merchandise():
    if 'user' in session:
        return render_template('register_merchandise.html')
    else:
        return redirect(url_for('index'))

@app.route('/merchandise_exe', methods=['POST'])
def merchandise_exe():
    if 'user' in session:
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
    else:
        return redirect(url_for('index'))

@app.route('/add_cart', methods=['POST'])
def product_cart():
    if 'user' in session:
        user_id = session['user']
        book_id = int(request.form['book_id'])
        selected_book = db.merchandise_id(book_id)
        return render_template('add_cart.html', user_id=user_id, selected_book=selected_book)
    else:
        return redirect(url_for('index'))
    
@app.route('/cart_exe', methods=['POST'])
def cart_add():
    if 'user' in session:
        user_id = session['user']
        name = request.args.get('name')
        price = request.args.get('price')
        db.register_cart(user_id, name, price)
        return redirect(url_for('product_list'))
    else:
        return redirect(url_for('index'))
    
@app.route('/cart_list')
def cart_list():
    if 'user' in session:
        user_id = session['user']
        cart = db.cart_id(user_id)
        return render_template('cart.html', user_id=user_id, cart=cart)
    else:
        return redirect(url_for('index'))

@app.route('/delete_cart', methods=['POST'])
def delete_cart():
    if 'user' in session:
        db.delete_cart(session['user'])
        return redirect(url_for('product_list'))
    else:
        return redirect(url_for('index'))
    
@app.route('/admin')
def admin():
    if 'user' in session:
        product_list = db.select_all_merchandise()
        return render_template('admin_list.html', product_list=product_list)
    else:
        return redirect(url_for('index'))

@app.route('/delete_merchandise', methods=['GET'])
def delete_merchandise():
    if 'user' in session:
        name = request.args.get('name')
        merchandise = db.merchandise_detail(name)
        return render_template('delete_merchandise.html', merchandise=merchandise)
    else:
        return redirect(url_for('index'))
    
@app.route('/cate_admin', methods=['GET'])
def cate_admin():
    if 'user' in session:
        cate = request.args.get('cate')
        product_list = db.select_all_cate_merchandise(cate)
        return render_template('admin_list.html', product_list=product_list)
    else:
        return redirect(url_for('index'))

@app.route('/search_admin', methods=['POST'])
def search_admin():
    if 'user' in session:
        key = request.form.get('search')
        product_list = db.select_all_search_merchandise(key)
        return render_template('admin_list.html', product_list=product_list)
    else:
        return redirect(url_for('index'))
    
@app.route('/delete_exe', methods=['POST'])
def delete_exe():
    if 'user' in session:
        db.delete_merchandise(request.args.get('name'))
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)
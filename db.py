import os, psycopg2, string, hashlib, random

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits
    
    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password


def insert_user(user_name, mail, password):
    sql = 'INSERT INTO shopping_user VALUES (default, %s, %s, %s, %s)'
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    try: 
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name, mail, hashed_password, salt))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError: 
        count=0
    finally:
        cursor.close()
        connection.close()
        
    return count

def login(mail, password):
    sql = 'SELECT hashed_password, salt FROM shopping_user WHERE mail ~ %s'
    flg = False
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (mail,))
        user = cursor.fetchone()
        
        if user != None:
            salt = user[1]
            
            hashed_password = get_hash(password, salt)
            
            if hashed_password == user[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
    
    return flg

def register_merchandise(name, price, cate):
    sql = 'INSERT INTO shopping_merchandise VALUES (default, %s, %s, %s)'
    try: 
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (name, price, cate))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError: 
        count=0
    finally:
        cursor.close()
        connection.close()
        
    return count

def select_all_merchandise():
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "SELECT * FROM shopping_merchandise"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def select_all_cate_merchandise(category):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "SELECT * FROM shopping_merchandise where category = %s"
    
    cursor.execute(sql, (category,))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def select_all_search_merchandise(key):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "SELECT * FROM shopping_merchandise where name like %s"
    key = '%' + key + '%'
    cursor.execute(sql, (key,))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def insert_book(title, author, publisher, pages):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "INSERT INTO books_sample VALUES(default, %s, %s, %s, %s)"
    cursor.execute(sql, (title, author, publisher, pages))
    
    connection.commit()
    
    cursor.close()
    connection.close()
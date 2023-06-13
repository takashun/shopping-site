import os
import psycopg2

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def select_all_merchandise():
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "SELECT title, author, publisher, pages FROM merchandise"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def select_all_search_merchandise(category):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "SELECT title, author, publisher, pages FROM merchandise where = %s"
    
    cursor.execute(sql, (category,))
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
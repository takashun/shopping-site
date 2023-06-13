from flask import Blueprint, render_template

book_bp = Blueprint('book', __name__, url_prefix='/book')

@book_bp.route('list')
def book_list():
    return render_template('list.html')
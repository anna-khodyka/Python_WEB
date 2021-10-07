import pathlib
from datetime import datetime
from flask import Flask

from classbook import *
from model import *
from notes_book import *

from db_classes import *
from clean import *
from error_handler import error_handler
import contact_bp
# from view import *

app = Flask(__name__)
# model = Model()
# view = ConsoleView()
app.register_blueprint(contact_bp.contact_bp)

# @app.route('/')
# def show():
#     # number = view.enter_number_of_page()
#     number = 5
#     records_list = model.book.return_all_records()
#     iter = model.book.iterator(records_list, number)
#     result = ""
#     for i in iter:
#         result += i
#     result += "The end of the contacts book"
#     return result

# for i in iter:
#     view.show_one_page_of_addressbook(i)
# view.notify_of_message("The end of the contacts book")

# @error_handler


def main():
    app.run()


if __name__ == '__main__':
    main()

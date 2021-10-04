from classbook import *
from model import *
from notes_book import *
from clean import *
from controller import *
from error_handler import error_handler
from view import *


# @error_handler
def main():
    controller = Controller()
    view = ConsoleView()
    controller.view = view
    view.greete()
    # выполнение основных комманд HELPER-a
    while view.esc_e:
        user_inpu = view.choose_command()
        result = controller.handler(user_inpu)
        if result:
            print(result)
        elif result == None:
            pass
        else:
            break


if __name__ == '__main__':
    main()

import tkinter as tk
from model import MarketsModel
from view import MarketsView
from controller import MarketsController


def main():
    root = tk.Tk()

    model = MarketsModel()
    view = MarketsView(root)
    controller = MarketsController(model, view)

    # Установка контроллера для view и model
    view.set_controller(controller)
    model.set_controller(controller)

    controller.run()


if __name__ == '__main__':
    main()

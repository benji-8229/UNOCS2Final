from logic import *


def main():
    application = QApplication([])

    # Need to explicitly pass window size to Logic class in order to position widgets that are relative to the window size
    # No matter what order setFixedSize and window.geometry.width() are called in, the latter is not updated
    # from the default until after the application is exec'd
    # When doing this we might as well call setFixedWidth and setFixedHeight from inside Logic class
    window = Logic(600, 300)
    window.setWindowTitle("Greenhouse Control")
    window.show()
    application.exec()


if __name__ == "__main__":
    main()

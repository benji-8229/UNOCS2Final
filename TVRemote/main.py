from logic import *


def main():
    application = QApplication([])
    # Same as with the other project, it makes sense for dynamic placement to pass in
    # our width / height and set the window size inside Logic
    remote = Logic(225, 250)
    remote.setWindowTitle("TV Remote")
    remote.show()
    application.exec()


if __name__ == "__main__":
    main()

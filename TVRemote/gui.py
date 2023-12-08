from PyQt6 import QtWidgets, QtCore, QtGui


class RemoteGUI:
    """
    Main gui for the remote control of our TV. Includes multiple decorative
    buttons alongside the functional buttons. Will still control and update
    the state of the TV even if the window is closed.
    """

    __main_font = QtGui.QFont("Times", 11)

    def __init__(self):
        """
        Initialize empty variables (mainly for IDE hinting / silencing warnings)
        """

        self.power_button = None
        self.new_tv_button = None
        self.channel_up_button = None
        self.channel_down_button = None
        self.volume_up_button = None
        self.volume_down_button = None
        self.mute_button = None

    def setupUI(self, main_window: QtWidgets.QMainWindow, width: int, height: int) -> None:
        """
        Initializes our push buttons into the main_window and dynamically spaces them based
        off the dimensions given
        :param main_window: QMainWindow object
        :param width: Declared window width
        :param height: Declared window height
        :return: None
        """

        main_window.setStyleSheet("background-color: dimgray;")

        self.power_button = QtWidgets.QPushButton("POWER", main_window)
        self.power_button.setFixedSize(75, 25)

        self.new_tv_button = QtWidgets.QPushButton("NEW TV", main_window)
        self.new_tv_button.move(width - 75, 0)
        self.new_tv_button.setFixedSize(75, 25)

        self.channel_up_button = QtWidgets.QPushButton("↑", main_window)
        self.channel_up_button.setFixedSize(50, 50)
        self.channel_up_button.move(width // 2 - 25, 50)

        # Non-functional buttons just for decor
        select = QtWidgets.QPushButton("O", main_window)
        select.setFixedSize(50, 50)
        select.move(width // 2 - 25, 105)

        left = QtWidgets.QPushButton("←", main_window)
        left.setFixedSize(50, 50)
        left.move(width // 2 - 80, 105)

        right = QtWidgets.QPushButton("→", main_window)
        right.setFixedSize(50, 50)
        right.move(width // 2 + 30, 105)

        self.channel_down_button = QtWidgets.QPushButton("↓", main_window)
        self.channel_down_button.setFixedSize(50, 50)
        self.channel_down_button.move(width // 2 - 25, 160)

        self.volume_up_button = QtWidgets.QPushButton("↑", main_window)
        self.volume_up_button.setFixedSize(20, 50)
        self.volume_up_button.move(width - 20, 80)

        self.volume_down_button = QtWidgets.QPushButton("↓", main_window)
        self.volume_down_button.setFixedSize(20, 50)
        self.volume_down_button.move(width - 20, 130)

        self.mute_button = QtWidgets.QPushButton("x", main_window)
        self.mute_button.setFixedSize(20, 20)
        self.mute_button.move(width - 20, 180)

        # Adding all our buttons to a list in order to do identical formatting to all of them cleanly
        buttons = [self.power_button, self.new_tv_button, self.channel_up_button, self.channel_down_button,
                   left, select, right, self.volume_up_button, self.volume_down_button, self.mute_button]
        for button in buttons:
            if button:
                button.setFont(RemoteGUI.__main_font)
                button.setStyleSheet("background-color: grey;")


class TvWindow(QtWidgets.QWidget):
    """
    TvWindow object that will display the state of our TV that we control with our remote.
    Will automatically update on button presses, as well as import the tv state when initialized
    """

    __main_font = QtGui.QFont("Times", 13)

    def __init__(self):
        """
        Initializes empty variables for IDE hinting and warning suppression, as well as initializing superclass
        """

        super().__init__()
        self.volume_label = None
        self.channel_label = None
        self.power_label = None

    def setupUI(self, width: int) -> None:
        """
        Initializes, dynamically places, and styles labels
        :param width: TV window width
        :return: None
        """

        self.power_label = QtWidgets.QLabel("OFF", self)
        self.power_label.setFixedWidth(100)
        self.power_label.move(width // 2 - 50, 0)
        self.power_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.power_label.setFont(TvWindow.__main_font)
        self.power_label.setStyleSheet("color: yellow;")

        self.channel_label = QtWidgets.QLabel("CHANNEL", self)
        self.channel_label.setFixedWidth(150)
        self.channel_label.move(3, 0)
        self.channel_label.setFont(TvWindow.__main_font)
        self.channel_label.setStyleSheet("color: yellow;")

        self.volume_label = QtWidgets.QLabel("VOLUME", self)
        self.volume_label.setFixedWidth(100)
        self.volume_label.move(width - 103, 0)
        self.volume_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.volume_label.setFont(TvWindow.__main_font)
        self.volume_label.setStyleSheet("color: yellow;")

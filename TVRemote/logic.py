from gui import *
from PyQt6.QtWidgets import *


class Logic(QMainWindow, RemoteGUI):
    """
    Logic controller for our remote and TV windows. Mostly the Television class for
    Lab 12 plus the necessary code for the MVC framework.
    """

    __MIN_VOLUME = 0
    __MAX_VOLUME = 10
    __CHANNELS = [{"channel": "Fox", "color": "dodgerblue"},
                  {"channel": "CNN", "color": "indianred"},
                  {"channel": "ESPN", "color": "green"},
                  {"channel": "HISTORY", "color": "teal"},
                  {"channel": "CN", "color": "slateblue"},
                  {"channel": "DISCOVERY", "color": "purple"},
                  {"channel": "PBS", "color": "darkmagenta"}]
    __MIN_CHANNEL = 0
    __MAX_CHANNEL = len(__CHANNELS) - 1

    def __init__(self, width: int, height: int):
        """
        Constructor for our Logic controller, creates initial TV object and does setup
        :param width: window width
        :param height: window height
        """

        super().__init__()

        self.__status = False
        self.__muted = False
        self.__volume = Logic.__MIN_VOLUME
        self.__channel = Logic.__MIN_CHANNEL
        self.__prev_volume = self.__volume

        self.setupUI(self, width, height)
        self.setFixedSize(width, height)

        self.TV = TvWindow()
        self.TV.setFixedSize(400, 400)
        self.TV.setupUI(400)
        self.TV.setWindowTitle("TV")
        self.__tv_refresh_state()
        self.TV.show()

        self.__bindings()

    def __bindings(self) -> None:
        """
        Binds our gui buttons to the functions in this class after they've been created
        :return: None
        """

        self.power_button.clicked.connect(self.__power)
        self.channel_up_button.clicked.connect(self.__channel_up)
        self.channel_down_button.clicked.connect(self.__channel_down)
        self.new_tv_button.clicked.connect(self.__new_tv)
        self.volume_down_button.clicked.connect(self.__volume_down)
        self.volume_up_button.clicked.connect(self.__volume_up)
        self.mute_button.clicked.connect(self.__mute)

    def __power(self) -> None:
        """
        Toggles the power state of the TV and refreshes our gui after
        :return: None
        """

        if self.__status:
            self.__status = False
        else:
            self.__status = True

        self.__tv_refresh_state()

    def __mute(self) -> None:
        """
        Toggles the mute status of the TV. Does nothing if TV is off and returns volume
        to previous value if unmuting, and finally refreshes TV gui.
        :return: None
        """

        if not self.__status:
            return

        if self.__muted:
            self.__muted = False
            self.__volume = self.__prev_volume
        else:
            self.__prev_volume = self.__volume
            self.__volume = 0
            self.__muted = True

        self.__tv_refresh_state()

    def __channel_up(self) -> None:
        """
        Increases channel of our TV. Does nothing if powered off, increases
        channel by one otherwise and refreshes TV gui. Will loop back to the
        minimum channel if we exceed our max channel.
        :return: None
        """

        if not self.__status:
            return

        self.__channel += 1
        if self.__channel > Logic.__MAX_CHANNEL:
            self.__channel = Logic.__MIN_CHANNEL

        self.__tv_refresh_state()

    def __channel_down(self) -> None:
        """
        Decreases channel of our TV. Does nothing if powered off, decreases
        channel by one otherwise and refreshes TV gui. Will loop back to the
        maximum channel if we go lower than our minimum channel.
        :return: None
        """

        if not self.__status:
            return

        self.__channel -= 1
        if self.__channel < Logic.__MIN_CHANNEL:
            self.__channel = Logic.__MAX_CHANNEL

        self.__tv_refresh_state()

    def __volume_up(self) -> None:
        """
        Increases volume of our TV. Does nothing if powered off, increases
        volume by one otherwise and refreshes TV gui. Will not exceed maximum
        volume setting.
        :return: None
        """

        if not self.__status:
            return

        if self.__muted:
            self.__mute()
        if self.__volume == Logic.__MAX_VOLUME:
            return

        self.__volume += 1

        self.__tv_refresh_state()

    def __volume_down(self) -> None:
        """
        Decreases volume of our TV. Does nothing if powered off, decreases
        volume by one otherwise and refreshes TV gui. Will not go past minimum
        volume setting.
        :return: None
        """

        if not self.__status:
            return

        if self.__muted:
            self.__mute()
        if self.__volume == Logic.__MIN_VOLUME:
            return

        self.__volume -= 1

        self.__tv_refresh_state()

    def __tv_set_color(self, svg_color: str) -> None:
        """
        Sets the background color of our tv, used for graphic when
        swapping channel and turning off TV
        :param svg_color: a color string as defined here https://www.w3.org/TR/SVG11/types.html#ColorKeywords
        :return: None
        """

        # Make sure we have a TV available to set the color to
        if not self.TV:
            return

        self.TV.setStyleSheet(f"background-color: {svg_color}")

    def __tv_refresh_state(self) -> None:
        """
        Refreshes the state of the TV based on the state of this class. Called in every
        function that changes the state of the tv (volume up/down, channel up/down, etc)
        :return: None
        """

        if self.__status:
            self.__tv_set_color(Logic.__CHANNELS[self.__channel]["color"])
        else:
            self.__tv_set_color("black")

        self.TV.power_label.setText(f"POWER\n{'ON' if self.__status else 'OFF'}")
        self.TV.volume_label.setText(f"VOLUME\n{'MUTED' if self.__muted else f'{self.__volume}/{Logic.__MAX_VOLUME}'}")
        self.TV.channel_label.setText(f"CHANNEL\n{self.__channel} - {Logic.__CHANNELS[self.__channel]['channel']}")

    def __new_tv(self) -> None:
        """
        Callback function for our new TV button, used to instantiate a new TV
        window in the event the initial one is closed
        :return: None
        """

        self.TV = TvWindow()
        self.TV.setFixedSize(400, 400)
        self.TV.setWindowTitle("TV")
        self.TV.setupUI(400)
        self.__tv_refresh_state()
        self.TV.show()

    def closeEvent(self, event) -> None:
        """
        Callback event for when a window is closed. Used to clean up the self.TV object
        in case that window is closed
        :param event: internal event used by PyQt6
        :return: None
        """

        # Prevent exception for sake of graceful exit in case we
        # close the remote window while the tv window is closed
        if self.TV:
            self.TV.close()
            self.TV = None
        self.close()

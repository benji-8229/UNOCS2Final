from PyQt6 import QtWidgets, QtCore, QtGui


class GreenhouseGUI:
    """
    GUI controller for greenhouse control unit. Controls creation of labels, text fields, buttons, and dynamically placing them.
    """

    __small_font = QtGui.QFont("Times", 9)
    __default_field_height = 24
    __default_field_width = 100

    def __init__(self):
        """
        Initialize empty variables (mainly for IDE hinting / silencing warnings)
        """

        self.humidity_field = None
        self.temp_field = None
        self.temp_f_button = None
        self.temp_c_button = None
        self.temp_unit_button_group = None
        self.co2_field = None

        self.light_button = None
        self.light_on_field = None
        self.light_off_field = None
        self.photo_button = None
        self.photo_field = None

        self.submit_button = None
        self.submit_label = None

    def setupUI(self, main_window: QtWidgets.QMainWindow, width: int, height: int) -> None:
        """
        Generates the unpopulated labels and buttons based on screen geometry, as well as
        setting up UI groups and other initialization logic
        :param main_window: Main QMainWindow object
        :param width: Our declared width
        :param height: Our declared height
        :return: None
        """

        main_window.setStyleSheet("background-color: lavender;")

        # ------------- Top line of gui labels / fields / buttons -------------
        side_offset = int(width / 12) * 2
        top_offset = int(height / 8)

        __, self.humidity_field = self.__create_label_field(main_window, "% Relative Humidity", side_offset, top_offset)  # Starts at side_offset and spans to 150
        __, self.temp_field = self.__create_label_field(main_window, "Temperature", int(width / 2) - 50, top_offset)  # Centered to screen
        __, self.co2_field = self.__create_label_field(main_window, "Co2 PPM", width - 100 - side_offset, top_offset)  # Mirrors first label

        # Create buttons for temperature and add them to a group to make them mutually exclusive and seperated from our other buttons
        self.temp_c_button = QtWidgets.QRadioButton("C", main_window)
        self.temp_c_button.move(int(width / 2) - 50, top_offset + 25)
        self.temp_c_button.setMaximumSize(50, 20)
        self.temp_f_button = QtWidgets.QRadioButton("F", main_window)
        self.temp_f_button.move(int(width / 2) + 25, top_offset + 25)
        self.temp_f_button.setMaximumSize(50, 20)
        self.temp_unit_button_group = QtWidgets.QButtonGroup(main_window)
        self.temp_unit_button_group.addButton(self.temp_c_button)
        self.temp_unit_button_group.addButton(self.temp_f_button)

        # ------------- Bottom line of gui labels / fields / buttons -------------
        side_offset = int(width / 6)
        top_offset = int(height / 3)

        # Light labels, fields, and button
        self.light_button = QtWidgets.QRadioButton("Automatic Lights", main_window)
        self.light_button.setFixedWidth(200)
        self.light_button.move(side_offset, top_offset)
        self.light_button.setAutoExclusive(False)
        self.light_on_field = self.__create_label_field_side(main_window, "Light On Time", side_offset, top_offset)
        self.light_off_field = self.__create_label_field_side(main_window, "Light Off Time", side_offset, top_offset + int(GreenhouseGUI.__default_field_height * 1.1))

        # Photo labels, fields, and button
        # Start position for these will be the length from top of screen to bottom of our light settings + 20%
        top_offset_photos = int((top_offset + GreenhouseGUI.__default_field_height * 1.1 + 33) * 1.2)
        self.photo_button = QtWidgets.QRadioButton("Automatic Photos", main_window)
        self.photo_button.move(side_offset, top_offset_photos)
        self.photo_button.setFixedWidth(200)
        self.photo_field = self.__create_label_field_side(main_window, "Photo Timer", side_offset, top_offset_photos)

        # Submit button + information label
        self.submit_label = QtWidgets.QLabel("Please enter new values for greenhouse control", main_window)
        self.submit_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.submit_label.move(int(side_offset * 3.5), top_offset + 7)
        self.submit_label.setFixedSize(side_offset * 2, int(top_offset * 2))
        self.submit_label.setWordWrap(True)
        self.submit_button = QtWidgets.QPushButton("Submit", main_window)
        self.submit_button.move(side_offset * 4, top_offset_photos + 27)
        self.submit_button.setDisabled(False)

    @staticmethod
    def __create_label_field(window: QtWidgets.QMainWindow, label_text: str, x: int, y: int, width: int = __default_field_width, height: int = __default_field_height) -> tuple:
        """
        Generates a line edit field with label centered above
        :param window: Window to parent widgets to
        :param label_text: Text to be above field
        :param x: X position of line edit field
        :param y: Y position of line edit field
        :param width: Width of line edit field
        :param height: Height of line edit field
        :return: Tuple of (label_obj, field_obj)
        """

        label = QtWidgets.QLabel(label_text, window)
        label.setFont(GreenhouseGUI.__small_font)
        # Add some padding to label so text is not cut off by moving
        # label left 25 units, add 50 units to width, and center.
        label.move(x-25, y-height)
        label.setFixedSize(width+50, height)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        field = QtWidgets.QLineEdit(window)
        field.move(x, y)
        field.setFixedSize(width, height)
        field.setFont(GreenhouseGUI.__small_font)

        return label, field

    @staticmethod
    def __create_label_field_side(window: QtWidgets.QMainWindow, label_text: str, x: int, y: int) -> QtWidgets.QLineEdit:
        """
        Generates a field with a label to its right. Used for the second line of our gui
        :param window: Window to parent widgets to
        :param label_text: Text to be to the right of field
        :param x: X position of line edit field
        :param y: Y position of line edit field
        :return:
        """

        return_field = QtWidgets.QLineEdit(window)
        return_field.setFixedSize(75, GreenhouseGUI.__default_field_height)
        return_field.move(x, y + 30)
        return_field.setEnabled(False)

        tmp_label = QtWidgets.QLabel(label_text, window)
        tmp_label.move(x + 80, y + 33)
        tmp_label.setFixedHeight(GreenhouseGUI.__default_field_height)
        tmp_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        return return_field

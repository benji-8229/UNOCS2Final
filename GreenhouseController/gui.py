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

        self.window = None

        self.humidity_field = None
        self.temp_field = None
        self.temp_f_button = None
        self.temp_c_button = None
        self.unit_button_group = None
        self.co2_field = None

        self.light_button = None
        self.light_on_field = None
        self.light_off_field = None
        self.photo_button = None
        self.photo_field = None

        self.submit_button = None
        self.submit_label = None

    def setupUI(self, main_window: QtWidgets.QMainWindow, dec_width: int, dec_height: int) -> None:
        """
        Generates the unpopulated labels and buttons based on screen geometry, as well as
        setting up UI groups and other initialization logic
        :param main_window: Main QMainWindow object
        :param dec_width: Our expliclity declared width
        :param dec_height: Our explicitly declared height
        :return: None
        """

        self.window = main_window

        # ------------- Top line of gui labels / fields / buttons -------------
        side_offset = int(dec_width / 12) * 2
        top_offset = int(dec_height / 8)
        # Starts at side_offset and spans to 150
        __, self.humidity_field = self.create_label_field("% Relative Humidity", side_offset, top_offset)
        # Starts at center of screen - half the width of this field, spans to center of screen + half the width of label (perfectly centered)
        __, self.temp_field = self.create_label_field("Temperature", int(dec_width / 2) - 50, top_offset)
        # Starts at end of screen - (width of label + 50), spans to end of screen - side_offset (mirroring first label)
        __, self.co2_field = self.create_label_field("Co2 PPM", dec_width - 100 - side_offset, top_offset)
        # Create buttons for temperature and add them to a group to make them mutually exclusive and seperated from our other buttons
        self.temp_c_button = QtWidgets.QRadioButton("C", self.window)
        self.temp_c_button.move(int(dec_width / 2) - 50, top_offset + 20)
        self.temp_f_button = QtWidgets.QRadioButton("F", self.window)
        self.temp_f_button.move(int(dec_width / 2) + 25, top_offset + 20)
        self.unit_button_group = QtWidgets.QButtonGroup(self.window)
        self.unit_button_group.addButton(self.temp_c_button)
        self.unit_button_group.addButton(self.temp_f_button)

        # ------------- Bottom line of gui labels / fields / buttons -------------
        side_offset = int(dec_width / 6)
        top_offset = int(dec_height / 3)
        # Light labels, fields, and button
        self.light_button = QtWidgets.QRadioButton("Automatic Lights", self.window)
        self.light_button.setFixedWidth(200)
        self.light_button.move(side_offset, top_offset)
        self.light_button.setAutoExclusive(False)
        self.light_on_field = self.create_label_field_side("Light On Time", side_offset, top_offset)
        self.light_off_field = self.create_label_field_side("Light Off Time", side_offset, top_offset + int(GreenhouseGUI.__default_field_height * 1.1))
        # Photo gui
        # Start position will be 1.2 * the end position of our light settings
        top_offset_photos = int((top_offset + GreenhouseGUI.__default_field_height * 1.1 + 33) * 1.2)
        self.photo_button = QtWidgets.QRadioButton("Automatic Photos", self.window)
        self.photo_button.move(side_offset, top_offset_photos)
        self.photo_button.setFixedWidth(200)
        self.photo_field = self.create_label_field_side("Photo Timer", side_offset, top_offset_photos)
        # Submit button
        self.submit_label = QtWidgets.QLabel("Please enter new values for greenhouse control", self.window)
        self.submit_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.submit_label.move(int(side_offset * 3.5), top_offset + 7)
        self.submit_label.setFixedSize(side_offset * 2, int(top_offset * 2))
        self.submit_label.setWordWrap(True)
        self.submit_button = QtWidgets.QPushButton("Submit", self.window)
        self.submit_button.move(side_offset * 4, top_offset_photos + 27)
        self.submit_button.setDisabled(False)

    def create_label_field(self, label_text: str, x: int, y: int, width: int = __default_field_width, height: int = __default_field_height) -> tuple:
        """
        Generates a line edit field with label centered above
        :param label_text: Text to be above field
        :param x: X position of line edit field
        :param y: Y position of line edit field
        :param width: Width of line edit field
        :param height: Height of line edit field
        :return: Tuple of (label_obj, field_obj)
        """

        label = QtWidgets.QLabel(label_text, self.window)
        label.setFont(GreenhouseGUI.__small_font)
        # Add some padding to label so text is not cut off by moving
        # label left 25 units, add 50 units to width, and center.
        label.move(x-25, y-height)
        label.setFixedSize(width+50, height)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        field = QtWidgets.QLineEdit(self.window)
        field.move(x, y)
        field.setFixedSize(width, height)
        field.setFont(GreenhouseGUI.__small_font)

        return label, field

    def create_label_field_side(self, label_text: str, x: int, y: int) -> QtWidgets.QLineEdit:
        """
        Generates a field with a label to its right. Used for the second line of our gui
        :param label_text: Text to be to the right of field
        :param x: X position of line edit field
        :param y: Y position of line edit field
        :return:
        """

        return_field = QtWidgets.QLineEdit(self.window)
        return_field.setFixedSize(75, GreenhouseGUI.__default_field_height)
        return_field.move(x, y + 30)
        return_field.setEnabled(False)

        tmp_label = QtWidgets.QLabel(label_text, self.window)
        tmp_label.move(x + 80, y + 33)
        tmp_label.setFixedHeight(GreenhouseGUI.__default_field_height)
        tmp_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        return return_field

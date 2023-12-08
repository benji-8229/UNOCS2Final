import json
from gui import *
from PyQt6.QtWidgets import *


class Logic(QMainWindow, GreenhouseGUI):
    """
    The Logic class is responsible for generating values, converting units, reading and writing
    files, validating input, and beginning UI initialization.
    """

    __start_dict = {"humidity": 0.0,
                    "co2": 0,
                    "temp": {"degrees": 0.0, "unit": "f"},
                    "light": {"enabled": False, "on_time": 0.0, "off_time": 0.0},
                    "photo": {"enabled": False, "timer": 0.0}}

    def __init__(self, width, height):
        """
        :param width: Target application width
        :param height: Target application height
        """

        super().__init__()

        self.__current_unit = None

        # At this point window.geometry.getWidth() would not return dec_width, therefore to position
        # labels relative to window edge we pass these values in explicitly
        self.setupUI(self, width, height)
        self.setFixedSize(width, height)

        # Try and read settings file, handling empty / corruption
        with open("settings.json", "a+", encoding='utf-8') as settings:
            settings.seek(0)
            settings.flush()
            file_contents = settings.read()

            try:
                self.data = json.loads(file_contents, strict=False)
            except json.JSONDecodeError as e:  # Empty / corrupted json, wipe file and rewrite our template
                settings.seek(0)
                settings.truncate(0)
                json.dump(Logic.__start_dict, settings, indent=4)
                self.data = Logic.__start_dict

        self.__bindings_and_population()

    def __bindings_and_population(self) -> None:
        """
        Binds buttons to functions in Logic and populates fields from settings.json
        :return: None
        """

        # Populate humidity field
        self.humidity_field.setText(self.__clean_float(self.data["humidity"]))

        # Populate temperature fields
        self.temp_field.setText(self.__clean_float(self.data["temp"]["degrees"]))
        if self.data["temp"]["unit"] == "c":
            self.temp_c_button.setChecked(True)
            self.__current_unit = "c"
        else:
            self.temp_f_button.setChecked(True)
            self.__current_unit = "f"

        # Populate Co2 fields
        self.co2_field.setText(str(self.data["co2"]))

        # Populate light fields
        if self.data["light"]["enabled"]:
            self.light_button.setChecked(True)
            self.light_on_field.setEnabled(True)
            self.light_off_field.setEnabled(True)
        self.light_on_field.setText(self.__clean_float(self.data["light"]["on_time"]))
        self.light_off_field.setText(self.__clean_float(self.data["light"]["off_time"]))

        # Populate photo fields
        if self.data["photo"]["enabled"]:
            self.photo_button.setChecked(True)
            self.photo_field.setEnabled(True)
        self.photo_field.setText(self.__clean_float(self.data["photo"]["timer"]))
        self.submit_button.setEnabled(True)

        # Button bindings
        self.temp_c_button.clicked.connect(self.__button_use_c)
        self.temp_f_button.clicked.connect(self.__button_use_f)
        self.light_button.clicked.connect(self.__lights_clicked)
        self.photo_button.clicked.connect(self.__photo_clicked)
        self.submit_button.clicked.connect(self.__submit_clicked)

    def __button_use_f(self) -> None:
        """
        Handles swapping from C to F by changing the current internal unit and converting the value in our field
        :return: None
        """

        # Necessary to prevent clicking the already selected button
        if self.__current_unit == "f":
            return

        try:
            c_temp = float(self.temp_field.text())
        except ValueError:
            return

        self.__current_unit = "f"
        self.temp_field.setText(f"{Logic.__clean_float(c_temp * 9 / 5 + 32)}")  # Necessary to remove trailing 0's / decimal

    def __button_use_c(self) -> None:
        """
        Handles swapping from C to F by changing the current internal unit and converting the value in our field
        :return: None
        """

        # Necessary to prevent clicking the already selected button
        if self.__current_unit == "c":
            return

        try:
            c_temp = float(self.temp_field.text())
        except ValueError:
            return

        self.__current_unit = "c"
        self.temp_field.setText(f"{Logic.__clean_float((c_temp - 32) * 5 / 9)}")  # Necessary to remove trailing 0's / decimal

    def __lights_clicked(self) -> None:
        """
        Handle enabling / disable fields when the radio button to enable lights is toggled
        :return: None
        """

        if self.light_button.isChecked():
            self.light_on_field.setEnabled(True)
            self.light_off_field.setEnabled(True)
        else:
            self.light_on_field.setEnabled(False)
            self.light_off_field.setEnabled(False)

    def __photo_clicked(self) -> None:
        """
        Handle enabling / disable fields when the radio button to enable lights is toggled
        :return: None
        """

        if self.photo_button.isChecked():
            self.photo_field.setEnabled(True)
        else:
            self.photo_field.setEnabled(False)

    def __submit_clicked(self) -> None:
        """
        Validates all values inside fields, cleans them up, and submits them to settings.json
        :return: None
        """

        try:
            # Try and convert all our values. Only real invalid inputs here would be
            # strings, which would then throw a value error.
            self.data["humidity"] = float(self.humidity_field.text())
            self.data["co2"] = int(self.co2_field.text())
            self.data["temp"]["degrees"] = round(float(self.temp_field.text()), 3)
            self.data["temp"]["unit"] = self.__current_unit
            self.data["light"]["enabled"] = self.light_button.isChecked()
            self.data["light"]["on_time"] = round(float(self.light_on_field.text()), 3)
            self.data["light"]["off_time"] = round(float(self.light_off_field.text()), 3)
            self.data["photo"]["enabled"] = self.photo_button.isChecked()
            self.data["photo"]["timer"] = round(float(self.photo_field.text()), 3)
        except ValueError:
            self.submit_label.setText("Incorrect values provided. Please enter all values as integers or floats (i.e \"30\" rather than \"30 minutes\")")
            return

        if self.data["humidity"] < 0 or self.data["humidity"] > 100:
            self.submit_label.setText("Please submit relative humidity value as a number between 0 and 100")
            return
        elif self.data["co2"] < 0:
            self.submit_label.setText("Please submit a Co2 PPM value greater than 0")
            return
        elif self.data["light"]["on_time"] < 0 or self.data["light"]["off_time"] < 0 or self.data["photo"]["timer"] < 0:
            self.submit_label.setText("Please enter time values greater than 0")
            return

        # Overwrite settings file with new data
        with open("settings.json", "w", encoding='utf-8') as settings:
            json.dump(self.data, settings, indent=4)

        self.submit_label.setText("Greenhouse settings have been successfully updated")

    @staticmethod
    def __clean_float(n: float) -> str:
        """
        Cleans a float by rounding to 2 digits and removing trailing 0's or decimals
        :param n: Float to clean
        :return: str
        """

        # Check if float, int, or valid float-like string
        try:
            float(n)
        except ValueError:
            raise ValueError("n given was not numerical or float-like string")

        return f"{round(n, 2) + 0}".rstrip('0').rstrip('.')

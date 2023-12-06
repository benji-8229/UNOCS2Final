import json
from gui import *
from PyQt6.QtWidgets import *
from pathlib import Path


class Logic(QMainWindow, GreenhouseGUI):
    """
    Logic class responsible for generating values, converting units, reading and writing
    files, and beginning UI initialization.
    """

    start_dict = {"prh": 0.0,
                  "co2": 0,
                  "temp": {"degrees": 0.0, "unit": "f"},
                  "light": {"enabled": False, "on_time": 0.0, "off_time": 0.0},
                  "photo": {"enabled": False, "timer": 0.0}}

    def __init__(self, dec_width, dec_height):
        """
        :param dec_width: Target application width
        :param dec_height: Target application height
        """
        super().__init__()

        self.current_unit = None

        self.setFixedWidth(dec_width)
        self.setFixedHeight(dec_height)

        # At this point window.geometry.getWidth() would return 640 no matter dec_width, therefore to position
        # labels relative to window edge we pass these values in explicitly
        self.setupUI(self, dec_width, dec_height)

        # Try and read settings file, handling empty / corruption
        with open("settings.json", "a+", encoding='utf-8') as settings:
            settings.seek(0)
            settings.flush()
            file_contents = settings.read()

            try:
                self.data = json.loads(file_contents, strict=False)
            except json.JSONDecodeError as e:  # Empty / corrupted json, wipe file and rewrite our template
                settings.seek(0)
                settings.truncate()
                json.dump(Logic.start_dict, settings, indent=4)
                self.data = Logic.start_dict

        self.bindings_and_population()

    def bindings_and_population(self):
        # Populate fields with previous values
        self.humidity_field.setText(str(self.data["prh"]))
        self.temp_field.setText(str(self.data["temp"]["degrees"]))
        if self.data["temp"]["unit"] == "c":
            self.temp_c_button.setChecked(True)
            self.current_unit = "c"
        else:
            self.temp_f_button.setChecked(True)
            self.current_unit = "f"
        self.co2_field.setText(str(self.data["co2"]))
        if self.data["light"]["enabled"]:
            self.light_button.setChecked(True)
            self.light_on_field.setEnabled(True)
            self.light_off_field.setEnabled(True)
        self.light_on_field.setText(str(self.data["light"]["on_time"]))
        self.light_off_field.setText(str(self.data["light"]["off_time"]))
        if self.data["photo"]["enabled"]:
            self.photo_button.setChecked(True)
            self.photo_field.setEnabled(True)
        self.photo_field.setText(str(self.data["photo"]["timer"]))
        self.submit_button.setEnabled(True)

        # Button bindings
        self.temp_c_button.clicked.connect(self.button_use_c)
        self.temp_f_button.clicked.connect(self.button_use_f)
        self.light_button.clicked.connect(self.lights_clicked)
        self.photo_button.clicked.connect(self.photo_clicked)
        self.submit_button.clicked.connect(self.submit_clicked)

    def button_use_f(self):
        if self.current_unit == "f":
            return

        try:
            c_temp = float(self.temp_field.text())
        except ValueError:
            return

        self.current_unit = "f"
        self.temp_field.setText(f"{Logic.clean_float(c_temp * 9/5 + 32)}")  # Necessary to remove trailing 0's / decimal

        # Sanity check to prevent -0
        if self.temp_field.text() == "-0":
            self.temp_field.setText("0")

    def button_use_c(self):
        if self.current_unit == "c":
            return

        try:
            c_temp = float(self.temp_field.text())
        except ValueError:
            return

        self.current_unit = "c"
        self.temp_field.setText(f"{Logic.clean_float((c_temp - 32) * 5/9)}")  # Necessary to remove trailing 0's / decimal

        # Sanity check to prevent -0
        if self.temp_field.text() == "-0":
            self.temp_field.setText("0")

    def lights_clicked(self):
        if self.light_button.isChecked():
            self.light_on_field.setEnabled(True)
            self.light_off_field.setEnabled(True)
        else:
            self.light_on_field.setEnabled(False)
            self.light_off_field.setEnabled(False)

    def photo_clicked(self):
        if self.photo_button.isChecked():
            self.photo_field.setEnabled(True)
        else:
            self.photo_field.setEnabled(False)

    def submit_clicked(self) -> None:
        """
        Validates all values inside fields, cleans them up, and submits them to settings.json
        :return: None
        """

        try:
            self.data["prh"] = float(self.humidity_field.text())
            self.data["co2"] = int(self.co2_field.text())
            self.data["temp"]["degrees"] = Logic.clean_float(self.temp_field.text())
            self.data["temp"]["unit"] = self.current_unit
            self.data["light"]["enabled"] = self.light_button.isChecked()
            self.data["light"]["on_time"] = Logic.clean_float(self.light_on_field.text())
            self.data["light"]["off_time"] = Logic.clean_float(self.light_off_field.text())
            self.data["photo"]["enabled"] = self.photo_button.isChecked()
            self.data["photo"]["timer"] = Logic.clean_float(self.photo_field.text())
        except ValueError:
            self.submit_label.setText("Incorrect values provided. Please enter all values as integers or floats (i.e \"30\" rather than \"30 minutes\")")
            return

        if self.data["prh"] < 0 or self.data["prh"] > 100:
            self.submit_label.setText("Please submit relative humidity value as a number between 0 and 100")
            return

        # Overwrite settings file with new data
        with open("settings.json", "w", encoding='utf-8') as settings:
            json.dump(self.data, settings, indent=4)

        self.submit_label.setText("Greenhouse settings have been successfully updated")

    @staticmethod
    def clean_float(n: float) -> float:
        """
        Cleans a float by rounding to 2 digits and removing trailing 0's or decimals
        :param n: Float to clean
        :return: float
        """

        # Check if float, int, or valid float-like string
        try:
            n = float(n)
        except ValueError:
            raise ValueError("n given was not numerical or float-like string")

        n = round(n, 2)  # Round 2 digits
        n = float(str(n).rstrip("0").rstrip("."))  # Converting to string and back to float is gross but actually the cleanest solution in this case

        return n
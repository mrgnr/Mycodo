# coding=utf-8
import copy

from mycodo.inputs.base_input import AbstractInput

measurements_dict = {
    0: {"measurement": "light_uv", "unit": "uv"},
    1: {"measurement": "light", "unit": "full"},
    2: {"measurement": "light_uvi", "unit": "uvi"},
    3: {"measurement": "light", "unit": "lux"},
}

# Input information
INPUT_INFORMATION = {
    "input_name_unique": "LTR390",
    "input_manufacturer": "Optoelectronics",
    "input_name": "LTR390",
    "input_library": "Adafruit-CircuitPython-LTR390",
    "measurements_name": "UV Light",
    "measurements_dict": measurements_dict,
    "url_manufacturer": "",
    "url_datasheet": "https://optoelectronics.liteon.com/upload/download/DS86-2015-0004/LTR-390UV_Final_%20DS_V1%201.pdf",
    "url_product_purchase": [
        "https://www.adafruit.com/product/4831",
        "https://shop.pimoroni.com/products/adafruit-ltr390-uv-light-sensor-stemma-qt-qwiic",
        "https://www.berrybase.de/sensoren-module/licht/adafruit-ltr390-uv-licht-sensor-stemma-qt/qwiic",
    ],
    "options_enabled": ["i2c_location", "period", "pre_output"],
    "options_disabled": ["interface"],
    "dependencies_module": [
        ("pip-pypi", "adafruit_extended_bus", "adafruit-extended-bus==1.0.1"),
        ("pip-pypi", "adafruit_ltr390", "adafruit-circuitpython-ltr390==1.1.1"),
    ],
    "interfaces": ["I2C"],
    "i2c_location": ["0x53"],
    "i2c_address_editable": False,
}


class InputModule(AbstractInput):
    """A sensor support class that monitors the LTR390's light"""

    def __init__(self, input_dev, testing=False):
        super(InputModule, self).__init__(input_dev, testing=testing, name=__name__)

        self.sensor = None

        if not testing:
            self.initialize_input()

    def initialize_input(self):
        import adafruit_ltr390
        from adafruit_extended_bus import ExtendedI2C

        self.sensor = adafruit_ltr390.LTR390(
            ExtendedI2C(self.input_dev.i2c_bus),
            address=int(str(self.input_dev.i2c_location), 16),
        )

    def get_measurement(self):
        """Gets the UV and ambient light"""
        if not self.sensor:
            self.logger.error("Input not set up")
            return

        self.return_dict = copy.deepcopy(measurements_dict)

        if self.is_enabled(0):
            self.value_set(0, self.sensor.uvs)

        if self.is_enabled(1):
            self.value_set(1, self.sensor.light)

        if self.is_enabled(2):
            self.value_set(2, self.sensor.uvi)

        if self.is_enabled(3):
            self.value_set(3, self.sensor.lux)

        return self.return_dict

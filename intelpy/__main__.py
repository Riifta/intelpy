#!/usr/bin/env python3
import sys
from intelpy import config
from intelpy.gui import mainwindow_intelpy
import intelpy.eve.evedata as evedata
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
import os
import intelpy.logging.logger

def main():
    app_name = "IntelPy"
    #os.path.dirname(__file__)
    script_dir = os.getcwd()
    resources_dir = os.path.join(script_dir, "intelpy", "resources")
    # Set the default configuration
    default_json = {
        "home_system": "1DQ1-A",
        "eve_log_location": "",
        "watched_channels": [
            "delve.imperium",
            "querious.imperium",
            "ftn.imperium",
            "vnl.imperium",
            "cr.imperium",
            "aridia.imperium",
            "khanid.imperium",
            "lone.imperium"
        ],
        "alert_jumps": 3,
        "alert_systems": [],
        "log_watch_active": 1,
        "config_loc": "",
        "alarm_sound": str(resources_dir) + os.sep + "alarm2.mp3",
        "display_alerts": 1,
        "display_clear": 1,
        "display_all": 1,
        "filter_status": 1,
        "filter_clear": 1,
        "debug": 0,
        "message_timeout": 1.0,
        "alert_timeout": 5,
        "dark_theme": 0
    }

    configuration = config.Config(app_name, default_json)
    configuration.value["config_loc"] = configuration.file_location

    # todo: remove this for release (set to 0)
    configuration.value["debug"] = 1

    if configuration.value["debug"]:
        logger = intelpy.logging.logger.logger(app_name)
        logger.write_log("== New instance of IntelPy Started ==")
        print("---- IntelPy ----")
        print("Debug enabled. See debug.log for output.")
        logger.write_log("Loading Eve data..")
    else:
        logger = None

    # Load eve data
    eve_data_file = str(resources_dir) + os.sep + "evedata.p"
    eve_systems = str(resources_dir) + os.sep + "systems.p"
    eve_idstosystems = str(resources_dir) + os.sep + "idtosystems.p"
    eve_data = evedata.EveData(eve_data_file, eve_systems, eve_idstosystems)

    if configuration.value["debug"]:
        logger.write_log("---- Configuration on loading ----")
        logger.write_log("eve_data_file: " + eve_data_file)
        logger.write_log("eve_systems: " + eve_systems)
        logger.write_log("eve_ids to systems: " + eve_idstosystems)
        #debug_config.debug_config(configuration)
        logger.debug_config(configuration)

    # Load main window GUI
    app = QApplication(sys.argv)

    # Nice dark theme if the user wishes to use it
    if 'dark_theme' not in configuration.value:
        configuration.value['dark_theme'] = 0
        configuration.flush_config_to_file()

    if configuration.value['dark_theme'] == 1:
        logger.write_log("Dark theme was enabled")
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)

    window = mainwindow_intelpy.MainWindow(configuration, eve_data, logger)
    window.show()
    app.exec_()

    if configuration.value["debug"]:
        logger.write_log("---- Configuration after closing ----")
        #debug_config.debug_config(configuration)
        logger.debug_config(configuration)
        logger.write_log("== This instance of IntelPy closed ==")

    # Flush configuration
    # todo: remove this for release (set to 0)
    configuration.value["debug"] = 0

    configuration.flush_config_to_file()
    window.stop_watchdog()

if __name__ == '__main__':
    main()



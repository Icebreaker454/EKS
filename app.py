# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QTextBrowser, QLabel,
    QDialog, QCheckBox, QComboBox)
from PyQt5.QtGui import *

from keyscraper import KeyScraper

from settings import s as KeyValue

EVALUATION_CHOICES = (
    'EAV',
    'ESS',
)


class SettingsForm(QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(SettingsForm, self).__init__(parent, *args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('Settings')
        self.setModal(True)

        self.resize(240, 120)

        label = QLabel('Old Style (Username/Password)?')
        old_checkbox = QCheckBox(
            checked=KeyValue.get('old_style'))
        label2 = QLabel('Evaluation Type')
        box = QComboBox()
        box.addItems(EVALUATION_CHOICES)
        index = box.findText(
            KeyValue.get('evaluation_type'),
            QtCore.Qt.MatchFixedString)
        if not index < 0:
            box.setCurrentIndex(index)
        ok_button = QPushButton('OK')
        ok_button.setFixedWidth(90)

        layout = QGridLayout()
        layout.addWidget(label, 1, 1)
        layout.addWidget(old_checkbox, 1, 2)
        layout.addWidget(label2, 2, 1)
        layout.addWidget(box, 2, 2)
        layout.addWidget(ok_button, 3, 1, 3, 2, QtCore.Qt.AlignCenter)

        old_checkbox.stateChanged.connect(
            lambda: self.set_old_style(old_checkbox))
        box.currentIndexChanged.connect(lambda: self.set_eval_type(box))
        ok_button.clicked.connect(self.close)

        self.setLayout(layout)

    def set_old_style(self, sender):
        KeyValue.set('old_style', sender.isChecked())

    def set_eval_type(self, sender):
        KeyValue.set('evaluation_type', sender.currentText())


class MainForm(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)

        self.resize(320, 360)

        self.setWindowIcon(QIcon('./assets/eset_logo.png'))
        self.setWindowTitle("ESET Key scraper")

        self.label = QLabel(
            "Keys for " + (KeyValue.get('evaluation_type') or 'EAV'))
        self.label.setFixedSize(100, 20)

        text_box = QTextBrowser()
        text_box.setFont(QFont('Ubuntu mono', 12))
        refresh_button = QPushButton("Refresh")
        refresh_button.setFixedHeight(40)
        settings_button = QPushButton()
        settings_button.setFixedSize(60, 40)
        settings_button.setIcon(QIcon('./assets/settings.png'))

        layout = QGridLayout()
        layout.addWidget(self.label, 1, 1, 1, 2)
        layout.addWidget(text_box, 2, 1, 1, 2)
        layout.addWidget(refresh_button, 3, 1)
        layout.addWidget(settings_button, 3, 2)

        refresh_button.clicked.connect(lambda: self.refresh(text_box))
        settings_button.clicked.connect(self.show_settings)

        self.setLayout(layout)
        self.refresh(text_box)

    def initialize_keyscraper(self):
        self.ks = KeyScraper(
            KeyValue.get('site_location') or 'http://trialeset.ru',
            KeyValue.get('evaluation_type') or 'EAV',
            KeyValue.get('old_style'))

    def refresh(self, sender):
        sender.clear()
        self.label.setText(
            "Keys for " + (KeyValue.get('evaluation_type') or 'EAV'))
        self.initialize_keyscraper()
        if KeyValue.get('old_style'):
            for x in self.ks.get_key():
                sender.append(str(x[0]) + ' pass: ' + str(x[1]))
            return
        for x in self.ks.get_key():
            sender.append(x)

    def show_settings(self):
        form = SettingsForm(self)
        form.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainForm()
    widget.show()
    app.exec_()
    KeyValue.dump()

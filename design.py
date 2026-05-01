# design.py
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Scroll Area
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 1180, 850))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1178, 848))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # ==================== SECTION AUDIO ====================
        self.groupBox_audio = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_audio.setGeometry(QtCore.QRect(20, 20, 550, 480))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.groupBox_audio.setFont(font)
        self.groupBox_audio.setObjectName("groupBox_audio")

        # Bouton charger audio
        self.btn_load_wav = QtWidgets.QPushButton(self.groupBox_audio)
        self.btn_load_wav.setGeometry(QtCore.QRect(20, 50, 200, 32))
        self.btn_load_wav.setObjectName("btn_load_wav")

        # Zone caractéristiques audio
        label_audio_features = QtWidgets.QLabel(self.groupBox_audio)
        label_audio_features.setGeometry(QtCore.QRect(20, 95, 150, 25))
        label_audio_features.setObjectName("label_audio_features")

        self.audio_features = QtWidgets.QTextEdit(self.groupBox_audio)
        self.audio_features.setGeometry(QtCore.QRect(20, 120, 510, 100))
        self.audio_features.setReadOnly(True)
        self.audio_features.setObjectName("audio_features")

        # Signal temporel
        label_signal_temporal = QtWidgets.QLabel(self.groupBox_audio)
        label_signal_temporal.setGeometry(QtCore.QRect(20, 235, 150, 25))
        label_signal_temporal.setObjectName("label_signal_temporal")

        self.label_signal_temporal = QtWidgets.QLabel(self.groupBox_audio)
        self.label_signal_temporal.setGeometry(QtCore.QRect(20, 260, 510, 200))
        self.label_signal_temporal.setStyleSheet("border: 1px solid gray; background-color: white;")
        self.label_signal_temporal.setScaledContents(True)
        self.label_signal_temporal.setObjectName("label_signal_temporal")

        # ==================== SECTION ECHANTILLONNAGE ====================
        self.groupBox_sampling = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_sampling.setGeometry(QtCore.QRect(590, 20, 550, 250))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.groupBox_sampling.setFont(font)
        self.groupBox_sampling.setObjectName("groupBox_sampling")

        # Boutons radio
        self.radio_fe2 = QtWidgets.QRadioButton(self.groupBox_sampling)
        self.radio_fe2.setGeometry(QtCore.QRect(20, 50, 100, 25))
        self.radio_fe2.setObjectName("radio_fe2")
        self.radio_fe2.setChecked(True)

        self.radio_fe4 = QtWidgets.QRadioButton(self.groupBox_sampling)
        self.radio_fe4.setGeometry(QtCore.QRect(130, 50, 100, 25))
        self.radio_fe4.setObjectName("radio_fe4")

        self.radio_fe8 = QtWidgets.QRadioButton(self.groupBox_sampling)
        self.radio_fe8.setGeometry(QtCore.QRect(240, 50, 100, 25))
        self.radio_fe8.setObjectName("radio_fe8")

        # Bouton valider
        self.btn_validate_resample = QtWidgets.QPushButton(self.groupBox_sampling)
        self.btn_validate_resample.setGeometry(QtCore.QRect(360, 45, 150, 32))
        self.btn_validate_resample.setObjectName("btn_validate_resample")

        # Signal échantillonné
        label_signal_echantillonne = QtWidgets.QLabel(self.groupBox_sampling)
        label_signal_echantillonne.setGeometry(QtCore.QRect(20, 100, 150, 25))
        label_signal_echantillonne.setObjectName("label_signal_echantillonne")

        self.label_signal_echantillonne = QtWidgets.QLabel(self.groupBox_sampling)
        self.label_signal_echantillonne.setGeometry(QtCore.QRect(20, 130, 510, 100))
        self.label_signal_echantillonne.setStyleSheet("border: 1px solid gray; background-color: white;")
        self.label_signal_echantillonne.setScaledContents(True)
        self.label_signal_echantillonne.setObjectName("label_signal_echantillonne")

        # ==================== SECTION COMPRESSION AUDIO ====================
        self.groupBox_compression_audio = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_compression_audio.setGeometry(QtCore.QRect(590, 290, 550, 210))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.groupBox_compression_audio.setFont(font)
        self.groupBox_compression_audio.setObjectName("groupBox_compression_audio")

        self.btn_compress_audio = QtWidgets.QPushButton(self.groupBox_compression_audio)
        self.btn_compress_audio.setGeometry(QtCore.QRect(20, 40, 180, 32))
        self.btn_compress_audio.setObjectName("btn_compress_audio")

        label_spectre = QtWidgets.QLabel(self.groupBox_compression_audio)
        label_spectre.setGeometry(QtCore.QRect(20, 90, 150, 25))
        label_spectre.setObjectName("label_spectre")

        self.label_spectre = QtWidgets.QLabel(self.groupBox_compression_audio)
        self.label_spectre.setGeometry(QtCore.QRect(20, 115, 510, 80))
        self.label_spectre.setStyleSheet("border: 1px solid gray; background-color: white;")
        self.label_spectre.setScaledContents(True)
        self.label_spectre.setObjectName("label_spectre")

        # ==================== SECTION VIDEO ====================
        self.groupBox_video = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_video.setGeometry(QtCore.QRect(20, 520, 550, 310))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.groupBox_video.setFont(font)
        self.groupBox_video.setObjectName("groupBox_video")

        self.btn_load_video = QtWidgets.QPushButton(self.groupBox_video)
        self.btn_load_video.setGeometry(QtCore.QRect(20, 50, 200, 32))
        self.btn_load_video.setObjectName("btn_load_video")

        label_video_features = QtWidgets.QLabel(self.groupBox_video)
        label_video_features.setGeometry(QtCore.QRect(20, 95, 150, 25))
        label_video_features.setObjectName("label_video_features")

        self.video_features = QtWidgets.QTextEdit(self.groupBox_video)
        self.video_features.setGeometry(QtCore.QRect(20, 120, 510, 80))
        self.video_features.setReadOnly(True)
        self.video_features.setObjectName("video_features")

        label_video_preview = QtWidgets.QLabel(self.groupBox_video)
        label_video_preview.setGeometry(QtCore.QRect(20, 215, 150, 25))
        label_video_preview.setObjectName("label_video_preview")

        self.label_video_preview = QtWidgets.QLabel(self.groupBox_video)
        self.label_video_preview.setGeometry(QtCore.QRect(20, 240, 510, 60))
        self.label_video_preview.setStyleSheet("border: 1px solid gray; background-color: black;")
        self.label_video_preview.setScaledContents(True)
        self.label_video_preview.setObjectName("label_video_preview")

        # ==================== SECTION COMPRESSION VIDEO ====================
        self.groupBox_compression_video = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_compression_video.setGeometry(QtCore.QRect(590, 520, 550, 310))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.groupBox_compression_video.setFont(font)
        self.groupBox_compression_video.setObjectName("groupBox_compression_video")

        # Paramètres FPS, Width, Height
        label_fps = QtWidgets.QLabel(self.groupBox_compression_video)
        label_fps.setGeometry(QtCore.QRect(20, 50, 50, 25))
        label_fps.setObjectName("label_fps")

        self.input_fps = QtWidgets.QLineEdit(self.groupBox_compression_video)
        self.input_fps.setGeometry(QtCore.QRect(80, 50, 80, 25))
        self.input_fps.setObjectName("input_fps")

        label_width = QtWidgets.QLabel(self.groupBox_compression_video)
        label_width.setGeometry(QtCore.QRect(180, 50, 50, 25))
        label_width.setObjectName("label_width")

        self.input_width = QtWidgets.QLineEdit(self.groupBox_compression_video)
        self.input_width.setGeometry(QtCore.QRect(240, 50, 80, 25))
        self.input_width.setObjectName("input_width")

        label_height = QtWidgets.QLabel(self.groupBox_compression_video)
        label_height.setGeometry(QtCore.QRect(340, 50, 50, 25))
        label_height.setObjectName("label_height")

        self.input_height = QtWidgets.QLineEdit(self.groupBox_compression_video)
        self.input_height.setGeometry(QtCore.QRect(400, 50, 80, 25))
        self.input_height.setObjectName("input_height")

        # Liste des codecs
        label_codec = QtWidgets.QLabel(self.groupBox_compression_video)
        label_codec.setGeometry(QtCore.QRect(20, 90, 50, 25))
        label_codec.setObjectName("label_codec")

        self.list_codec = QtWidgets.QListWidget(self.groupBox_compression_video)
        self.list_codec.setGeometry(QtCore.QRect(80, 90, 150, 70))
        self.list_codec.setObjectName("list_codec")
        self.list_codec.addItems(["mp4v", "MJPG", "XVID"])
        self.list_codec.setCurrentRow(0)

        self.btn_compress_video = QtWidgets.QPushButton(self.groupBox_compression_video)
        self.btn_compress_video.setGeometry(QtCore.QRect(20, 180, 150, 32))
        self.btn_compress_video.setObjectName("btn_compress_video")

        label_video_results = QtWidgets.QLabel(self.groupBox_compression_video)
        label_video_results.setGeometry(QtCore.QRect(20, 225, 200, 25))
        label_video_results.setObjectName("label_video_results")

        self.video_results = QtWidgets.QTextEdit(self.groupBox_compression_video)
        self.video_results.setGeometry(QtCore.QRect(20, 250, 510, 50))
        self.video_results.setReadOnly(True)
        self.video_results.setObjectName("video_results")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Traitement Multimédia - Audio & Vidéo"))

        # Audio section
        self.groupBox_audio.setTitle(_translate("MainWindow", "Analyse du signal audio"))
        self.btn_load_wav.setText(_translate("MainWindow", "Charger le fichier .wav"))
        label_audio_features = self.groupBox_audio.findChild(QtWidgets.QLabel, "label_audio_features")
        if label_audio_features:
            label_audio_features.setText(_translate("MainWindow", "Caractéristiques:"))
        label_signal_temporal = self.groupBox_audio.findChild(QtWidgets.QLabel, "label_signal_temporal")
        if label_signal_temporal:
            label_signal_temporal.setText(_translate("MainWindow", "Signal temporel:"))

        # Sampling section
        self.groupBox_sampling.setTitle(_translate("MainWindow", "Échantillonnage du signal"))
        self.radio_fe2.setText(_translate("MainWindow", "Fe/2"))
        self.radio_fe4.setText(_translate("MainWindow", "Fe/4"))
        self.radio_fe8.setText(_translate("MainWindow", "Fe/8"))
        self.btn_validate_resample.setText(_translate("MainWindow", "Valider"))
        label_signal_echantillonne = self.groupBox_sampling.findChild(QtWidgets.QLabel, "label_signal_echantillonne")
        if label_signal_echantillonne:
            label_signal_echantillonne.setText(_translate("MainWindow", "Signal échantillonné:"))

        # Audio compression section
        self.groupBox_compression_audio.setTitle(_translate("MainWindow", "Compression du signal"))
        self.btn_compress_audio.setText(_translate("MainWindow", "Compresser (r=128)"))
        label_spectre = self.groupBox_compression_audio.findChild(QtWidgets.QLabel, "label_spectre")
        if label_spectre:
            label_spectre.setText(_translate("MainWindow", "Spectre du signal:"))

        # Video section
        self.groupBox_video.setTitle(_translate("MainWindow", "Analyse de vidéo"))
        self.btn_load_video.setText(_translate("MainWindow", "Charger la vidéo"))
        label_video_features = self.groupBox_video.findChild(QtWidgets.QLabel, "label_video_features")
        if label_video_features:
            label_video_features.setText(_translate("MainWindow", "Caractéristiques:"))
        label_video_preview = self.groupBox_video.findChild(QtWidgets.QLabel, "label_video_preview")
        if label_video_preview:
            label_video_preview.setText(_translate("MainWindow", "Aperçu vidéo (trames):"))

        # Video compression section
        self.groupBox_compression_video.setTitle(_translate("MainWindow", "Compression vidéo"))
        label_fps = self.groupBox_compression_video.findChild(QtWidgets.QLabel, "label_fps")
        if label_fps:
            label_fps.setText(_translate("MainWindow", "FPS:"))
        label_width = self.groupBox_compression_video.findChild(QtWidgets.QLabel, "label_width")
        if label_width:
            label_width.setText(_translate("MainWindow", "Width:"))
        label_height = self.groupBox_compression_video.findChild(QtWidgets.QLabel, "label_height")
        if label_height:
            label_height.setText(_translate("MainWindow", "Height:"))
        label_codec = self.groupBox_compression_video.findChild(QtWidgets.QLabel, "label_codec")
        if label_codec:
            label_codec.setText(_translate("MainWindow", "Codec:"))
        self.btn_compress_video.setText(_translate("MainWindow", "Compresser"))
        label_video_results = self.groupBox_compression_video.findChild(QtWidgets.QLabel, "label_video_results")
        if label_video_results:
            label_video_results.setText(_translate("MainWindow", "Caractéristiques après compression:"))
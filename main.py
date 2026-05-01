# main.py
import os
import sys
import numpy as np
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import cv2
from scipy.io import wavfile
from scipy.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt

# Désactiver le mode interactif de matplotlib
plt.ioff()


class DesignWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(DesignWindow, self).__init__()

        # Charger l'interface
        qtcreator_file = "design.ui"
        if os.path.exists(qtcreator_file):
            # Charger depuis le fichier .ui
            uic.loadUi(qtcreator_file, self)
        else:
            # Fallback: utiliser la classe générée manuellement
            from design import Ui_MainWindow
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            # Transférer les widgets vers self
            self.btn_load_wav = self.ui.btn_load_wav
            self.audio_features = self.ui.audio_features
            self.label_signal_temporal = self.ui.label_signal_temporal
            self.radio_fe2 = self.ui.radio_fe2
            self.radio_fe4 = self.ui.radio_fe4
            self.radio_fe8 = self.ui.radio_fe8
            self.btn_validate_resample = self.ui.btn_validate_resample
            self.label_signal_echantillonne = self.ui.label_signal_echantillonne
            self.btn_compress_audio = self.ui.btn_compress_audio
            self.label_spectre = self.ui.label_spectre
            self.btn_load_video = self.ui.btn_load_video
            self.video_features = self.ui.video_features
            self.label_video_preview = self.ui.label_video_preview
            self.input_fps = self.ui.input_fps
            self.input_width = self.ui.input_width
            self.input_height = self.ui.input_height
            self.list_codec = self.ui.list_codec
            self.btn_compress_video = self.ui.btn_compress_video
            self.video_results = self.ui.video_results
            self.statusbar = self.ui.statusbar

        # Variables pour stocker les données
        self.audio_fe = None
        self.audio_signal = None
        self.audio_signal_mono = None
        self.audio_file_path = None

        self.video_cap = None
        self.video_path = None
        self.video_fps = None
        self.video_width = None
        self.video_height = None
        self.video_frame_count = None

        # Connexion des signaux
        self.btn_load_wav.clicked.connect(self.handle_load_audio)
        self.btn_validate_resample.clicked.connect(self.handle_resampling)
        self.btn_compress_audio.clicked.connect(self.handle_audio_compression)
        self.btn_load_video.clicked.connect(self.handle_load_video)
        self.btn_compress_video.clicked.connect(self.handle_video_compression)

        # Ajouter des items à la liste des codecs si elle est vide
        if self.list_codec.count() == 0:
            self.list_codec.addItems(["mp4v", "MJPG", "XVID"])

        # Sélectionner Fe/2 par défaut
        self.radio_fe2.setChecked(True)

        # Afficher la fenêtre
        self.show()

    # ==================== FONCTIONS UTILITAIRES AUDIO ====================

    def get_audio_info(self, fe, signal):
        """
        Extrait les informations du fichier audio
        """
        if signal.ndim == 1:
            n = len(signal)
            c = 1
            type_audio = "Mono"
        else:
            n, c = signal.shape
            type_audio = "Stéréo"

        duree = n / fe

        info = {
            'type': type_audio,
            'fe': fe,
            'echantillons': n,
            'duree': duree,
            'canaux': c
        }
        return info

    def plot_to_pixmap(self, signal, fe, title="Signal temporel", portion=None):
        """
        Convertit un signal numérique en QPixmap
        """
        plt.clf()

        # Créer le vecteur temps
        if portion is not None:
            signal_to_plot = signal[:portion]
        else:
            signal_to_plot = signal[:10000] if len(signal) > 10000 else signal

        t = np.arange(len(signal_to_plot)) / fe

        plt.figure(figsize=(6, 2.5))
        plt.plot(t, signal_to_plot, color='blue', linewidth=0.8)
        plt.xlabel("Temps (secondes)")
        plt.ylabel("Amplitude")
        plt.title(title)
        plt.tight_layout()

        # Sauvegarder en mémoire
        temp_filename = "temp_audio_plot.png"
        plt.savefig(temp_filename, dpi=100)
        plt.close()

        pixmap = QPixmap(temp_filename)

        # Nettoyer
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        return pixmap

    def plot_comparison_to_pixmap(self, original, resampled, factor):
        """
        Génère un graphique comparatif : Original (bleu) vs Échantillonné (rouge)
        """
        plt.clf()
        plt.figure(figsize=(6, 2))

        # Limiter à 10000 points pour la lisibilité
        limit = min(10000, len(original))
        original_plot = original[:limit]

        # Tracer l'original en bleu
        plt.plot(original_plot, color='blue', linewidth=0.8, label="Original")

        # Tracer le signal échantillonné en rouge
        resampled_limit = min(10000 // factor, len(resampled))
        indices = np.arange(0, resampled_limit) * factor
        plt.plot(indices, resampled[:resampled_limit], color='red', linewidth=0.6,
                 label=f"Fe/{factor}")

        plt.xlabel("Échantillons")
        plt.ylabel("Amplitude")
        plt.title(f"Comparaison - Sous-échantillonnage facteur {factor}")
        plt.legend(loc='upper right', fontsize=8)
        plt.tight_layout()

        temp_filename = "temp_resample.png"
        plt.savefig(temp_filename, dpi=100)
        plt.close()

        pixmap = QPixmap(temp_filename)
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        return pixmap

    def resample_signal(self, signal, factor):
        """
        Réduit la fréquence d'échantillonnage par un facteur n
        """
        if factor < 1:
            return signal
        return signal[::factor]

    def compress_audio_logic(self, signal, fe, r=128):
        """
        Compresse le signal par seuillage dans le domaine fréquentiel
        """
        # Convertir en mono si nécessaire
        if signal.ndim > 1:
            signal = signal[:, 0]

        # 1. Transformation FFT
        N = len(signal)
        z = fft(signal)

        # 2. Calcul du seuil
        modules = np.abs(z)
        modules_tries = np.sort(modules)
        indice_seuil = int(N * (1 - 1 / r))
        seuil = modules_tries[indice_seuil]

        # 3. Filtrage
        z_compresse = z.copy()
        z_compresse[np.abs(z) < seuil] = 0

        # 4. Reconstruction IFFT
        signal_reconstruit = ifft(z_compresse).real

        # Informations sur la compression
        ratio_conservation = (np.count_nonzero(z_compresse) / N) * 100

        return signal_reconstruit, z_compresse, seuil, ratio_conservation

    def plot_spectrum_to_pixmap(self, z, fe):
        """
        Affiche le spectre des fréquences
        """
        plt.clf()

        N = len(z)
        # Calcul des fréquences en Hertz
        freqs = fftfreq(N, 1 / fe)

        # Ne prendre que les fréquences positives
        half_N = N // 2
        freqs_pos = freqs[:half_N]
        magnitude = np.abs(z)[:half_N]

        plt.figure(figsize=(6, 2))
        plt.plot(freqs_pos, magnitude, color='green', linewidth=0.8)
        plt.xlabel("Fréquence (Hz)")
        plt.ylabel("Amplitude")
        plt.title("Spectre fréquentiel (FFT)")
        plt.xlim(0, fe / 2)
        plt.tight_layout()

        temp_filename = "temp_spectrum.png"
        plt.savefig(temp_filename, dpi=100)
        plt.close()

        pixmap = QPixmap(temp_filename)
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        return pixmap

    # ==================== GESTIONNAIRES AUDIO ====================

    def handle_load_audio(self):
        """
        Gestionnaire pour charger un fichier audio
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Charger un fichier audio", "",
            "Fichiers audio (*.wav *.aiff *.mp3);;Tous les fichiers (*.*)"
        )

        if not file_path:
            return

        try:
            # Charger le fichier
            fe, signal = wavfile.read(file_path)

            # Stocker les données
            self.audio_fe = fe
            self.audio_signal = signal
            self.audio_file_path = file_path

            # Extraire un canal mono pour l'analyse
            if signal.ndim == 1:
                self.audio_signal_mono = signal
            else:
                self.audio_signal_mono = signal[:, 0]

            # Obtenir les informations
            info = self.get_audio_info(fe, signal)

            # Afficher les caractéristiques
            info_text = f"Type: {info['type']}\n"
            info_text += f"Fréquence échantillonnage: {info['fe']} Hz\n"
            info_text += f"Nombre d'échantillons: {info['echantillons']}\n"
            info_text += f"Nombre de canaux: {info['canaux']}\n"
            info_text += f"Durée totale: {info['duree']:.2f} secondes"
            self.audio_features.setText(info_text)

            # Afficher le signal temporel
            pixmap = self.plot_to_pixmap(self.audio_signal_mono, fe, "Signal audio original")
            self.label_signal_temporal.setPixmap(pixmap)
            self.label_signal_temporal.setScaledContents(True)

            # Message de succès
            QMessageBox.information(self, "Succès", f"Fichier audio chargé avec succès!\n{info_text}")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement du fichier audio:\n{str(e)}")

    def handle_resampling(self):
        """
        Gestionnaire pour le sous-échantillonnage
        """
        if self.audio_signal_mono is None:
            QMessageBox.warning(self, "Attention", "Veuillez d'abord charger un fichier audio!")
            return

        # Récupérer le facteur de division
        if self.radio_fe2.isChecked():
            factor = 2
        elif self.radio_fe4.isChecked():
            factor = 4
        elif self.radio_fe8.isChecked():
            factor = 8
        else:
            factor = 2

        try:
            # Sous-échantillonner le signal
            resampled_signal = self.resample_signal(self.audio_signal_mono, factor)

            # Afficher la comparaison
            pixmap = self.plot_comparison_to_pixmap(self.audio_signal_mono, resampled_signal, factor)
            self.label_signal_echantillonne.setPixmap(pixmap)
            self.label_signal_echantillonne.setScaledContents(True)

            # Informations sur le sous-échantillonnage
            nouvelle_fe = self.audio_fe / factor
            QMessageBox.information(
                self, "Sous-échantillonnage",
                f"Sous-échantillonnage effectué avec facteur {factor}\n"
                f"Nouvelle fréquence d'échantillonnage: {nouvelle_fe:.1f} Hz\n"
                f"Nouveau nombre d'échantillons: {len(resampled_signal)}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du sous-échantillonnage:\n{str(e)}")

    def handle_audio_compression(self):
        """
        Gestionnaire pour la compression audio
        """
        if self.audio_signal is None:
            QMessageBox.warning(self, "Attention", "Veuillez d'abord charger un fichier audio!")
            return

        try:
            r = 128  # Facteur de compression

            # Compresser le signal
            signal_compresse, z_compresse, seuil, ratio = self.compress_audio_logic(
                self.audio_signal, self.audio_fe, r
            )

            # Afficher le spectre
            pixmap = self.plot_spectrum_to_pixmap(z_compresse, self.audio_fe)
            self.label_spectre.setPixmap(pixmap)
            self.label_spectre.setScaledContents(True)

            # Afficher les informations de compression
            QMessageBox.information(
                self, "Compression audio",
                f"Compression effectuée avec r = {r}\n"
                f"Seuil d'amplitude: {seuil:.2f}\n"
                f"Taux de conservation: {ratio:.2f}%\n"
                f"Taux de compression: {100 - ratio:.2f}%"
            )

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la compression audio:\n{str(e)}")

    # ==================== FONCTIONS UTILITAIRES VIDEO ====================

    def display_frame(self, frame):
        """
        Affiche une frame dans le QLabel
        """
        if frame is None:
            return

        # Convertir BGR (OpenCV) en RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convertir en QImage
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

        # Convertir en QPixmap et afficher
        pixmap = QPixmap.fromImage(qt_image)

        # Redimensionner pour l'affichage
        label_width = self.label_video_preview.width()
        label_height = self.label_video_preview.height()
        pixmap = pixmap.scaled(label_width, label_height,
                               Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)

        self.label_video_preview.setPixmap(pixmap)

    # ==================== GESTIONNAIRES VIDEO ====================

    def handle_load_video(self):
        """
        Gestionnaire pour charger un fichier vidéo
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Charger une vidéo", "",
            "Fichiers vidéo (*.avi *.mp4 *.mov);;Tous les fichiers (*.*)"
        )

        if not file_path:
            return

        try:
            # Ouvrir la vidéo
            cap = cv2.VideoCapture(file_path)

            if not cap.isOpened():
                raise Exception("Impossible d'ouvrir le fichier vidéo")

            # Extraire les métadonnées
            self.video_fps = cap.get(cv2.CAP_PROP_FPS)
            self.video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.video_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_path = file_path

            # Calculer la durée
            duree = self.video_frame_count / self.video_fps if self.video_fps > 0 else 0

            # Afficher les caractéristiques
            info_text = f"FPS: {self.video_fps:.2f}\n"
            info_text += f"Dimensions: {self.video_width} x {self.video_height} pixels\n"
            info_text += f"Nombre de trames: {self.video_frame_count}\n"
            info_text += f"Durée: {duree:.2f} secondes\n"
            info_text += f"Chemin: {os.path.basename(file_path)}"
            self.video_features.setText(info_text)

            # Lire la première frame
            ret, frame = cap.read()
            if ret:
                self.display_frame(frame)

            # Libérer la capture
            cap.release()

            # Mettre à jour les champs avec les valeurs par défaut
            self.input_fps.setText(f"{self.video_fps:.2f}")
            self.input_width.setText(str(self.video_width))
            self.input_height.setText(str(self.video_height))

            QMessageBox.information(self, "Succès", f"Vidéo chargée avec succès!\n{info_text}")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement de la vidéo:\n{str(e)}")

    def handle_video_compression(self):
        """
        Gestionnaire pour compresser la vidéo
        """
        if self.video_path is None:
            QMessageBox.warning(self, "Attention", "Veuillez d'abord charger une vidéo!")
            return

        try:
            # Récupérer les paramètres de compression
            try:
                new_fps = float(self.input_fps.text())
                new_width = int(self.input_width.text())
                new_height = int(self.input_height.text())
            except ValueError:
                QMessageBox.warning(self, "Erreur", "Veuillez saisir des valeurs numériques valides!")
                return

            # Récupérer le codec sélectionné
            selected_item = self.list_codec.currentItem()
            if selected_item is None:
                selected_codec = "mp4v"
            else:
                selected_codec = selected_item.text()

            fourcc_map = {
                "mp4v": cv2.VideoWriter_fourcc(*'mp4v'),
                "MJPG": cv2.VideoWriter_fourcc(*'MJPG'),
                "XVID": cv2.VideoWriter_fourcc(*'XVID')
            }
            fourcc = fourcc_map.get(selected_codec, cv2.VideoWriter_fourcc(*'mp4v'))

            # Ouvrir la vidéo source
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                raise Exception("Impossible d'ouvrir la vidéo source")

            # Créer le chemin de sortie
            base_name = os.path.splitext(self.video_path)[0]
            output_path = f"{base_name}_compressed_{selected_codec}_{new_width}x{new_height}_{new_fps}fps.avi"

            # Créer le VideoWriter
            out = cv2.VideoWriter(output_path, fourcc, new_fps, (new_width, new_height))

            if not out.isOpened():
                raise Exception("Impossible de créer le fichier de sortie")

            # Calculer la taille originale en Mo
            original_size = os.path.getsize(self.video_path) / (1024 * 1024)

            # Traiter frame par frame
            frame_count = 0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Redimensionner la frame
                frame_resized = cv2.resize(frame, (new_width, new_height))

                # Écrire la frame compressée
                out.write(frame_resized)

                frame_count += 1

                # Afficher la progression dans la barre de statut
                if frame_count % 100 == 0:
                    progress = (frame_count / total_frames) * 100
                    self.statusbar.showMessage(f"Compression vidéo: {progress:.1f}%")

            # Libérer les ressources
            cap.release()
            out.release()

            # Calculer la nouvelle taille
            new_size = os.path.getsize(output_path) / (1024 * 1024)

            # Afficher les résultats comparatifs
            reduction = ((original_size - new_size) / original_size) * 100 if original_size > 0 else 0

            results_text = f"=== RÉSULTATS DE LA COMPRESSION ===\n\n"
            results_text += f"Fichier original: {os.path.basename(self.video_path)}\n"
            results_text += f"Taille originale: {original_size:.2f} Mo\n\n"
            results_text += f"Fichier compressé: {os.path.basename(output_path)}\n"
            results_text += f"Taille compressée: {new_size:.2f} Mo\n"
            results_text += f"Réduction: {reduction:.1f}%\n\n"
            results_text += f"Paramètres appliqués:\n"
            results_text += f"• FPS: {self.video_fps:.1f} → {new_fps}\n"
            results_text += f"• Résolution: {self.video_width}x{self.video_height} → {new_width}x{new_height}\n"
            results_text += f"• Codec: {selected_codec}\n"
            results_text += f"• Trames totales: {self.video_frame_count} (inchangé)"

            self.video_results.setText(results_text)

            self.statusbar.showMessage(f"Compression terminée! Fichier sauvegardé: {os.path.basename(output_path)}",
                                       5000)

            QMessageBox.information(
                self, "Compression vidéo",
                f"Compression terminée avec succès!\n\n"
                f"Taille originale: {original_size:.2f} Mo\n"
                f"Nouvelle taille: {new_size:.2f} Mo\n"
                f"Réduction: {reduction:.1f}%\n\n"
                f"Fichier sauvegardé: {os.path.basename(output_path)}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la compression vidéo:\n{str(e)}")


# ==================== POINT D'ENTRÉE PRINCIPAL ====================

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DesignWindow()
    sys.exit(app.exec())
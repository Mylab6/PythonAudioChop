import os
from PyQt6.QtWidgets import *
from pydub import AudioSegment

class WavSplitter(QWidget):
    def __init__(self):
        super().__init__()

        self.input_file_label = QLabel("No file selected")
        self.select_input_file_button = QPushButton("Select input file", self)
        self.select_input_file_button.clicked.connect(self.select_input_file)

        self.output_file_label = QLabel("No output path selected")
        self.select_output_path_button = QPushButton("Select output path", self)
        self.select_output_path_button.clicked.connect(self.select_output_path)

        self.prefix_label = QLabel("File prefix:")
        self.prefix_textbox = QLineEdit()

        self.split_button = QPushButton("Split", self)
        self.split_button.clicked.connect(self.split)

        self.normalize_checkbox = QCheckBox("Half Normalize")

        self.duration_label = QLabel("Duration (in seconds):")
        self.duration_textbox = QLineEdit()

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Input file:"))
        hbox1.addWidget(self.input_file_label)
        hbox1.addWidget(self.select_input_file_button)
        vbox.addLayout(hbox1)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Output path:"))
        hbox2.addWidget(self.output_file_label)
        hbox2.addWidget(self.select_output_path_button)
        vbox.addLayout(hbox2)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.prefix_label)
        hbox3.addWidget(self.prefix_textbox)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.normalize_checkbox)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.duration_label)
        hbox4.addWidget(self.duration_textbox)
        vbox.addLayout(hbox4)
        vbox.addWidget(self.split_button)
        hbox5 = QHBoxLayout()
        hbox5.addWidget(QLabel("Status:"))
        self.status_label = QLabel("")
        hbox5.addWidget(self.status_label)
        vbox.addLayout(hbox5)
        self.setLayout(vbox)
        self.show()

    def select_input_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", os.getenv("HOME"), "Audio files (*.wav)")
        if filename:
            self.input_file_label.setText(filename)

    def select_output_path(self):
        dirname = QFileDialog.getExistingDirectory(self, "Select output directory", os.getenv("HOME"))
        if dirname:
            self.output_file_label.setText(dirname)

    def split(self):
        try:
            audio = AudioSegment.from_file(self.input_file_label.text())
            length = len(audio)
            segment_duration = int(float(self.duration_textbox.text()) * 1000)
            num_segments = length // segment_duration
            output_dir_path = self.output_file_label.text()
            prefix = self.prefix_textbox.text()
            os.makedirs(output_dir_path, exist_ok=True)
            if self.normalize_checkbox.isChecked():
                audio = audio.apply_gain(-audio.dBFS/2)
            for i in range(num_segments):
                start = i * segment_duration
                end = start + segment_duration
                output_file_path = os.path.join(output_dir_path, f"{prefix}_{i}.wav")
                audio[start:end].export(output_file_path, format="wav")
            self.status_label.setText("Done")
        except:
            self.status_label.setText("Error")

if __name__ == "__main__":
    app = QApplication([])
    splitter = WavSplitter()
    app.exec()

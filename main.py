import wave
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class WavSegmenter:
    def __init__(self, segment_duration):
        self.segment_duration = segment_duration

    def split(self, input_file, output_prefix):
        with wave.open(input_file, "rb") as wav_file:
            num_channels = wav_file.getnchannels()
            sample_rate = wav_file.getframerate()
            segment_frames = int(self.segment_duration * sample_rate)
            audio_data = np.frombuffer(wav_file.readframes(-1), dtype=np.int16)
            total_frames = len(audio_data)
            num_segments = int(np.ceil(total_frames / segment_frames))
            for i in range(num_segments):
                start_frame = i * segment_frames
                end_frame = min((i + 1) * segment_frames, total_frames)
                with wave.open(f"{output_prefix}_{i}.wav", "wb") as segment_file:
                    segment_file.setnchannels(num_channels)
                    segment_file.setframerate(sample_rate)
                    segment_file.setsampwidth(wav_file.getsampwidth())
                    segment_file.writeframes(audio_data[start_frame:end_frame].tobytes())
            messagebox.showinfo("Success", f"Successfully split {input_file} into {num_segments} segments.")
            

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.segment_duration = tk.StringVar()
        self.input_file = tk.StringVar()
        self.output_prefix = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Segment duration (seconds):").grid(row=0, column=0)
        tk.Entry(self.master, textvariable=self.segment_duration).grid(row=0, column=1)
        tk.Button(self.master, text="Select input file (.wav)", command=self.select_input_file).grid(row=1, column=0)
        tk.Entry(self.master, textvariable=self.input_file).grid(row=1, column=1)
        tk.Button(self.master, text="Select output prefix", command=self.select_output_prefix).grid(row=2, column=0)
        tk.Entry(self.master, textvariable=self.output_prefix).grid(row=2, column=1)
        tk.Button(self.master, text="Split", command=self.split).grid(row=3, column=0)

    def select_input_file(self):
        filetypes = [("WAV files", "*.wav")]
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if file_path:
            self.input_file.set(file_path)

    def select_output_prefix(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".wav")
        if file_path:
            self.output_prefix.set(file_path)

    def split(self):
        segmenter = WavSegmenter(float(self.segment_duration.get()))
        segmenter.split(self.input_file.get(), self.output_prefix.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

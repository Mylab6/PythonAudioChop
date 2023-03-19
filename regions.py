import os
import aubio
import numpy as np
from pydub import AudioSegment
import PySimpleGUI as sg

def detect_regions(input_file, threshold=-70):
    win_s = 1024
    hop_s = win_s // 2
    src = aubio.source(input_file, hop_s, hop_s)
    o = aubio.onset('default', win_s, hop_s, src.samplerate)
    o.set_threshold(threshold)
    regions = []

    while True:
        samples, read = src()
        if o(samples):
            regions.append(o.get_last())
        if read < hop_s:
            break

    return [int(region * 1000) for region in regions]

def split_audio(input_file, output_dir, prefix, regions):
    audio = AudioSegment.from_wav(input_file)
    output_files = []

    for i, region in enumerate(regions[:-1]):
        start = region
        end = regions[i + 1]
        segment = audio[start:end]
        duration = len(segment) / 1000
        output_file = os.path.join(output_dir, f"{prefix}_{i}_{duration:.2f}s.wav")
        output_files.append(output_file)
        segment.export(output_file, format="wav")

    return output_files

def main():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Select a WAV file to split')],
        [sg.Input(), sg.FileBrowse(file_types=(("WAV Files", "*.wav"),))],
        [sg.Text('Threshold (lower value detects more regions, default -70)'), sg.InputText('-70')],
        [sg.Text('Select output directory'), sg.Input(key='output_dir'), sg.FolderBrowse()],
        [sg.Text('Output file prefix'), sg.InputText('output', key='prefix')],
        [sg.Button('Split'), sg.Button('Exit')],
        [sg.Output(size=(60, 20), key='output')]
    ]

    window = sg.Window('WAV Audio Splitter', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == 'Split':
            input_file = values[0]
            threshold = float(values[1])
            output_dir = values['output_dir']
            prefix = values['prefix']

            if not input_file.lower().endswith('.wav'):
                sg.popup_error('Please select a WAV file.')
                continue

            try:
                regions = detect_regions(input_file, threshold)
                output_files = split_audio(input_file, output_dir, prefix, regions)
                window['output'].update(f"Split complete. Created {len(output_files)} files:\n" + "\n".join(output_files))
            except Exception as e:
                window['output'].update(f"Error: {e}")

    window.close()

if __name__ == '__main__':
    main()

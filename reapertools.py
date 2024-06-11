import librosa
import re
from pathlib import Path


def extract_text(file_path):
    pattern = r'[^_]+(?=\.[^.]*$)'
    match = re.search(pattern, str(file_path))
    if match:
        return match.group()
    return 'Track'


def build_item(wav_path, position, duration, soffset, title=""):
    if title == 'StereoMix':
        mute = 'MUTE 1 0'
    else:
        mute = 'MUTE 0 0'
    rpp_out = (f"\n\t\t<ITEM\n\t\t\tPOSITION {position}\n\t\t\tLENGTH {str(duration)}\n\t\t\t{mute}\n\t\t\t"
               f"SOFFS {str(soffset)}\n\t\t\tNAME \"{title}\"\n\t\t\t<SOURCE WAVE\n\t\t\t\t"
               f"FILE '{wav_path}'\n\t\t\t>\n\t\t>")
    return rpp_out


def build_rpp(name, wav_list, out_path):
    tracks = []
    for idx, wav_path in enumerate(wav_list):
        tn = extract_text(wav_path)
        if tn == 'StereoMix':
            track_name = f'{tn}\n\t\tISBUS 1 1'
        elif idx == len(wav_list) - 1:
            track_name = f'{tn}\n\t\tISBUS 2 -1'
        else:
            track_name = f'{tn}\n\t\tISBUS 0 0'
        duration = librosa.get_duration(path=str(wav_path))
        item = build_item(wav_path, 0, duration, 0, tn)
        tracks.append(f"\n\t<TRACK\n\t\tNAME {track_name}{item}\n\t>")

    start = "<REAPER_PROJECT\n"
    export = 'RENDER_FILE "' + f'{name}.wav' + \
             '"\nRENDER_FMT 0 1 44100\nRENDER_1X 0\nRENDER_RANGE 1 0 0 18 1000\nRENDER_RESAMPLE 3 0 ' \
             '1\nRENDER_ADDTOPROJ 0\nRENDER_STEMS 0\nRENDER_DITHER 0\nRENDER_NORMALIZE 193 0.1 0.668344 0 0 1 ' \
             '1\nTIMELOCKMODE 0\nTEMPOENVLOCKMODE 0\nITEMMIX 1\nDEFPITCHMODE 589824 0\nTAKELANE 1\nSAMPLERATE 44100 ' \
             '0 0\n<RENDER_CFG\nZXZhdxgAAA==\n> '
    end = f"\n{export}{''.join(tracks)}\n>"

    r = f"{start}{end}"

    with open(out_path / f"{name}.rpp", 'w') as f:  # write the rpp to disk
        f.write(r)

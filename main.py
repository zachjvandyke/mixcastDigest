import shutil
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from reapertools import build_rpp
import re
from pathlib import Path


def extract_directory(file_path):
    path = Path(file_path).parent
    return str(path)


def explode_polywav(wav_path):
    wav_path = make_directory_move_file(wav_path)
    # Load the stereo audio file
    stereo_audio = AudioSegment.from_wav(wav_path)

    # Split the stereo audio into left and right channels
    left_channel = stereo_audio.split_to_mono()[12]
    right_channel = stereo_audio.split_to_mono()[13]
    stereo_out = combine_mono_to_stereo(left_channel, right_channel)

    mic_1 = stereo_audio.split_to_mono()[0]
    mic_2 = stereo_audio.split_to_mono()[1]
    mic_3 = stereo_audio.split_to_mono()[2]
    mic_4 = stereo_audio.split_to_mono()[3]

    usb_left = stereo_audio.split_to_mono()[4]
    usb_right = stereo_audio.split_to_mono()[5]
    usb_stereo = combine_mono_to_stereo(usb_left, usb_right)

    line_left = stereo_audio.split_to_mono()[6]
    line_right = stereo_audio.split_to_mono()[7]
    line_stereo = combine_mono_to_stereo(line_left, line_right)

    bluetooth_left = stereo_audio.split_to_mono()[8]
    bluetooth_right = stereo_audio.split_to_mono()[9]
    bluetooth_stereo = combine_mono_to_stereo(bluetooth_left, bluetooth_right)

    sfx_left = stereo_audio.split_to_mono()[10]
    sfx_right = stereo_audio.split_to_mono()[11]
    sfx_stereo = combine_mono_to_stereo(sfx_left, sfx_right)

    wav_list = []
    # Export the left and right channels as separate mono WAV files
    if has_audio(stereo_out):
        stereo_out.export(f'{wav_path.stem}_StereoMix.wav', format="wav")
        wav_list.append(f'{wav_path.stem}_StereoMix.wav')
    if has_audio(mic_1):
        mic_1.export(f'{wav_path.stem}_Mic1.wav', format="wav")
        wav_list.append(f'{wav_path.stem}_Mic1.wav')
    if has_audio(mic_2):
        mic_2.export(f'{wav_path.stem}_Mic2.wav', format="wav")
        wav_list.append(f'{wav_path.stem}_Mic2.wav')
    if has_audio(mic_3):
        mic_3.export(f'{wav_path.stem}_Mic3.wav', format="wav")
        wav_list.append(f'{wav_path.stem}_Mic3.wav')
    if has_audio(mic_4):
        mic_4.export(f'{wav_path.stem}_Mic4.wav', format="wav")
        wav_list.append(f'{wav_path.stem}_Mic4.wav')
    if has_audio(usb_stereo):
        usb_stereo.export(f'{wav_path.stem}_USB.wav', format="wav")
        wav_list.append(f'{wav_path.stem}_USB.wav')
    if has_audio(line_stereo):
        line_stereo.export(f'{wav_path.stem}_AUX.wav', format="wav")
        wav_list.append(f'{wav_path.stem}_AUX.wav')
    if has_audio(bluetooth_stereo):
        bluetooth_stereo.export(f'{wav_path.stem}_Bluetooth.wav', format="wav")
        wav_list.append(f'{wav_path.stem}_Bluetooth.wav')
    if has_audio(sfx_stereo):
        sfx_stereo.export(f'{wav_path.stem}_SFX.wav', format="wav")
        wav_list.append(f'{wav_path.stem}_SFX.wav')

    name = wav_path.stem
    build_rpp(name, wav_list, extract_directory(str(wav_path)))


def combine_mono_to_stereo(left_audio, right_audio):
    # Ensure both segments have the same frame rate and sample width
    if left_audio.frame_rate != right_audio.frame_rate:
        raise ValueError("Left and right audio segments must have the same frame rate")
    if left_audio.sample_width != right_audio.sample_width:
        raise ValueError("Left and right audio segments must have the same sample width")

    # Combine the two mono audio segments into one stereo segment
    stereo_audio = AudioSegment.from_mono_audiosegments(left_audio, right_audio)
    return stereo_audio


def has_audio(audio_segment, silence_thresh=-50.0, min_silence_len=1000):
    nonsilent_ranges = detect_nonsilent(audio_segment, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    return len(nonsilent_ranges) > 0


def make_directory_move_file(filepath):
    path = Path(filepath)
    new_directory = path.parent / path.stem
    new_directory.mkdir(parents=True, exist_ok=True)
    new_filepath = new_directory / f'{path.stem}.wav'
    shutil.move(filepath, new_filepath)
    return new_filepath


def main():
    explode_polywav(Path(input('Paste the file path to your MixCast polywav: ')))


if __name__ == "__main__":
    main()

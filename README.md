# Digest and Explode MixCast 4 PolyWAV to a multitrack REAPER file

This Python script processes MixCast 4 PolyWAV files by extracting individual audio channels and exporting them as separate mono or stereo WAV files. It uses the `pydub` library to handle audio operations and includes a custom `reapertools.py` for building Reaper project files.

## Usage

To use the script, run the `main()` function, which will prompt you to input the file path to your MixCast PolyWAV file. The script will then process the file and export the individual channels.

```python
if __name__ == "__main__":
    main()
```

### Example

1. Run the script:

```bash
python explode_polywav.py
```

2. Paste the file path to your MixCast PolyWAV when prompted.

## Dependencies

- `shutil`
- `pydub`
- `re`
- `os`

Ensure you have the `pydub` library installed before running the script. You can install it via pip:

```bash
pip install pydub
```

## How It Works

- **Directory Extraction**: The script extracts the directory path from the given file path.
- **Channel Splitting**: It splits the provided PolyWAV file into individual channels and exports each channel as a separate WAV file if it contains audio.
- **Reaper Project File**: The script builds a Reaper project file from the extracted channels.

This script is useful for audio engineers and producers who need to manage and process multi-channel PolyWAV files efficiently.

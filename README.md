# audiocube

Toolbox for and information about the "*Audio-Cube*". The "*Audio-Cube*" is a cheap, cube-shaped device capable of playing audio files (usually: audio-books) stored on the Micro-SD-card in the Micro-SD-slot on the back of the device. The "*Audio-cube*" has no buttons - playback is controlled by placing "*Mifare Classic 1k*" NFC tags on top of the device that contain the ID of the audio file to be played.

In Germany, the "*Audio-Cube*" is sold as part of the "*[Märchenheld](collections/Märchenheld/)*" collection that contains 30 fairy-tales for children.

## audiocube.py

*audiocube.py* is a tiny toolbox for the Audio-Cube, providing the following features:

- Encrypt/decrypt audio files to be used by the Audio-Cube
- Create `.mct` files suitable for the free Android app "[MIFARE Classic Tool - MCT](https://play.google.com/store/apps/details?id=de.syss.MifareClassicTool)", allowing to create NFC tags that are compatible with the Audio-Cube

### Encrypt/decrypt audio files to be used by the Audio-Cube

```sh
$ audiocube.py crypt_file -h
usage: audiocube.py crypt_file [-h] input_file output_file

Encrypt/decrypt a sound file

positional arguments:
  input_file   the input file to read from ("-" for STDIN)
  output_file  the output file to write to ("-" for STDOUT)

optional arguments:
  -h, --help   show this help message and exit
```

Usage example: Encrypting a MP3 file named `foo.mp3` to an Audio-Cube-compatible `.smp` file with ID 3:
```sh
$ audiocube.py crypt_file foo.mp3 T0003.smp
```

Usage example: Decrypting an Audio-Cube-compatible `.smp` file with ID 39 to a MP3 file named `bar.mp3`:
```sh
$ audiocube.py crypt_file T0039.smp bar.mp3
```

### Create `.mct` files

```sh
$ audiocube.py nfc_content -h
usage: audiocube.py nfc_content [-h] [directory_id] file_id output_file

Generate a .mct NFC tag content file

positional arguments:
  directory_id  The directory ID, a hexadecimal string in range 00...FF (default: 01)
  file_id       The file ID, a hexadecimal string in range 0000...FFFF
  output_file   the output file to write to ("-" for STDOUT)

optional arguments:
  -h, --help    show this help message and exit
```

Usage example: Create a `.mct` file named "`Track 7.mct`" for the audio file with file ID 7 and the default directory ID 1:
```sh
$ audiocube.py nfc_content 7 "Track 7.mct"
```

Usage example: Create a `.mct` file named "`Track 13-9.mct`" for the audio file with file ID 9 and directory ID 13:
```sh
$ audiocube.py nfc_content 13 9 "Track 13-9.mct"
```

## Credits

"**Marc D.**" figured out and [published](https://www.mikrocontroller.net/topic/503014) all relevant information about the Audio-Cube.

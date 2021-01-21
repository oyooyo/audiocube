# LIDL Storyland

![](image-0004-512x512.jpg)

The "[LIDL Storyland](https://www.lidl-hellas.gr/storyland)" is a device sold in greek LIDL stores for 9,99 €. Figures are sold separately for 1,99 € each.

## Program usage

### Show general command overview

```sh
$ audiocube.py storyland --help
usage: audiocube.py storyland [-h] {encrypt,decrypt,create_nfc_file} ...

Toolbox for "LIDL Storyland"

positional arguments:
  {encrypt,decrypt,create_nfc_file}
                        The command to execute

optional arguments:
  -h, --help            show this help message and exit
```

### Encrypt/Convert .mp3 files to .SMP

To encrypt/convert .mp3 file(s) to the .SMP format that the files stored on the device need to have, use the `encrypt` command:

```sh
$ audiocube.py storyland encrypt --help
usage: audiocube.py storyland encrypt [-h] [--output_file_pattern OUTPUT_FILE_PATTERN] input_file [input_file ...]

Encrypt audio file(s)

positional arguments:
  input_file            The input file(s) to read from

optional arguments:
  -h, --help            show this help message and exit
  --output_file_pattern OUTPUT_FILE_PATTERN, -ofp OUTPUT_FILE_PATTERN
                        Pattern for the output filenames (default: {name}.SMP)
```

### Decrypt/Convert .SMP files to .mp3

To decrypt/convert .SMP file(s) stored on the device to regular MP3 file(s), use the "decrypt" command:

```sh
$ audiocube.py storyland decrypt --help
usage: audiocube.py storyland decrypt [-h] [--output_file_pattern OUTPUT_FILE_PATTERN] input_file [input_file ...]

Decrypt audio file(s)

positional arguments:
  input_file            The input file(s) to read from

optional arguments:
  -h, --help            show this help message and exit
  --output_file_pattern OUTPUT_FILE_PATTERN, -ofp OUTPUT_FILE_PATTERN
                        Pattern for the output filenames (default: {name}.mp3)
```

For example, to convert files L0010.SMP and L0011.SMP to L0010.mp3 and L0011.mp3:

```sh
$ audiocube.py storyland decrypt L0010.SMP L0011.SMP
"L0010.SMP" -> "L0010.mp3"
"L0011.SMP" -> "L0011.mp3"
```

### Create a custom NFC tag

This project contains [a directory](https://github.com/oyooyo/audiocube/tree/master/docs/devices/storyland/nfc) with several ready-to-use .csv files for creating NFC tags that will play the official fairytales/audio files by LIDL.

If however you want to create custom NFC tags that play custom audio files created by yourself, you can use the `create_nfc_file` subcommand to create custom .csv files.

In both cases, these .csv files can then be used by the "NFC TagWriter by NXP" smartphone app in order to create/write the required NFC tags.

```sh
$ audiocube.py storyland create_nfc_file --help
usage: audiocube.py storyland create_nfc_file [-h] file_id [name]

Create a NFC tag content file, in order to create a compatible ("NTAG213") NFC tag via the "NFC TagWriter by NXP" (https://play.google.com/store/apps/details?id=com.nxp.nfc.tagwriter) smartphone app

positional arguments:
  file_id     The file ID, a four-character ASCII string
  name        The name/label for this NFC tag. Determines the output file name. Optional, defaults to "L{file_id}" (default: None)

optional arguments:
  -h, --help  show this help message and exit
```

For example, to create a NFC tag that will play audio file "L0014.SMP", and shows up as "Some description" in the "NFC TagWriter by NXP" app, use:

```sh
$ audiocube.py storyland create_nfc_file 14 "Some description"
```

This will create a file named `Some description.csv`. In order to actually create the NFC tag, you need to perform the following steps afterwards:
1. Copy the `.csv` file to your smartphone, for example via `adb push`, by emailing it to your smartphone or however. The directory where you store it on your smartphone should not matter.
2. Install the free [NFC TagWriter by NXP](https://play.google.com/store/apps/details?id=com.nxp.nfc.tagwriter) app on your NFC-enabled Android smartphone, if you haven't installed it yet.
3. Open the "NFC TagWriter by NXP" app.
4. On the main screen, click "Write tags"
5. Click "Write from CSV"
6. Select the created `.csv` file
7. Do as the app advises you.

## Files

The audio files that the device is able to play need to be stored on the MicroSD card built into the device. The device ships with a 4GB MicroSD card that initially contains 6 audio files.

### Filesystem

ToDo

### File format

The audio files that the device plays are ultimately MP3 files. The device is a bit picky though and will not simply play all MP3 files. It is not 100% clear yet what characteristics a MP3 file needs to have to be compatible, but here's a few hints:

- The device *might* have problems playing MP3 files with ID3 metadata in the latest version v2.4. The audio files shipped with the device seem to use ID3 version v2.3 instead, so if you have the possibility, it might be a good idea to use ID3v2.3 as well just to avoid any potential problems.
- It might be necessary to store the filename (without extension, for example "L0016") in the title field of the ID3v2 tag
- The audio files shipped with the device use a sample rate of 44100 Hz, so that sample rate should be safe to use. However, the device is probably capable of playing all kinds of bit rates and sample rates

See [here](https://github.com/oyooyo/audiocube/issues/1#issuecomment-750953311) for a discussion on this.

### Encryption

They are standard MP3 files, but encrypted with a simple encryption algorithm:
1. For each byte in the MP3 file, the bits are rotated right by 3 bits (For example, 0b11010001 would become 0b00111010)
2. The whole file is then XORed with the byte array \[0x01, 0x80, 0x04, 0x04\]

## NFC Tags

ToDo

## Photos

![](image-0001.jpg)
![](image-0002.jpg)
![](image-0003.jpg)
![](image-0004.jpg)
![](image-0005.jpg)
![](image-0006.jpg)

## Credits

- [bserem](https://github.com/bserem) provided useful information about this and also the "Migros Storybox" device
- [cratsil1979](https://github.com/cratsil1979) provided lots of useful information, photos etc., details how to create compatible MP3 files etc.
- [Storylander](https://github.com/Storylander) found out that the device can not only distinguish 100 different files, but millions

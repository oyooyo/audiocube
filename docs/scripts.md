# Helper Scripts

## Storyland Encrypter

A bash script to facilitate encrypting any mp3 file into a storyland compatible
exists under the `scripts` folder.

### Requirements

- audiocube
- [eyed3](https://eyed3.readthedocs.io/en/latest/) (`apt install eyed3`)

Created and tested on Linux systems, but should be possible to port.

### Usage

Execute the script with:

```bash
cd scripts
./storyland_encrypter.sh /path/to/file.mp3 17
```

to convert `file.mp3` into `L0017.SMP`. ID3 tags will be automatically set to
create a compatible file and a CSV file with the NFC data will be created under
the `encrypted` folder.


Alternatively use:

```bash
cd scripts
./storyland_encrypter.sh /path/to/file.mp3 17 --nonfc
```

to not create the CSV file containing NFC data.

In both cases, an `index.txt` file holding information for the file will be created.
If the `index` file exists, new information will be appended.

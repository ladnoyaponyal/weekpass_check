# weekpass_check
This script, weekapss.py, allows users to check MD5 or NTLM hashes against the WeakPass API to find clear-text passwords. It supports single hash lookup or bulk processing from a file, with multithreading for fast and efficient operations.

# WeakPass Hash Checker

`weekpass.py` is a Python script that leverages the [WeakPass API](https://weakpass.com/) to retrieve clear-text passwords for MD5 and NTLM hashes. It supports checking single hashes or multiple hashes from a file and outputs the results to a specified file. With multithreading enabled, the script ensures high efficiency, especially for large hash lists.

## Features

- Lookup single or multiple hashes (MD5, NTLM) via WeakPass API
- Multi-threaded processing for faster handling of large hash lists
- Output results to a specified file, overwriting previous data

## Installation

Ensure Python 3.x is installed, along with the `requests` library:
```bash
pip install requests
```

## Usage

To use the script, run `check_hash.py` with the following options:

```bash
python3 check_hash.py [-s HASH] [-l FILE] -o OUTPUT [-t THREADS]
```

### Parameters
```
Argument	Description
-s, --hash	Check a single hash.
-l, --list	Check multiple hashes from a file.
-o, --output	Specify the output file for results (required).
-t, --threads	Set the number of threads (default: 50).
Note: The output file is cleared each time before writing new results.
```

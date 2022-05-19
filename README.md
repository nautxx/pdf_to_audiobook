# PDF to Audiobook Quickstart

A Python command-line application that converts pdf files into audiobooks.

## Install

```shell
pip install -r requirements.txt
```

## Dependencies
You can open and save WAV files with pure python. For opening and saving non-wav 
files – like mp3 – you'll need [ffmpeg](http://www.ffmpeg.org/) or 
[libav](http://libav.org/).
You will also need to obtain application credentials for 
[Google Cloud Vision](https://cloud.google.com/vision/docs/libraries?hl=en_US) and 
[Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech/docs/libraries?hl=en_US)
## Run

After following the setup instructions, run the sample:

```shell
python main.py [filename]
```
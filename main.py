import io
import os
import re
import json
import tempfile
import shutil
import argparse

from google.cloud import texttospeech   # pip install --upgrade google-cloud-texttospeech
from google.cloud import vision         # pip install --upgrade google-cloud-vision
from pdf2image import convert_from_path # pip install pdf2image
from pydub import AudioSegment          # pip install pydub

# Instantiates API clients
speech_client = texttospeech.TextToSpeechClient()
vision_client = vision.ImageAnnotatorClient()


# FILE_NAME = "Cracking_the_Coding_Interview_6th_Edition_Chapter_2.pdf"
FILE_NAME = None


def convert_pdf_to_png(file):
    """Coverts a PDF to PNG. PNGs stored in _temp folder."""

    global FILE_NAME
    FILE_NAME = file

    png_id = file.replace(".pdf", "")[:4]  # use the first 4 chars as file_id
    
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(
            file, dpi=200, output_folder=path, first_page=None,
            last_page=None
        )

    if not os.path.exists('_temp'):
        os.mkdir('_temp')

    print(f"Converting {file} to PNG...")
    for batch_id, image in enumerate(images_from_path, start=100):  # batch_id numbering starts at 100 for sort
        image.save(f'_temp/{png_id}_{batch_id}.png', 'PNG')
        print(f'_temp/{png_id}_{batch_id}.png created.')
    print(f"Finished converting PDF to PNGs for {file}")


def detect_document(path):
    """Detects document features in an image."""

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = vision_client.document_text_detection(image=image)

    # for page in response.full_text_annotation.pages:
    #     for block in page.blocks:
    #         print('\nBlock confidence: {}\n'.format(block.confidence))

    #         for paragraph in block.paragraphs:
    #             print('Paragraph confidence: {}'.format(
    #                 paragraph.confidence))

    #             for word in paragraph.words:
    #                 word_text = ''.join([
    #                     symbol.text for symbol in word.symbols
    #                 ])
    #                 print('Word text: {} (confidence: {})'.format(
    #                     word_text, word.confidence))

    #                 for symbol in word.symbols:
    #                     print('\tSymbol: {} (confidence: {})'.format(
    #                         symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return response


def detect_text(path):
    """Detects text in the file."""

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = vision_client.text_detection(image=image)

    texts = response.text_annotations
    text_unfiltered = texts[0].description

    # print('Texts:')

    # for text in texts:
    #     print('\n"{}"'.format(text.description))

    #     vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                 for vertex in text.bounding_poly.vertices])

    #     print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return text_unfiltered


def extract_page_text():
    """Stores .png files into a list of texts in sequential order."""

    file_names = []

    file_names = [file_name for file_name in os.listdir('_temp')]
        # file_names.append(file_name)

    file_names_sorted = sorted(file_names)
    file_names_sorted = file_names_sorted
    
    text_data_list = [] # merge text data into one file.
    for file_name in file_names_sorted:
        text_data_list.append(detect_text(f"_temp/{file_name}"))

    return text_data_list


def generate_mp3_from_text(text, batch_id):
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=1.5
    )
    response = speech_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    if not os.path.exists('_temp_mp3'):
        os.mkdir('_temp_mp3')

    mp3_file_id = FILE_NAME[:4]  # use the first 4 chars as file_id
    mp3_file_path = "_temp_mp3/" + mp3_file_id
    with open(f"{mp3_file_path}_{batch_id}.mp3", "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{mp3_file_path}_{batch_id}.mp3"')


def generate_mp3_files(text):
    """Generates all MP3s into _temp_mp3 folder from text_data_list."""

    print("Converting text to audio...")
    for batch_id, page_text in enumerate(text, start=100):
        generate_mp3_from_text(page_text, batch_id)


def merge_mp3_files():
    """Merges the files generated from generate_mp3_files and old files."""

    merged_mp3 = None
    mp3_list = [mp3 for mp3 in os.listdir('_temp_mp3')]
    mp3_list_sorted = sorted(mp3_list)

    print("Started merging mp3 files.")
    for mp3 in mp3_list_sorted:
        mp3_data = AudioSegment.from_file(f"_temp_mp3/{mp3}", format="mp3")
        if merged_mp3:
            merged_mp3 += mp3_data
            print(f"{mp3} added.")
        else:
            merged_mp3 = mp3_data
            print(f"{mp3} added.")

    # save the merged mp3 file
    mp3_file_name = FILE_NAME.replace(".pdf", "")
    merged_mp3.export(f"{mp3_file_name}.mp3", format="mp3")
    print("Finished merging mp3 files.")

    # delete temporary files
    print("Deleting temp files...")
    shutil.rmtree('_temp')
    shutil.rmtree('_temp_mp3')
    print("Temp files deleted.")


def pdf_to_audiobook(file):
    convert_pdf_to_png(file)
    text = extract_page_text()
    generate_mp3_files(text)
    merge_mp3_files()


# response = extract_page_text()
# with open("output_document10.txt", "a") as f:
#     print(response, file=f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="The name of the pdf to convert to audio.")
    args = parser.parse_args()

    pdf_to_audiobook(args.file_name)
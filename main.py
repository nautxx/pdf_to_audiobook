import io
import os
import re
import json
import tempfile

from google.cloud import texttospeech   # pip install --upgrade google-cloud-texttospeech
from google.cloud import vision     #pip install --upgrade google-cloud-vision
from pdf2image import convert_from_path

# Instantiates API clients
speech_client = texttospeech.TextToSpeechClient()
vision_client = vision.ImageAnnotatorClient()


def convert_pdf_to_png(file):
    png_id = file.replace(".pdf", "")[:4]  # use the first 4 chars as file_id
    
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(
            file, dpi=200, output_folder=path, first_page=None,
            last_page=None
        )

    if not os.path.isfile('_temp'):
        os.mkdir('_temp')

    for i, image in enumerate(images_from_path):
        image.save(f'_temp/{png_id}{i}.png', 'PNG')


# def book_pdf_to_audiobook(file=FILE_NAME, start_page=1):
#     """Reads outloud selected page from book."""
#     with open(SAVE_DIRECTORY + file + ".json", "r") as json_file:
#         pages = json.load(json_file)

#         cont = True
#         while cont:
#             page = pages[str(start_page)]
#             page_parsed = re.sub("\n", "", page)

#             txt_to_speech(f"Now Reading Page {start_page} of {len(pages)}:{page_parsed}")
#             print(f"Reading Page {start_page} of {len(pages)}:\n\n{page_parsed}\n")
#             txt_to_speech(page_parsed)
            
#             txt_to_speech("Would you like to continue? Type y for yes or n for no.")
#             if input("Continue? y/n ") == "n":
#                 cont = False
#             start_page += 1


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


def generate_mp3_from_text(text):
    
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

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    #TODO Delete temp_dir and files after success



#script
convert_pdf_to_png("example.pdf")
# text = detect_text("temp_dir/png_blob0.png")
# generate_mp3_from_text(text)
# with open("output_document2.txt", "a") as f:
#     print(response, file=f)

import io
import os
import re
import json

from google.cloud import texttospeech   # pip install --upgrade google-cloud-texttospeech
from google.cloud import vision     #pip install --upgrade google-cloud-vision

# from pdf2image import convert_from_path # pip install pdf2image
# import PyPDF2   # pip install PyPDF2


FILE_NAME = "Cracking_the_Coding_Interview_6th_Edition"
SAVE_DIRECTORY = "Saved/"
PAGE_NO = 1


# Instantiates API clients
speech_client = texttospeech.TextToSpeechClient()
vision_client = vision.ImageAnnotatorClient()


def generate_mp3_from_text(text):
    
    synthesis_input = texttospeech.SynthesisInput(text="Hello, World!")
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


# def convert_pdf_to_png():
#     with tempfile.TemporaryDirectory() as path:
#         images_from_path = convert_from_path(
#             'example.pdf', dpi=200, output_folder=path, first_page=None,
#             last_page=None
#         )

#         if not os.path.isfile('temp_dir'):
#             os.mkdir('temp_dir')

#         for i, image in enumerate(images_from_path):
#             image.save(f'temp_dir/png_blob{i}.png', 'PNG')


# def get_text_from_pdf(file=FILE_NAME, page=1):
#     """Converts 1 pdf page to text."""
#     # open file and convert to text
#     file_path = open(file, 'rb')
#     # initialize the object
#     pypdf2_file = PyPDF2.PdfFileReader(file_path)

#     text_from_page = pypdf2_file.getPage(int(page))
#     pdf_to_text_converted = text_from_page.extractText()

#     return pdf_to_text_converted


# def save_pdf_book_to_json(file=FILE_NAME):
#     """Saves entire book to json for faster access later at a cost of storage. Deletes original .pdf after."""
#     file_path = open(file + ".pdf", 'rb')
#     pypdf2_file = PyPDF2.PdfFileReader(file_path)

#     number_of_pages = pypdf2_file.numPages
#     all_pages = {}

#     for page in range(number_of_pages):
#         all_pages.update({page: pypdf2_file.getPage(page).extractText()})

#     with open(SAVE_DIRECTORY + file + ".json", "w") as json_file:
#         json.dump(all_pages, json_file)

#     os.remove(file + ".pdf")


# def txt_to_speech(text):
#     """Reads outloud inputted text."""
#     # initialize the object
#     pyttsx3_file = pyttsx3.init()
#     pyttsx3_file.setProperty('voice', "com.apple.speech.synthesis.voice.daniel")    
#     pyttsx3_file.say(text)
#     pyttsx3_file.runAndWait()


# def pdf_to_speech(file=FILE_NAME, page=PAGE_NO):
#     text = get_text_from_pdf(FILE_NAME, page)
#     txt_to_speech(text)


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


# # pdf_to_speech()
# # save_pdf_book_to_json(FILE_NAME)
# book_pdf_to_audiobook(start_page=23)

# get_text_from_pdf()
# convert_pdf_to_png()

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

    dictionary = json.loads(response.text)
    print(dictionary)
    
    # texts = response.text_annotations
    # print('Texts:')

    # for text in texts:
    #     print('\n"{}"'.format(text.description))

    #     vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                 for vertex in text.bounding_poly.vertices])

    #     print('bounds: {}'.format(','.join(vertices)))

    # if response.error.message:
    #     raise Exception(
    #         '{}\nFor more info on error messages, check: '
    #         'https://cloud.google.com/apis/design/errors'.format(
    #             response.error.message))

    return response

response = detect_document("temp_dir/png_blob0.png")


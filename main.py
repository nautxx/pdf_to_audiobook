import PyPDF2
import fitz
import pyttsx3
import json


FILE_NAME = "Cracking_the_Coding_Interview_6th_Edition"
# PAGE = input("Enter Page No.: ")


def get_text_from_pdf(file, page=1):
    """Converts 1 pdf page to text."""
    # open file and convert to text
    file_path = open(file, 'rb')
    # initialize the object
    pypdf2_file = PyPDF2.PdfFileReader(file_path)

    text_from_page = pypdf2_file.getPage(int(page))
    pdf_to_text_converted = text_from_page.extractText()

    return pdf_to_text_converted


def save_pdf_book_to_json(file):
    """Saves entire book to json for faster access later at a cost of storage."""
    file_path = open(file + ".pdf", 'rb')
    pypdf2_file = PyPDF2.PdfFileReader(file_path)

    number_of_pages = pypdf2_file.numPages
    all_pages = {}

    for page in range(number_of_pages):
        all_pages.update({pypdf2_file.getPage(page).extractText(): page})

    with open(FILE_NAME, "w") as json_file:
        json.dump(all_pages, json_file)


def speak_pdf(text):
    """Reads outloud inputted text."""
    # initialize the object
    pyttsx3_file = pyttsx3.init()

    pyttsx3_file.say(text)
    pyttsx3_file.runAndWait()


def pdf_to_audiobook():
    text = get_text_from_pdf(FILE_NAME, PAGE)
    speak_pdf(text)


def book_pdf_to_audiobook(file=FILE_NAME, start_page=1):
    """Reads outloud selected page from book."""
    with open(file + ".json", "r") as json_file:
        text = json.load(json_file)
        print(text)
        speak_pdf(text[start_page])


# pdf_to_audiobook()
# save_pdf_page()
# save_pdf_book_to_json(FILE_NAME)
book_pdf_to_audiobook(start_page=25)
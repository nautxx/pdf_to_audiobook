import PyPDF2
import pyttsx3
import json
import re
import os


FILE_NAME = "Cracking_the_Coding_Interview_6th_Edition"
SAVE_DIRECTORY = "Saved/"
PAGE_NO = 1


def get_text_from_pdf(file=FILE_NAME, page=1):
    """Converts 1 pdf page to text."""
    # open file and convert to text
    file_path = open(file, 'rb')
    # initialize the object
    pypdf2_file = PyPDF2.PdfFileReader(file_path)

    text_from_page = pypdf2_file.getPage(int(page))
    pdf_to_text_converted = text_from_page.extractText()

    return pdf_to_text_converted


def save_pdf_book_to_json(file=FILE_NAME):
    """Saves entire book to json for faster access later at a cost of storage. Deletes original .pdf after."""
    file_path = open(file + ".pdf", 'rb')
    pypdf2_file = PyPDF2.PdfFileReader(file_path)

    number_of_pages = pypdf2_file.numPages
    all_pages = {}

    for page in range(number_of_pages):
        all_pages.update({page: pypdf2_file.getPage(page).extractText()})

    with open(SAVE_DIRECTORY + file + ".json", "w") as json_file:
        json.dump(all_pages, json_file)

    os.remove(file + ".pdf")


def txt_to_speech(text):
    """Reads outloud inputted text."""
    # initialize the object
    pyttsx3_file = pyttsx3.init()
    pyttsx3_file.setProperty('voice', "com.apple.speech.synthesis.voice.daniel")    
    pyttsx3_file.say(text)
    pyttsx3_file.runAndWait()


# def save_voice_file(text, page):
#     """Saves voice file to .mp3"""
#     pyttsx3_file = pyttsx3.init()

#     pyttsx3_file.save_to_file(text, f"{FILE_NAME}_{page}.mp3")
#     pyttsx3_file.runAndWait()


def pdf_to_speech(file=FILE_NAME, page=PAGE_NO):
    text = get_text_from_pdf(FILE_NAME, page)
    txt_to_speech(text)


def book_pdf_to_audiobook(file=FILE_NAME, start_page=1):
    """Reads outloud selected page from book."""
    with open(SAVE_DIRECTORY + file + ".json", "r") as json_file:
        pages = json.load(json_file)

        cont = True
        while cont:
            page = pages[str(start_page)]
            page_parsed = re.sub("\n", "", page)

            txt_to_speech(f"Now Reading Page {start_page} of {len(pages)}:{page_parsed}")
            print(f"Reading Page {start_page} of {len(pages)}:\n\n{page_parsed}\n")
            txt_to_speech(page_parsed)
            
            txt_to_speech("Would you like to continue? Type y for yes or n for no.")
            if input("Continue? y/n ") == "n":
                cont = False
            start_page += 1
        





# pdf_to_speech()
# save_pdf_book_to_json(FILE_NAME)
book_pdf_to_audiobook(start_page=23)

from flask import Flask, request, jsonify, make_response, redirect, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from markupsafe import escape
from time import sleep
from requests import get
import threading
from PyPDF2 import PdfReader
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "sadfjls#skjdfk21DJSFK1231#@"

upload_dir = os.path.join(app.instance_path, 'uploads')
processed_files_dir = os.path.join(app.instance_path, 'processed_files')
os.makedirs(upload_dir, exist_ok=True)
os.makedirs(processed_files_dir, exist_ok=True)

@app.get("/")
def default():
    print(session)
    return make_response("This world is really awesome and soon I will be rich with no loans")


@app.get("/Shashi")
def home():
    threading.Thread(target=parallel, args=[]).start()
    session["someone"] = "browser"
    print(session)
    return jsonify({
        "fruits": ['mango', 'orange', 'apple']
    })


def parallel():
    print("#########")
    response = get("https://catfact.ninja/fact?max_length=22")
    return redirect("/Shashi")


@app.post("/read-pdf")
def read_pdf():
    file = request.files.get('file')
    fileName = file.filename
    
    # save file on sever temporarily
    filePath = os.path.join(upload_dir, secure_filename(fileName))
    file.save(filePath)

    # offloading the high intensive processing to new thread
    t1 = threading.Thread(target=parsePdf, args=[filePath])
    t1.start()
    
    return "done"

def parsePdf(filePath):
    try:
        pdf_reader = PdfReader(filePath)
        texts_combine = ""

        for texts in pdf_reader.pages:
            texts_combine += texts.extract_text()

        # text_file = os.path.join(upload_dir, 'parsed.txt')
        # with open(text_file, "w", encoding="utf-8") as text_file:
        #     writable_text = texts_combine.split('\n')
        #     text_file.writelines(writable_text)

        os.remove(filePath)
        # os.remove(text_file)
    except Exception as e:
        print(str(e))


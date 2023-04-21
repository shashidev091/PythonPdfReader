from flask import Flask, request
from dotenv import load_dotenv
from markupsafe import escape
import requests, PyPDF2
from io import BytesIO

load_dotenv()

app = Flask(__name__)

@app.post("/<name>")
def home(name):
    print(request.get_json())
    url = 'https://www.blv.admin.ch/dam/blv/de/dokumente/lebensmittel-und-ernaehrung/publikationen-forschung/jahresbericht-2017-2019-oew-rr-rasff.pdf.download.pdf/Jahresbericht_2017-2019_DE.pdf'
    response = requests.get(url)
    my_raw_data = response.content

    with BytesIO(my_raw_data) as data:
        read_pdf = PyPDF2.PdfReader(data)
        print("############# => Reading Completed, Now extracting")
        for page in range(len(read_pdf.pages)):
            print(read_pdf.pages[page].extract_text())
    return f"<h3>This is home page {escape(name)}</h3>"
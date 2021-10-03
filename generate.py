from functools import reduce
import base64
from io import BytesIO

from flask import Flask, request
import qrcode

def get_qrcode(student):
    url = "https://sig.site.internal:1000/logout?;"
    url += "https://sig.site.internal:1000/login?#"

    qrcode_url = url + student

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qrcode_url)
    qr.make(fit=True)

    return qr.make_image(fill='black', back_color='white')


app = Flask(__name__)
@app.route("/")
def submit_form():
    form = """<form action="/submit_usernames" method="POST">
        <textarea name="student_logins" rows="10"></textarea>
        <input type="submit">
    </form>"""
    return form


@app.route('/submit_usernames', methods=['POST'])
def submit_usernames():
    students = request.form['student_logins'].splitlines()
    
    qr_codes = []
    for student in students:
        img_buf = BytesIO()
        img = get_qrcode(student)
        img.save(img_buf)
        img_buf.seek(0)

        data = img_buf.read()
        data = base64.b64encode(data)
        data = data.decode()
        
        html = "<div class='qr_code_div'>"
        html += "<h2>" + student + "</h2>"
        html += "<img alt={} src='data:image/png;base64,{}'>".format(student, data)
        html += "</div>"

        qr_codes += html
    
    qr_html = reduce(lambda x, y: x + y, qr_codes)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask app</title>
        <style>
            .qr_code_div {float: left}
            .qr_code_div h2 {text-align: center}
        </style>
    </head>
    <body>
        """ + qr_html + """
    </body>
    </html>"""
    return html

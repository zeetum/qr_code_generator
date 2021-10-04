from flask import Flask, request
import base64
from io import BytesIO
import qrcode

def get_qrcode(student):
    url = "https://sig.site.internal:1000/logout?;"
    url += "https://sig.site.internal:1000/login?#" + student

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_buf = BytesIO()
    img.save(img_buf)
    img_buf.seek(0)

    data = img_buf.read()
    data = base64.b64encode(data)
    data = data.decode()

    return data


app = Flask(__name__)
@app.route("/")
def submit_form():
    form = """
    <form action="/submit_usernames" method="POST">
        <textarea name="student_logins" rows="10"></textarea>
        <input type="submit">
    </form>"""
    return form


@app.route('/submit_usernames', methods=['POST'])
def submit_usernames():
    students = request.form['student_logins'].splitlines()
    
    qr_html = ""
    for student in students:
        data = get_qrcode(student)

        html = "<div class='qr_code_div'>"
        html += "<h2>" + student + "</h2>"
        html += "<img alt={} src='data:image/png;base64,{}'>".format(student, data)
        html += "</div>"

        qr_html += html
    

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DOE QR Codes</title>
        <style>
            .qr_code_div {float: left; border-style: solid;}
            .qr_code_div h2 {text-align: center}
        </style>
    </head>
    <body>
        """ + qr_html + """
    </body>
    </html>"""
    return html

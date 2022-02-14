import xlsxwriter
import base64
from io import BytesIO
import qrcode

def get_qrcode(filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(filename)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_buf = BytesIO()
    img.save(img_buf)
    img_buf.seek(0)

    return img_buf

workbook = xlsxwriter.Workbook('audiobooks.xlsx')
worksheet = workbook.add_worksheet()
with open("audio_links.txt", "r") as csv_file:
    worksheet.set_column('A:A', 40)
    worksheet.set_column('B:B', 85)
    for row, line in enumerate(csv_file):
        row += 1

        name = ' '.join(line.split()[4:])
        filename = "http://e5167s01sv011.indigo.schools.internal/Audiobooks/" + '%20'.join(line.split()[4:])
        image = get_qrcode(filename)

        worksheet.set_row(row -1, 400)
        worksheet.write('A' + str(row), name[:-4])
        worksheet.insert_image('B' + str(row), filename, {'image_data': image})

workbook.close()

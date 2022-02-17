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

    return (img_buf, img.size)

workbook = xlsxwriter.Workbook('audiobooks.xlsx')
worksheet = workbook.add_worksheet()
with open("audio_links.txt", "r") as csv_file:
    worksheet.set_column('A:A', 40)
    col_width = 0
    for row, line in enumerate(csv_file):

        name = line[:-4]
        filename = line

        (image, (width, height)) = get_qrcode(filename)
        if width > col_width:
            col_width = width

        worksheet.set_row_pixels(row, height)
        worksheet.write('A' + str(row + 1), name[:-4])
        worksheet.insert_image('B' + str(row), filename, {'image_data': image})

    print(col_width)
    worksheet.set_column_pixels('B:B', col_width)

workbook.close()

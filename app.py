from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import zipfile
from io import BytesIO
import uuid
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

UPLOAD_FOLDER = "static/certificates"
FONT_PATH_NORMAL = "Aptos-Display-Italic.ttf"
FONT_PATH_BOLD = "Aptos-Bold.ttf"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def adjust_font_size(draw, text, font_path, initial_size, max_width, min_size=26):
    font_size = initial_size
    font = ImageFont.truetype(font_path, font_size)
    text_width = draw.textbbox((0, 0), text, font=font)[2]

    while text_width > max_width and font_size > min_size:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        text_width = draw.textbbox((0, 0), text, font=font)[2]

    return font_size


def draw_paragraph_with_bold(draw, text_parts, start_x, start_y, max_width, base_font_size,
                              font_path_normal, font_path_bold, line_spacing=10, fill_color="black"):
    normal_font = ImageFont.truetype(font_path_normal, base_font_size)
    bold_font = ImageFont.truetype(font_path_bold, base_font_size)

    lines = []
    current_line = []
    current_width = 0

    for part, is_bold in text_parts:
        font = bold_font if is_bold else normal_font
        bbox = draw.textbbox((0, 0), part, font=font)
        part_width = bbox[2] - bbox[0]

        if current_width + part_width <= max_width:
            current_line.append((part, is_bold))
            current_width += part_width
        else:
            lines.append(current_line)
            current_line = [(part, is_bold)]
            current_width = part_width

    if current_line:
        lines.append(current_line)

    y = start_y
    for line in lines:
        x = start_x
        for part, is_bold in line:
            font = bold_font if is_bold else normal_font
            draw.text((x, y), part, font=font, fill=fill_color)
            part_width = draw.textbbox((0, 0), part, font=font)[2]
            x += part_width
        y += base_font_size + line_spacing


def generate_certificates_from_excel(excel_path, template_path, starting_number):
    df = pd.read_excel(excel_path)
    generated_files = []

    for index, row in df.iterrows():
        image = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(image)

        cert_id = f"Certificate ID : NHTPL-25-{starting_number + index}"

        draw.text((200, 360), cert_id, fill="black",
                  font=ImageFont.truetype(FONT_PATH_BOLD, 30))

        text_parts = [
            ("This is to certify that ", False),
            (row['NAME'], True),
            (", bearing Reg. No: ", False),
            (row['ROLLNO'], True),
            (", from ", False),
            (row['CLGNAME'], True),
            (" has successfully ", False),
            ("completed a", False),
            (" Long-term ", False),
            ("internship from, ", False),
            ("5th February ", True),
            ("2025 ", True),
            ("to ", False),
            ("10th April ", True),
            ("2025 ", True),
            ("on ", False),
            (row['DOMAIN'], True),
            ("  from ", False),
            (row['COURSE'], True),
            (" in the year 2025. ", False),
            ("This internship ", False),
            ("was organized, ", False),
            ("by NextHub Technologies ", False),
            ("Private Limited, ", False),
            ("in association with ", False),
            ("the Andhra  ", False),
            ("Pradesh State, ", False),
            ("Council of Higher", False),
            (" Education (APSCHE).", False),
        ]

        paragraph_text = ''.join([part for part, _ in text_parts])
        base_font_size = adjust_font_size(
            draw, paragraph_text, FONT_PATH_NORMAL, initial_size=30, max_width=1000)

        draw_paragraph_with_bold(
            draw, text_parts,
            start_x=200,
            start_y=420,
            max_width=1000,
            base_font_size=base_font_size,
            font_path_normal=FONT_PATH_NORMAL,
            font_path_bold=FONT_PATH_BOLD,
            line_spacing=8
        )

        filename = f"{row['ROLLNO'].replace(' ', '_')}_certificate.jpg"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(file_path)
        generated_files.append(file_path)

    return generated_files


def send_certificate_email(sender_email, sender_password, receiver_email, subject, body, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)

    with open(attachment_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)
    msg.add_attachment(file_data, maintype='application',
                       subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        excel_file = request.files.get('excel')
        template_file = request.files.get('template')
        starting_number = request.form.get('starting_number')
        sender_email = request.form.get('sender_email')
        sender_password = request.form.get('sender_password')

        if excel_file and template_file and starting_number and sender_email and sender_password:
            excel_path = f"{uuid.uuid4().hex}_data.xlsx"
            template_ext = template_file.filename.rsplit('.', 1)[-1].lower()
            template_path = f"{uuid.uuid4().hex}_template.{template_ext}"

            excel_file.save(excel_path)
            template_file.save(template_path)

            try:
                generated_files = generate_certificates_from_excel(
                    excel_path, template_path, int(starting_number))
                df = pd.read_excel(excel_path)

                for i, file_path in enumerate(generated_files):
                    row = df.iloc[i]
                    receiver_email = row['EMAIL']
                    subject = "Your Internship Certificate - NextHub Technologies"
                    body = f"Dear {row['NAME']},\n\nPlease find attached your internship certificate.\n\nRegards,\nNextHub Technologies"
                    try:
                        send_certificate_email(
                            sender_email,
                            sender_password,
                            receiver_email,
                            subject,
                            body,
                            file_path
                        )
                        print(f"✅ Sent to: {receiver_email}")
                    except Exception as e:
                        print(f"❌ Failed to send to {receiver_email}: {e}")

                # Optional: return zip of all certificates
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for file_path in generated_files:
                        zip_file.write(file_path, os.path.basename(file_path))
                zip_buffer.seek(0)

                return send_file(
                    zip_buffer,
                    mimetype='application/zip',
                    download_name='certificates.zip',
                    as_attachment=True
                )

            finally:
                os.remove(excel_path)
                os.remove(template_path)
                for file_path in os.listdir(UPLOAD_FOLDER):
                    os.remove(os.path.join(UPLOAD_FOLDER, file_path))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

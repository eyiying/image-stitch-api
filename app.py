from flask import Flask, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/combine', methods=['POST'])
def combine_images():
    files = request.files.getlist('images')
    if not files:
        return {"error": "No images uploaded"}, 400

    images = [Image.open(f.stream) for f in files]
    max_width = max(img.width for img in images)

    total_height = 0
    resized_images = []
    for img in images:
        ratio = img.height / img.width
        new_height = int(max_width * ratio)
        resized_img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        resized_images.append(resized_img)
        total_height += new_height

    result_img = Image.new('RGB', (max_width, total_height))
    y_offset = 0
    for img in resized_images:
        result_img.paste(img, (0, y_offset))
        y_offset += img.height

    output_io = io.BytesIO()
    result_img.save(output_io, format='JPEG')
    output_io.seek(0)

    return send_file(output_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

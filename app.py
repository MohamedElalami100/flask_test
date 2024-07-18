from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api
# import mysql.connector
from datetime import datetime
# import json
from dotenv import load_dotenv
import os

app = Flask(__name__)


@app.route('/')
def home():
    return "hello world"


app.config['CLOUDINARY_CLOUD_NAME'] = os.getenv('CLOUDINARY_CLOUD_NAME')
app.config['CLOUDINARY_API_KEY'] = os.getenv('CLOUDINARY_API_KEY')
app.config['CLOUDINARY_API_SECRET'] = os.getenv('CLOUDINARY_API_SECRET')

# Load Cloudinary configuration from environment variables
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# MySQL database configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '14C7c60595@'
DB_NAME = 'images_test'

# Initialize MySQL connection
# db_conn = mysql.connector.connect(
#     host=DB_HOST,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     database=DB_NAME
# )


def save_image_to_cloudinary(image_file, public_id):
    upload_result = cloudinary.uploader.upload(image_file, public_id=public_id)
    return upload_result["secure_url"]


@app.route('/uploadImage/<firmId>', methods=['POST'])
def upload_image(firmId):
    if 'rgb_image' not in request.files or 'nir_image' not in request.files:
        return jsonify({"error": "Image and metadata are required"}), 400

    rgb_image_file = request.files['rgb_image']
    nir_image_file = request.files['nir_image']

    # Extract metadata
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Validate image size (example: max 10 MB)
    if rgb_image_file.content_length > 10 * 1024 * 1024 or nir_image_file.content_length > 10 * 1024 * 1024:
        return jsonify({"error": "Image size exceeds limit"}), 400

    # Save image to Cloudinary
    rgb_public_id = f"{firmId}_rgb_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    nir_public_id = f"{firmId}_nir_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    rgb_image_url = save_image_to_cloudinary(rgb_image_file, rgb_public_id)
    nir_image_url = save_image_to_cloudinary(nir_image_file, nir_public_id)

    # Save metadata and image URL to MySQL database
    # cursor = db_conn.cursor()
    # cursor.execute(
    #     "INSERT INTO images (firm_id, upload_date, image_url) VALUES (%s, %s, %s)",
    #     (firmId, upload_date, rgb_image_url)
    # )
    # cursor.execute(
    #     "INSERT INTO images (firm_id, upload_date, image_url) VALUES (%s, %s, %s)",
    #     (firmId, upload_date, nir_image_url)
    # )
    # db_conn.commit()

    return jsonify({"message": "Images uploaded successfully", "rgb_image_url": rgb_image_url,
                    "nir_image_url": nir_image_url}), 200


if __name__ == '__main__':
    app.run()

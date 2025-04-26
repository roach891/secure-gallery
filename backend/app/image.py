import os
import io
from flask import Blueprint, request, jsonify, send_file, current_app as app
import mimetypes
from werkzeug.utils import secure_filename
import uuid

from jwt_utils import decode_access_token, token_required
from models import Image, User
from database import db
from crypto_utils import encrypt_data, generate_key, generate_iv, decrypt_data

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB

image_bp = Blueprint('image_bp', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_current_user_id():
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("No user ID ('sub') found in token payload")
        try:
            return uuid.UUID(user_id)
        except ValueError:
            raise ValueError(f"Invalid user ID format: {user_id}")
    except Exception:
        return None

@image_bp.route('/images', methods=['GET'])
@token_required
def list_images(current_user):
    try:
        images = Image.query.filter_by(user_id=current_user.id).all()
        image_list = [
            {
                "filename": img.filename,
                "url": f"{app.config['BACKEND_URL']}/images/{img.filename}"
            } for img in images
        ]
        return jsonify({"images": image_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@image_bp.route('/images/<filename>', methods=['GET'])
@token_required
def get_image(current_user, filename):
    try:
        image = Image.query.filter_by(filename=filename).first()
        if not image:
            return jsonify({"error": "Image not found"}), 404

        if image.user_id != current_user.id:
            return jsonify({"error": "You do not have permission to access this image"}), 403

        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = decrypt_data(encrypted_data, image.encryption_key, image.iv)

        original_ext = filename.rsplit('.', 2)[1]
        mime_type, _ = mimetypes.guess_type(f"file.{original_ext}")

        if not mime_type:
            mime_type = 'image/jpeg'

        response = send_file(
            io.BytesIO(decrypted_data),
            mimetype=mime_type,
            as_attachment=True,
            download_name=filename
        )
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@image_bp.route('/images/<filename>', methods=['DELETE'])
@token_required
def delete_image(current_user, filename):
    try:
        image = Image.query.filter_by(filename=filename, user_id=current_user.id).first()
        if not image:
            return jsonify({"error": "Image not found or not yours"}), 404
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            db.session.delete(image)
            db.session.commit()
            return jsonify({"message": "Image deleted"}), 200
        else:
            return jsonify({"error": "File not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@image_bp.route('/upload', methods=['POST'])
@token_required
def upload_image(current_user):
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and allowed_file(file.filename):
            file.seek(0, 2) 
            filesize = file.tell()
            file.seek(0, 0)
            if filesize > MAX_IMAGE_SIZE:
                return jsonify({"error": "File size exceeds the maximum limit of 2MB"}), 400

            file_data = file.read()
            encryption_key = generate_key()
            iv = generate_iv()
            encrypted_data = encrypt_data(file_data, encryption_key, iv)

            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}.enc"
            encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)

            new_image = Image(filename=unique_filename, user_id=current_user.id, encryption_key=encryption_key, iv=iv)
            db.session.add(new_image)
            db.session.commit()

            return jsonify({"message": "Image uploaded"}), 201
        else:
            return jsonify({"error": "Invalid file type. Please upload an image in PNG, JPG, JPEG, or GIF format."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

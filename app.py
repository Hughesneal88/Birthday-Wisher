from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from datetime import datetime
import uuid
from main import (
    get_user_data,
    get_users_with_today_birthday,
    send_sms_hubtel
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and send birthday wishes"""
    filepath = None
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get form data
        message = request.form.get('message', '')
        client_id = request.form.get('client_id', '')
        client_secret = request.form.get('client_secret', '')
        sender_id = request.form.get('sender_id', '')
        
        # Validate required fields
        if not all([message, client_id, client_secret, sender_id]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Get original filename for validation
        filename = file.filename
        
        # Save the uploaded file with a secure random filename
        file_ext = os.path.splitext(filename)[1].lower()
        secure_filename = f"{uuid.uuid4()}{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename)
        file.save(filepath)
        
        # Read the file based on extension
        if file_ext == '.csv':
            df = pd.read_csv(filepath)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(filepath)
        else:
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': 'Invalid file format. Please upload CSV or Excel file'}), 400
        
        # Process the data
        users = get_user_data(df)
        birthday_users = get_users_with_today_birthday(users)
        
        # Send SMS to birthday users
        results = []
        for user in birthday_users:
            try:
                if "phone" in user and isinstance(user["phone"], str):
                    recipient = user["phone"].split('/')[0].strip()
                    if recipient.startswith('+'):
                        recipient = recipient[1:]
                    
                    # Format the message with the user's name
                    try:
                        formatted_message = message.format(name=user.get("name", "Beloved"))
                    except KeyError as e:
                        results.append({
                            'name': user.get('name', 'Unknown'),
                            'phone': user.get('phone', 'Unknown'),
                            'status': 'error',
                            'message': f'Invalid message template: missing placeholder {e}'
                        })
                        continue
                    
                    # Send the SMS
                    response = send_sms_hubtel(client_id, client_secret, sender_id, recipient, formatted_message)
                    
                    # Check if response indicates success
                    if response and isinstance(response, dict):
                        results.append({
                            'name': user.get('name', 'Unknown'),
                            'phone': user.get('phone', 'Unknown'),
                            'status': 'success',
                            'message': 'SMS sent successfully'
                        })
                    else:
                        results.append({
                            'name': user.get('name', 'Unknown'),
                            'phone': user.get('phone', 'Unknown'),
                            'status': 'error',
                            'message': 'Failed to send SMS'
                        })
                else:
                    results.append({
                        'name': user.get('name', 'Unknown'),
                        'phone': user.get('phone', 'Unknown'),
                        'status': 'skipped',
                        'message': 'Invalid phone number'
                    })
            except Exception as e:
                results.append({
                    'name': user.get('name', 'Unknown'),
                    'phone': user.get('phone', 'Unknown'),
                    'status': 'error',
                    'message': str(e)
                })
        
        return jsonify({
            'success': True,
            'total_users': len(users),
            'birthday_users': len(birthday_users),
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the uploaded file
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass  # Ignore cleanup errors

if __name__ == '__main__':
    # Use environment variable for debug mode, default to False for production
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)

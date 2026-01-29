from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from datetime import datetime
from main import (
    get_user_data,
    get_users_with_today_birthday,
    send_sms_to_birthday_users
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
        
        # Save the uploaded file
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read the file based on extension
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(filepath)
        else:
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
                    formatted_message = message.format(name=user.get("name", "Beloved"))
                    
                    # Send the SMS (this is a dry run for now)
                    from main import send_sms_hubtel
                    response = send_sms_hubtel(client_id, client_secret, sender_id, recipient, formatted_message)
                    
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
        
        # Clean up the uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'total_users': len(users),
            'birthday_users': len(birthday_users),
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Birthday Wisher

A web-based application for sending automated birthday SMS messages to your contacts using the Hubtel API.

## Features

- 🎂 Upload CSV or Excel files containing birthday information
- 📱 Automatically send SMS to today's birthday celebrants
- ✉️ Customize birthday messages with personalization
- 🔒 Secure credential handling
- 📊 View detailed sending results

## Prerequisites

- Python 3.7 or higher
- Hubtel API credentials (Client ID and Client Secret)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Hughesneal88/Birthday-Wisher.git
cd Birthday-Wisher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Web Application

1. Run the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

### Using the Web Interface

1. **Upload Your Birthday List**
   - Prepare a CSV or Excel file with the following columns:
     - `NAME ` (note: includes a trailing space)
     - `DATE OF BIRTH`
     - `PHONE CONTACT`
   
   Example CSV format:
   ```csv
   NAME ,DATE OF BIRTH,PHONE CONTACT
   John Doe,January 15 1990,0244123456
   Jane Smith,December 25 1985,0201234567
   ```

2. **Enter Your Hubtel Credentials**
   - Client ID: Your Hubtel API client ID
   - Client Secret: Your Hubtel API client secret
   - Sender ID: The name that will appear as the sender (e.g., "LBC")

3. **Customize Your Message**
   - Write your birthday message in the text area
   - Use `{name}` to personalize the message for each recipient
   - Example:
     ```
     Happy Birthday {name}! 
     
     Wishing you a wonderful day filled with joy and happiness.
     ```

4. **Send Birthday Wishes**
   - Click the "Send Birthday Wishes" button
   - The application will automatically:
     - Parse your uploaded file
     - Identify today's birthday celebrants
     - Send personalized SMS messages
     - Display the results

## File Format Requirements

Your CSV or Excel file must include these columns (note the trailing space in NAME ):

- **NAME **: The recipient's full name (column name includes a trailing space)
- **DATE OF BIRTH**: Birthday in formats like:
  - "January 15 1990"
  - "Jan 15 1990"
  - "15/01/1990"
  - "15-01-1990"
- **PHONE CONTACT**: Phone number (formats accepted):
  - "0244123456" (local format)
  - "+233244123456" (international format)
  - "244123456" (without leading zero)

## Running the Original Script

To run the original command-line version:

```bash
python main.py
```

Note: You'll need to place your Excel file named `To_Neal.xlsx` in the project directory and configure the API credentials in the script.

## Security Notes

- **API Credentials**: Your Hubtel API credentials are sent with each request but are not stored by the application. For production use, consider implementing server-side configuration with environment variables.
- **File Upload**: The application validates file extensions and automatically deletes uploaded files after processing.
- **Debug Mode**: Set the `FLASK_DEBUG` environment variable to `true` only in development environments. Never use debug mode in production.
- Never commit your API credentials to version control

## Troubleshooting

### SMS Not Sending
- Verify your Hubtel API credentials are correct
- Ensure phone numbers are in valid format
- Check that you have sufficient credit in your Hubtel account

### File Upload Issues
- Ensure your file has the correct column names
- Check that dates are in a supported format
- Verify file size is under 16MB

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions, please open an issue on the GitHub repository.

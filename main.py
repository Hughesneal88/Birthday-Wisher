# API = "qTxidxjAsT7Jwb2OsCnLURcIRWz8tB7Z"
# Secret = "QPI7SA1uzoVUKITx"

import random
import requests
import pandas as pd
from datetime import datetime


# def get_oauth_token(api_key, secret):
#     """
#     Get an OAuth token using the provided API key and secret.
#     """
#     url = "https://api.mtn.com/v1/oauth/access_token/accesstoken?grant_type=client_credentials"
    
#     payload = {
#         # "grant_type": "client_credentials",
#         "scope": "send-sms",
#         "client_id": api_key,
#         "client_secret": secret
#     }
    
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded",
#         # "Accept": "application/json",  # Ensure the API accepts JSON responses
#     }
    
#     response = requests.post(url, data=payload, headers=headers)
    
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise Exception(f"Failed to get OAuth token: {response.text}")


# def send_sms(phone_number, message):
#     """
#     Send an SMS message using the MTN API.
#     """
#     url = "https://api.mtn.com/v2/messages/sms/outbound"

#     payload = {
#         "senderAddress": "+233559271576",
#         "receiverAddress": [phone_number],
#         "message": message,
#         "clientCorrelatorId": "test123"
#     }
#     token = get_oauth_token(API, Secret)

#     print(token)
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {token.get('access_token')}",
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code in [200, 201]:
#         print("SMS sent successfully!")
#         return response
#     else:
#         print(f"Error {response.status_code}: {response.text}")
#         raise Exception(f"Failed to send SMS: {response.text}")




# def send_sms_v3(api_key, secret, sender_address, receiver_addresses, message, client_correlator_id, keyword, service_code):
#     """
#     Send an SMS using the MTN API v3.
    
#     :param api_key: The API key for authentication.
#     :param secret: The client secret for authentication.
#     :param sender_address: The sender's address (e.g., "MTN").
#     :param receiver_addresses: A list of recipient phone numbers in E.164 format.
#     :param message: The SMS message to send.
#     :param client_correlator_id: A unique identifier for the request.
#     :param keyword: The keyword associated with the service.
#     :param service_code: The service code (e.g., "11221" or "131").
#     :return: The API response.
#     """
#     # Get OAuth token
#     token_url = "https://api.mtn.com/v1/oauth/access_token/accesstoken?grant_type=client_credentials"
#     token_payload = {
#         "grant_type": "client_credentials",
#         "scope": "SEND-SMS",
#         "client_id": api_key,
#         "client_secret": secret
#     }
#     token_headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     token_response = requests.post(token_url, data=token_payload, headers=token_headers)
    
#     if token_response.status_code != 200:
#         raise Exception(f"Failed to get OAuth token: {token_response.text}")
    
#     print(token_response.json())  # Debugging line to check the token response

#     access_token = token_response.json().get("access_token")
    
#     # Send SMS
#     url = "https://api.mtn.com/v2/messages/sms/outbound"
#     payload = {
#         "senderAddress": sender_address,
#         "receiverAddress": receiver_addresses,
#         "message": message,
#         "clientCorrelatorId": client_correlator_id,
#         "keyword": keyword,
#         # "serviceCode": service_code,
#         "requestDeliveryReceipt": False
#     }
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {access_token}",
#         "x-api-key": f"{api_key}"
#     }
    
#     response = requests.post(url, json=payload, headers=headers)
    
#     if response.status_code in [200, 201]:
#         print("SMS sent successfully!")
#         return response.json()
#     else:
#         print(f"Error {response.status_code}: {response.text}")
#         raise Exception(f"Failed to send SMS: {response.text}")

# # Example usage

def send_sms_hubtel(client_id, client_secret, sender_id, recipient, message):
    """
    Send an SMS message using the Hubtel API.

    :param client_id: Your Hubtel client ID.
    :param client_secret: Your Hubtel client secret.
    :param sender_id: The sender ID (e.g., "TrashApp").
    :param recipient: The recipient's phone number in international format (e.g., 233559271576).
    :param message: The SMS message content.
    :return: The API response.
    """
    url = "https://smsc.hubtel.com/v1/messages/send"
    params = {
        "clientsecret": client_secret,
        "clientid": client_id,
        "from": sender_id,
        "to": recipient,
        "content": message
    }
    response = requests.get(url, params=params)

    if response.status_code == 201 or 200:
        print(f"SMS sent successfully via Hubtel! to {recipient}")
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        raise Exception(f"Failed to send SMS via Hubtel: {response.text}")



def get_user_data(df, name_column="NAME ", dob_column="DATE OF BIRTH", phone_column="PHONE CONTACT"):
    """
    Extract user data from the DataFrame.
    
    :param df: The DataFrame containing user data.
    :param name_column: The column name for user names.
    :param dob_column: The column name for user dates of birth.
    :param phone_column: The column name for user phone numbers.
    :return: A list of dictionaries containing user data.
    """
    # Check if DOB column exists in the DataFrame
    has_dob_column = dob_column in df.columns
    
    users = []
    for index, row in df.iterrows():
        user = {
            "name": str(row[name_column]).strip() if pd.notna(row[name_column]) else "",
            "dob": str(row[dob_column]).strip() if has_dob_column and pd.notna(row[dob_column]) else "",
            "phone": str(row[phone_column]).strip() if pd.notna(row[phone_column]) else ""
        }
        #convert the phone number to E.164 format but remove the 0 before the first digit if it exists
        if user["phone"] and user["phone"].startswith("0"):
            user["phone"] = user["phone"][1:]
        if user["phone"]:
            user["phone"] = user["phone"].replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            if not user["phone"].startswith("+"):
                user["phone"] = "+233" + user["phone"]
        else:
            user["phone"] = ""
        if has_dob_column:
            normalized = normalize_dob(user["dob"])
            if normalized:
                user["dob"] = normalized
        users.append(user)
    return users

def normalize_dob(dob):
    """
    Normalize the date of birth (dob) to the format '%b %d %Y'.
    If the dob is invalid, return None.
    """
    # Map common incorrect or non-standard month abbreviations to their correct forms
    # month_mapping = {
    #     "Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
    #     "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
    #     "Sep": "September", "Sept": "September", "Oct": "October",
    #     "Nov": "November", "Dec": "December"
    # }

    # # Replace incorrect or non-standard month abbreviations
    # for short, full in month_mapping.items():
    #     if short in dob:
    #         dob = dob.replace(short, full)
    #         break  # Stop after the first match

    # Try parsing the dob with multiple formats
    formats = ["%B %d %Y", "%b %d %Y", "%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y", "%d/%m/%Y", "%d-%m-%Y"]  # Full month name and abbreviated month name
    for fmt in formats:
        try:
            # Parse and reformat the dob to '%b %d %Y'
            return datetime.strptime(dob.strip(), fmt).strftime("%b %d %Y")
        except ValueError:
            continue

    # If all parsing attempts fail, return None
    return None
def get_users_with_today_birthday(users):
    """
    Filter users whose birthday matches today's date.
    If no DOB data is available, return all users with valid phone numbers.
    """
    # Check if any user has DOB data
    has_any_dob = any(user.get("dob", "").strip() for user in users)
    
    # If no DOB column exists, return all users with valid phone numbers
    if not has_any_dob:
        print("No DOB column found. Returning all users with valid phone numbers.")
        return [user for user in users if user.get("phone", "").strip()]
    
    today = datetime.now().strftime("%m-%d")  # Format today's date as MM-DD
    users_with_birthday_today = []

    for user in users:
        dob = user.get("dob", "").strip()  # Get and strip the 'dob' field
        if not dob:
            print(f"Skipping user with empty DOB: {user}")
            continue

        # Normalize the dob
        normalized_dob = normalize_dob(dob)
        if not normalized_dob:
            print(f"Invalid DOB format for user: {user}")
            continue

        try:
            # Parse the normalized dob and compare it to today's date
            user_birthday = datetime.strptime(normalized_dob, "%b %d %Y").strftime("%m-%d")
            if user_birthday == today:
                users_with_birthday_today.append(user)
        except ValueError:
            print(f"Error parsing DOB for user: {user}")
            continue

    return users_with_birthday_today


def send_sms_to_birthday_users(users, client_id, client_secret, sender_id, message_template):
    """
    Send SMS to users whose birthday is today using the send_sms_hubtel function.

    :param users: List of user dictionaries with 'dob' and 'phone' fields.
    :param client_id: Hubtel client ID for authentication.
    :param client_secret: Hubtel client secret for authentication.
    :param sender_id: The sender ID for the SMS.
    :param message_template: The message template to send.
    """
    # Get users with today's birthday
    users_with_birthday_today = get_users_with_today_birthday(users)
    print("Users with today's birthday:", users_with_birthday_today)

    # Send SMS to each user
    for user in users_with_birthday_today:
        try:
            # Ensure 'phone' exists and is valid
            if "phone" in user and isinstance(user["phone"], str):
                recipient = user["phone"].split('/')[0].strip()  # Use the first phone number if multiple are provided
                if recipient.startswith('+'):
                    recipient = recipient[1:]  # Remove the '+' for Hubtel compatibility

                # Format the message with the user's name
                message = message_template.format(name=user.get("name", "Beloved"))

                # Send the SMS
                print(f"Sending SMS to {recipient}...")
                response = send_sms_hubtel(client_id, client_secret, sender_id, recipient, message)
                print(f"Response for {recipient}: {response}")
            else:
                print(f"Skipping user with invalid phone: {user}")
        except Exception as e:
            print(f"Error sending SMS to {user}: {e}")
# Helper function to validate date format
def is_valid_date(date_string, date_format):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    users = get_user_data(pd.read_excel("To_Neal.xlsx"))  # Load the DataFrame and extract user data
    today = datetime.now().strftime("%m-%d")  # Format as MM-DD

    birthday_users = get_users_with_today_birthday(users)
    print("Users with today's birthday:", birthday_users)

    # print("Users with today's birthday:" , get_users_with_today_birthday(users))
    # for user in get_users_with_today_birthday(users):
    #     message = f"Happy Birthday {user['name']}!. \n The Head Pastor of Legon Baptist church would like to wish you Happy Birthday on this special day. We give thanks to God for adding another year to your age. May the Lord continue to give you good health. and strength. May you continue to enjoy favor and mercies of God. The sovereign Lord, is your strength!!!  Amen!!"
    #     response = send_sms(user["phone"].split('/')[0].strip(), message)
    #     # response = send_sms("+233559271576", message)
    #     print(f"Sent SMS to {user['name']} ({user['phone'].split('/')[0].strip()}): {response.status_code} - {response.headers}")
    # API_KEY = API
    # SECRET = Secret

    # SENDER_ADDRESS = "Legon Baptist Church"
    # RECEIVER_ADDRESSES = ["233559271576"]
    # MESSAGE = "Hello, this is a test message."
    # CLIENT_CORRELATOR_ID = "unique-id-12345"
    # KEYWORD = "test-keyword"
    # SERVICE_CODE = "131"

    client_id = "iufiekdo"
    client_secret = "bkmiwpcc"
    sender_id = "LBC"
    # recipient = "233559271576"
    # recipient = "233244296945"
    message = f"""Dear Beloved in Christ,

On behalf of the entire church family and myself, I rejoice with you on the occasion of your birthday. Today we thank God for the gift of your life and the blessing you are to the Body of Christ.

Whether young or old, your presence in our fellowship is a testimony of God’s grace and faithfulness. May the Lord continue to order your steps, crown your years with His goodness, and cause His light to shine brightly upon your path.

As you celebrate today, I pray for good health, divine protection, and the abundant joy of the Lord to overflow in your life. May you grow in wisdom and in favor with both God and man, and may every new year draw you closer to your God-given purpose. 
The sovereign Lord, is your strength!!!

Happy Birthday!
With love and prayers,
Rev. Dr. Charles Akuetteh 
Head Pastor, LBC """
    send_sms_to_birthday_users(birthday_users,client_id, client_secret, sender_id, message)
    
    # for user in users:
    #     dob = user["dob"].strip()
    #     if not dob:
    #         print(f"Skipping user with empty DOB: {user}")
    #         continue
    #     if not is_valid_date(dob, "%B %d %Y"):
    #         print(f"Skipping user with invalid DOB format: {user}")
    #         continue
    #     user_birthday = datetime.strptime(dob, "%B %d %Y").strftime("%m-%d")
    #     if user_birthday != today:
    #         print(f"Skipping user with non-matching birthday: {user}")
    #         continue
    #     print(f"User with today's birthday: {user}")
    # for user in get_users_with_today_birthday(users):
    #     try:
    #         # Iterate over the list if 'user' is a list
    #         response = send_sms_to_birthday_users(users, client_id, client_secret, sender_id, message)
    #         print("Response:", response)            
    #     except Exception as e:
    #         print("Error:", e)

    # print(get_oauth_token(API))  # Test the OAuth token retrieval
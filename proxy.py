import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Email configuration (replace with your email server details)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'tsmdcltdmd@gmail.com'
EMAIL_HOST_PASSWORD = 'vfhfxsseptjklfgt'
TO_EMAILS = ['anireddysaikiran1010@gmail.com', 'jyothsnavengoti17@gmail.com']  # List of recipient emails

def fetch_count():
    url = "https://proxy6.net/en/order"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Look for the Indian flag container
    flag_container = soup.find('div', {'class': 'order-free-item', 'title': 'India (भारत)'})
    if flag_container:
        count_element = flag_container.find('span', {'class': 'label'})
        if count_element:
            count_text = count_element.get_text(strip=True)
            try:
                count = int(count_text)
                if 0 <= count <= 200:
                    return count
            except ValueError:
                pass
    return None

def send_email(count):
    subject = "Count Updated Notification"
    body = f"""
    <html>
    <body>
        <p style="font-size: 24px; font-weight: bold;">Dear User,</p>
        <p style="font-size: 36px; font-weight: bold;">India Count: {count}</p>
        <p style="font-size: 24px; font-weight: bold;">Best regards,<br>Anireddy</p>
    </body>
    </html>
    """

    message = MIMEMultipart()
    message['From'] = EMAIL_HOST_USER
    message['To'] = ', '.join(TO_EMAILS)  # Join the list of emails into a single comma-separated string
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(message)

previous_count = None

while True:
    count = fetch_count()

    if count is not None:
        if count != previous_count:
            send_email(count)
            previous_count = count
    
    time.sleep(2)  # Check every 2 seconds
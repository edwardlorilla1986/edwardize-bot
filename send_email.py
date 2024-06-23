import os
import smtplib
import logging
from openai import OpenAI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up OpenAI API key
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)
url = "https://www.merriam-webster.com/word-of-the-day"
response = requests.get(url)
word = ""
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the Word of the Day section
    word_section = soup.find('div', class_='word-and-pronunciation')
    word = word_section.find('h2').text.strip()
    
else:
    print("Failed to retrieve the Word of the Day")
def send_email(subject, body, to_email):
    from_email = os.getenv('EMAIL')
    email_password = os.getenv('EMAIL_PASSWORD')
    
    if not from_email or not email_password:
        logger.error('Email credentials are not set in the environment variables.')
        return
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, email_password)
        
        # Send the email
        server.send_message(msg)
        server.quit()
        logger.info(f'Email sent successfully to {to_email}')
    except Exception as e:
        logger.error(f'Failed to send email: {e}')

def generate_content(prompt, max_tokens=300):
    try:
        generator = pipeline('text-generation', model='gpt2', truncation=True)
        response = generator(prompt, max_length=max_tokens, pad_token_id=50256)
        return response[0]['generated_text']
    except Exception as e:
        logger.error(f'Transformers error: {e}')
        return "Content generation failed."

def sanitize_title(title):
    return ''.join(char for char in title if char.isalnum() or char.isspace()).strip()

if __name__ == '__main__':
    # List of recipient emails
    email_list = [
        os.getenv('TO_EMAIL10'), 
        os.getenv('TO_EMAIL11'), 
        os.getenv('TO_EMAIL12'), 
        os.getenv('TO_EMAIL13'), 
        os.getenv('TO_EMAIL14'),
        os.getenv('TO_EMAIL15'), 
        os.getenv('TO_EMAIL16'), 
        os.getenv('TO_EMAIL17'), 
        os.getenv('TO_EMAIL18'), 
        os.getenv('TO_EMAIL1'),
        os.getenv('TO_EMAIL8'), 
        os.getenv('TO_EMAIL9'), 
        os.getenv('TO_EMAIL7'), 
        os.getenv('TO_EMAIL2'), 
        os.getenv('TO_EMAIL3'), 
        os.getenv('TO_EMAIL4'), 
        os.getenv('TO_EMAIL5'), 
        os.getenv('TO_EMAIL6') 
    ]

    # Filter out any None values in case some email environment variables are not set
    email_list = [email for email in email_list if email]

    if not email_list:
        logger.error('No recipient emails are set in the environment variables.')
    else:
        for idx, to_email in enumerate(email_list, start=1):
            # Generate poem content
            poem_prompt = f'Write a affiliate marketing {idx}'
            poems = [generate_content(poem_prompt).strip() for _ in range(10)]
            content = "\n\n".join(poems)
            
            # Generate catchy title
            title_prompt = f'Generate a catchy title for a collection of affiliate marketing {idx}'
            title = generate_content(title_prompt, max_tokens=90)  # Shorter max_tokens for title generation
            
            # Sanitize title
            sanitized_title = sanitize_title(title)
            
            # Send email
            send_email(sanitized_title, content, to_email)

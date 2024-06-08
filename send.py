import os
import smtplib
import logging
from openai import OpenAI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from transformers import pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up OpenAI API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
    # Retrieve and split the email list from the environment variable
    email_list = os.getenv('TO_EMAILS', '').split(',')

    # Filter out any empty strings in case some email environment variables are not set
    email_list = [email.strip() for email in email_list if email.strip()]

    if not email_list:
        logger.error('No recipient emails are set in the environment variable TO_EMAILS.')
    else:
        for idx, to_email in enumerate(email_list, start=1):
            # Generate content
            prompt = f'Write an affiliate marketing {idx}'
            content = generate_content(prompt).strip()
            
            # Generate catchy title
            title_prompt = f'Generate a catchy title for a collection of affiliate marketing {idx}'
            title = generate_content(title_prompt, max_tokens=90).strip()
            
            # Sanitize title
            sanitized_title = sanitize_title(title)
            
            # Send email
            send_email(sanitized_title, content, to_email)

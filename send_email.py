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
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.error(f'OpenAI error: {e}')
        logger.info('Falling back to transformers.')
        try:
            generator = pipeline('text-generation', model='gpt2', truncation=True)
            response = generator(prompt, max_length=max_tokens, pad_token_id=50256)
            return response[0]['generated_text']
        except Exception as e:
            logger.error(f'Transformers error: {e}')
            return "Content generation failed."

if __name__ == '__main__':
    to_email1 = os.getenv('TO_EMAIL1')
    to_email2 = os.getenv('TO_EMAIL2')
    to_email3 = os.getenv('TO_EMAIL3')
    if not to_email1 or not to_email2:
        logger.error('Recipient emails are not set in the environment variables.')
    else:
        # First email
        poem_prompt1 = 'Write a poem'
        poems1 = [generate_content(poem_prompt1).strip() for _ in range(10)]
        content1 = "\n\n".join(poems1)
        
        title_prompt1 = 'Generate a title for a collection of poems'
        title1 = generate_content(title_prompt1, max_tokens=90)  # Shorter max_tokens for title generation
        
        send_email(title1, content1, to_email1)
        
        # Second email
        poem_prompt2 = 'Write another poem'
        poems2 = [generate_content(poem_prompt2).strip() for _ in range(10)]
        content2 = "\n\n".join(poems2)
        
        title_prompt2 = 'Generate a different title for another collection of poems'
        title2 = generate_content(title_prompt2, max_tokens=90)  # Shorter max_tokens for title generation
        
        send_email(title2, content2, to_email2)

        # Second email
        poem_prompt3 = 'Write another poem'
        poems3 = [generate_content(poem_prompt3).strip() for _ in range(10)]
        content3 = "\n\n".join(poems3)
        
        title_prompt3 = 'Generate a different title for another collection of poems'
        title3 = generate_content(title_prompt3, max_tokens=90)  # Shorter max_tokens for title generation
        
        send_email(title3, content3, to_email3)

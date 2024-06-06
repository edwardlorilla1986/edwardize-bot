import os
import smtplib
from transformers import pipeline
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    from_email = os.getenv('EMAIL')
    email_password = os.getenv('EMAIL_PASSWORD')
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, email_password)
    
    # Send the email
    server.send_message(msg)
    server.quit()

def generate_content(prompt):
    generator = pipeline('text-generation', model='gpt2', truncation=True)
    response = generator(prompt, max_length=300, pad_token_id=50256)
    return response[0]['generated_text']

if __name__ == '__main__':
    title_prompt = 'Write a blog post about the latest trends in technology title'
    title = generate_content(title_prompt).strip()
    prompt = 'Write a blog post about the latest trends in technology.'
    content = generate_content(prompt).strip()
    
    to_email = os.getenv('TO_EMAIL')
    send_email(title, content, to_email)

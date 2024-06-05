import os
from transformers import pipeline
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/blogger']

# Function to authenticate and get the service
def get_blogger_service():
    creds = service_account.Credentials.from_service_account_info(
        json.loads(os.getenv('CLIENT_SECRET_JSON')),
        scopes=SCOPES
    )
    service = build('blogger', 'v3', credentials=creds)
    return service

# Function to create a blog post
def create_blog_post(service, blog_id, title, content):
    post = {
        'title': title,
        'content': content
    }
    service.posts().insert(blogId=blog_id, body=post).execute()

# Function to generate content using Hugging Face's Transformers
def generate_content(prompt):
    generator = pipeline('text-generation', model='gpt2', truncation=True)
    response = generator(prompt, max_length=300, pad_token_id=50256)
    return response[0]['generated_text']

if __name__ == '__main__':
    service = get_blogger_service()
    blog_id = os.getenv('BLOG_ID')
    title = 'Automated Blog Post'
    prompt = 'Write a blog post about the latest trends in technology.'
    content = generate_content(prompt)
    create_blog_post(service, blog_id, title, content)

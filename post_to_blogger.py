import os
from transformers import pipeline
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_blogger_service():
    creds = service_account.Credentials.from_service_account_file(
        'service-account-file.json', 
        scopes=SCOPES
    )
    service = build('blogger', 'v3', credentials=creds)
    return service

def create_blog_post(service, blog_id, title, content):
    post = {
        'title': title,
        'content': content
    }
    service.posts().insert(blogId=blog_id, body=post).execute()

def generate_content(prompt):
    generator = pipeline('text-generation', model='gpt2', truncation=True)
    response = generator(prompt, max_length=300, pad_token_id=50256)
    return response[0]['generated_text']

if __name__ == '__main__':
    service = get_blogger_service()
    blog_id = os.getenv('BLOG_ID')
    title_prompt = 'Write a blog post about the latest trends in technology title'
    title = generate_content(title_prompt)
    prompt = 'Write a blog post about the latest trends in technology.'
    content = generate_content(prompt)
    create_blog_post(service, blog_id, title, content)

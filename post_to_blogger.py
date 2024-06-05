import os
from textgenrnn import textgenrnn
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Function to authenticate and get the service
def get_blogger_service():
    creds = service_account.Credentials.from_service_account_info(
        json.loads(os.getenv('CLIENT_SECRET_JSON')),
        scopes=['https://www.googleapis.com/auth/blogger']
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

# Function to generate content using textgenrnn
def generate_content(prompt):
    textgen = textgenrnn.TextgenRnn()
    # Here you can optionally train or load a pre-trained model
    generated_texts = textgen.generate(return_as_list=True, max_gen_length=300)
    return generated_texts[0]

if __name__ == '__main__':
    service = get_blogger_service()
    blog_id = os.getenv('BLOG_ID')
    title = 'Automated Blog Post'
    prompt = 'Write a blog post about the latest trends in technology.'
    content = generate_content(prompt)
    create_blog_post(service, blog_id, title, content)

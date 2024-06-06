import os
import pickle
import base64
from transformers import pipeline
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_blogger_service():
    creds = None
    token_pickle_base64 = os.getenv('TOKEN_PICKLE')
    
    if token_pickle_base64:
        token_pickle = base64.b64decode(token_pickle_base64)
        creds = pickle.loads(token_pickle)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f'Please go to this URL: {auth_url}')
            code = input('Enter the authorization code: ')
            flow.fetch_token(code=code)
            creds = flow.credentials
        with open('token.pickle', 'wb') as token_file:
            pickle.dump(creds, token_file)
        os.environ['TOKEN_PICKLE'] = base64.b64encode(pickle.dumps(creds)).decode('utf-8')
        
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

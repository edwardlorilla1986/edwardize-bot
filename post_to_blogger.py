import os
import pickle
import random
from transformers import pipeline
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/blogger']

# Define a list of topics
TOPICS = [
    "Politics in the Philippines", "Tourism in the Philippines", "Philippine festivals",
    "Global economy trends", "Climate change impact", "International relations",
    "Community events", "Local government initiatives", "Neighborhood news",
    "Startup trends", "Investment strategies", "Market analysis",
    "AI advancements", "Cybersecurity threats", "Latest gadgets",
    "Movie reviews", "Celebrity news", "Music trends",
    "Major sporting events", "Athlete profiles", "Fitness tips",
    "Space exploration", "Scientific discoveries", "Technological innovations",
    "Mental health awareness", "Fitness and wellness", "Medical breakthroughs"
]

def get_blogger_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('blogger', 'v3', credentials=creds)
    return service

def create_blog_post(service, blog_id, title, content):
    post = {
        'title': title,
        'content': content
    }
    service.posts().insert(blogId=blog_id, body=post).execute()

def generate_content(prompt, max_length=300, num_segments=4):
    generator = pipeline('text-generation', model='gpt2', truncation=True)
    content = ""
    for _ in range(num_segments):
        response = generator(prompt, max_length=max_length, pad_token_id=50256)
        content += response[0]['generated_text'] + "\n\n"
    return content

def choose_random_topic():
    topic = random.choice(TOPICS)
    return topic

if __name__ == '__main__':
    service = get_blogger_service()
    blog_id = os.getenv('BLOG_ID')
    topic = choose_random_topic()
    title_prompt = f'Create an engaging title for a blog post about {topic}'
    content_prompt = f'Write a detailed blog post about {topic}'
    title = generate_content(title_prompt, max_length=50, num_segments=1).strip()
    content = generate_content(content_prompt, max_length=300, num_segments=4).strip()
    create_blog_post(service, blog_id, title, content)

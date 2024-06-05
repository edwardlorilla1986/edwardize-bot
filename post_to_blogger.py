name: Post to Blogger

on:
  schedule:
    - cron: '0 0 * * *' # Runs every day at midnight
  workflow_dispatch:

jobs:
  post_to_blogger:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install tensorflow==2.16.1 keras textgenrnn==1.4.1 google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

    - name: Modify textgenrnn to remove multi_gpu_model import
      run: |
        python -c "import os, textgenrnn; path = os.path.join(os.path.dirname(textgenrnn.__file__), 'textgenrnn.py'); print(path)"
        sed -i 's/from tensorflow.keras.utils import multi_gpu_model/# from tensorflow.keras.utils import multi_gpu_model/' $(python -c "import os, textgenrnn; print(os.path.join(os.path.dirname(textgenrnn.__file__), 'textgenrnn.py'))")

    - name: Generate and post content
      env:
        BLOG_ID: ${{ secrets.BLOG_ID }}
        CLIENT_SECRET_JSON: ${{ secrets.CLIENT_SECRET_JSON }}
      run: |
        python post_to_blogger.py

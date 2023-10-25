
Wound Classifier Web Application

This application allows users to upload or capture a wound image and get a classification based on the provided model.

Setup and Installation

1. Clone the Repository
If you haven't already, clone the repository to your server:

```bash
git clone [URL-of-the-GitHub-repo]
cd [Name-of-the-cloned-repo]
```

2. Set Up a Virtual Environment
Using a virtual environment is recommended to avoid any package conflicts:

```bash
sudo apt-get install python3-venv
python3 -m venv woundClassifier
source woundClassifier/bin/activate
```

3. Install Required Packages
Install the necessary Python packages:

```bash
pip install Flask Flask-Session replicate gunicorn
```

4. Set Up Replicate API and Application Secrets
Before using the application, ensure you have a Replicate API key:

Register or log in to Replicate.
Navigate to the API section and generate a new API key.
Create a replicate_api.py file in the root directory of your application.
Add your Replicate API key, Flask secret key, and login password in this format:
```python
REPLICATE_API_TOKEN = "YOUR_REPLICATE_API_KEY"
SECRET_KEY = 'YOUR_FLASK_SECRET_KEY'
PASSWORD = "YOUR_LOGIN_PASSWORD"
```

Ensure replicate_api.py is added to .gitignore so that it's not committed to the repository.

5. Allow Traffic to Port 8000
Ensure port 8000 is open to accept incoming traffic:

```bash
ufw allow 8000
```

6. SSL (Optional)
If you want to secure your application with HTTPS, consider setting up an SSL certificate for your domain. This step is optional but recommended for production deployments.

7. Run the Application
To run the application and ensure it keeps running even after you close the SSH connection:

```bash
nohup gunicorn -b 0.0.0.0:8000 app:app &
```
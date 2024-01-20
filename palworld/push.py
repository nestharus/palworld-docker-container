from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# Get the value of the VERSION environment variable
version = os.getenv('VERSION')
repository = os.getenv('REPOSITORY')

os.system(f'docker-compose build')

# Use the version to tag the Docker image
os.system(f'docker tag {repository}:{version} {repository}:latest')

os.system(f'docker push {repository} --all-tags')
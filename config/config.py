import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

TENSIONS = [
    {"id": 1, "description": "Safe, Comfortable, & Compliant vs. Keeping Up with Rapid Pace of Change"},
    {"id": 2, "description": "Amplify Output Quantity vs. Amplify Output Quality"},
    {"id": 3, "description": "Innovative & Flexible Usage vs. Safe, Secure, Compliant, Unbiased Usage"},
    {"id": 4, "description": "Speedy Implementation vs. Safe Implementation"},
    {"id": 5, "description": "Goal: Maximize Reward vs. Goal: Minimize Risk"},
    {"id": 6, "description": "Short Term Gains vs. Long Term Gains"},
    {"id": 7, "description": "Efficient Governance vs. Inclusive Governance"},
    {"id": 8, "description": "Maximize Reward vs. Uphold Organization's Ethical Principles"},
    {"id": 10, "description": "Human Flourishing vs. Nature Flourishing"}
]
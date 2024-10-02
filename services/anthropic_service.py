from config.config import anthropic
import re

def clean_content(content):
    # Convert to string if it's not already
    if not isinstance(content, str):
        content = str(content)
    
    # Remove any leading/trailing whitespace
    content = content.strip()
    
    # Replace escaped newlines with actual newlines
    content = content.replace('\\n', '\n')
    
    # Remove TextBlock wrapper and type='text'
    content = re.sub(r'^\[?TextBlock\(text="|"\), type=\'text\'\]?$', '', content, flags=re.MULTILINE)
    
    # Normalize multiple consecutive newlines to a maximum of two
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content

def generate_section_content(prompt):
    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        messages=[
            {"role": "user", "content": f"{prompt}\n\nPlease format your response in HTML, using appropriate tags like <p>, <ul>, <li>, etc. for better readability."}
        ],
        max_tokens=1000
    )
    
    # Print the raw response for debugging
    print("Raw API Response:")
    print(response)
    print("\nResponse Content:")
    print(response.content)
    
    cleaned_content = clean_content(response.content[0].text)
    
    print("\nCleaned Content:")
    print(cleaned_content)
    
    return cleaned_content
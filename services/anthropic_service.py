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
    
    # Remove any TextBlock or similar wrappers
    content = re.sub(r'^\[?TextBlock\(text=\'?|\'?\)\]?$', '', content, flags=re.IGNORECASE)
    
    # Normalize multiple consecutive newlines to a maximum of two
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content

def generate_section_content(prompt):
    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return clean_content(response.content)

def generate_final_report(combined_content):
    with open("prompts/report/editor_prompt.txt", "r") as file:
        editing_prompt = file.read()

    full_prompt = f"{editing_prompt}\n\nHere's the combined content of all sections:\n\n{combined_content}"

    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=8192
    )
    return clean_content(response.content)
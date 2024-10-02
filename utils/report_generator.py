from config.config import TENSIONS
import time
import json
import os

def format_votes(vote_data):
    formatted_votes = []

    for tension in TENSIONS:
        key = f"tension_{tension['id']}"
        if key in vote_data:
            value = int(vote_data[key])
            left_aim, right_aim = tension['description'].split(" vs. ")
            formatted_vote = f"On a scale of -5 to 5, where -5 is as focused on {left_aim} as possible while still doing a bit of {right_aim}, and 5 is as focused on {right_aim} as possible while still doing a bit of {left_aim}, we're operating at {value}."
            formatted_votes.append(formatted_vote)

    return "\n".join(formatted_votes)

def load_section_index():
    with open("prompts/report/section_index.json", "r") as file:
        return json.load(file)

def get_prompts(vote_data):
    formatted_vote_data = format_votes(vote_data)
    prompts = {}
    section_index = load_section_index()

    # Provide default values for missing data
    default_data = {
        "company": vote_data.get("company", "Not provided"),
        "industry": vote_data.get("industry", "Not provided"),
        "ai_usage": vote_data.get("ai-usage", "Not provided"),
        "email": vote_data.get("email", "Not provided"),
        "formatted_vote_data": formatted_vote_data
    }

    for section_title, prompt_file in section_index.items():
        file_path = os.path.join("prompts", "report", prompt_file)
        with open(file_path, "r") as file:
            prompt_template = file.read()
            try:
                prompts[section_title] = prompt_template.format(**default_data)
            except KeyError as e:
                print(f"KeyError in {section_title} prompt: {str(e)}")
                prompts[section_title] = f"Error generating {section_title} prompt: Missing key {str(e)}"

    return prompts

def get_editor_prompt(vote_data, report_content):
    formatted_vote_data = format_votes(vote_data)
    
    # Provide default values for missing data
    default_data = {
        "company": vote_data.get("company", "Not provided"),
        "industry": vote_data.get("industry", "Not provided"),
        "ai_usage": vote_data.get("ai-usage", "Not provided"),
        "email": vote_data.get("email", "Not provided"),
        "formatted_vote_data": formatted_vote_data,
        "report_content": report_content
    }

    file_path = os.path.join("prompts", "report", "editor_prompt.txt")
    with open(file_path, "r") as file:
        prompt_template = file.read()
        try:
            editor_prompt = prompt_template.format(**default_data)
        except KeyError as e:
            print(f"KeyError in editor prompt: {str(e)}")
            editor_prompt = f"Error generating editor prompt: Missing key {str(e)}"

    return editor_prompt

def generate_report_with_progress(vote_data):
    formatted_vote_data = format_votes(vote_data)
    
    yield "Formatting vote data...", 0
    time.sleep(1)
    
    section_index = load_section_index()
    total_steps = len(section_index)
    
    for i, (section_title, _) in enumerate(section_index.items()):
        progress = ((i + 1) / total_steps) * 80  # 80% of progress for generating prompts
        yield f"Generating {section_title} prompt...", progress
        time.sleep(1)
    
    yield "Finalizing report...", 90
    time.sleep(1)

    # The actual report generation is now handled in routes/report.py
    yield "Report generation complete!", 100
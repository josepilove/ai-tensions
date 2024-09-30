from config.config import anthropic

def generate_section_content(prompt):
    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.content[0].text

def generate_final_report(combined_content):
    with open("prompts/report/editor_prompt.txt", "r") as file:
        editing_prompt = file.read()

    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8192,
        messages=[
            {
                "role": "user",
                "content": f"{editing_prompt}\n\nHere's the combined content of all sections:\n\n{combined_content}"
            }
        ]
    )
    return response.content[0].text
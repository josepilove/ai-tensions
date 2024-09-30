from config.config import TENSIONS

def format_votes(vote_data):
    formatted_votes = []
    tensions = [tension.split(" vs. ") for tension in TENSIONS]

    for i, (left_aim, right_aim) in enumerate(tensions, 1):
        key = f"tension_{i}"
        if key in vote_data:
            value = int(vote_data[key])
            formatted_vote = f"On a scale of -5 to 5, where -5 is as focused on {left_aim} as possible while still doing a bit of {right_aim}, and 5 is as focused on {right_aim} as possible while still doing a bit of {left_aim}, we're operating at {value}."
            formatted_votes.append(formatted_vote)

    return "\n".join(formatted_votes)

def get_prompts(formatted_vote_data, vote_data):
    prompts = {}
    prompt_files = [
        "summary_analysis",
        "challenges_opportunities",
#        "strategic_considerations",
        "workplace_culture",
        "governance_compliance",
#        "workforce_training",
        "next_steps"
    ]

    # Provide default values for missing data
    default_data = {
        "company": vote_data.get("company", "Not provided"),
        "industry": vote_data.get("industry", "Not provided"),
        "ai_usage": vote_data.get("ai-usage", "Not provided"),
        "email": vote_data.get("email", "Not provided")
    }

    for prompt_name in prompt_files:
        with open(f"prompts/report/{prompt_name}.txt", "r") as file:
            prompt_template = file.read()
            try:
                prompts[prompt_name] = prompt_template.format(
                    formatted_vote_data=formatted_vote_data,
                    **default_data
                )
            except KeyError as e:
                print(f"KeyError in {prompt_name} prompt: {str(e)}")
                prompts[prompt_name] = f"Error generating {prompt_name} prompt: Missing key {str(e)}"

    return prompts
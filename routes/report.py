from flask import Blueprint, jsonify, session
import traceback
from services.anthropic_service import generate_section_content, generate_final_report
from utils.report_generator import format_votes, get_prompts

report = Blueprint('report', __name__)

@report.route('/generate_report', methods=['POST'])
def generate_report():
    vote_data = session.get('vote_data', {})
    if not vote_data:
        return jsonify({"error": "No vote data found in session"}), 400

    human_readable_data = vote_data.get('human_readable', {})
    original_data = vote_data.get('original', {})

    formatted_vote_data = format_votes(human_readable_data)
    
    try:
        prompts = get_prompts(formatted_vote_data, original_data)
        
        report_sections = {}
        for section, prompt in prompts.items():
            report_sections[section] = generate_section_content(prompt)

        combined_content = "\n\n".join([f"{section.capitalize()}:\n{content}" for section, content in report_sections.items()])
        final_report = generate_final_report(combined_content)

        return jsonify({"report": {"final_report": final_report}})
    except Exception as e:
        error_message = f"An error occurred: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print(error_message)  # Log the error to the console
        return jsonify({"error": error_message}), 500
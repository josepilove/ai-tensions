from flask import Blueprint, render_template, session, Response, stream_with_context, request, jsonify
import traceback
from services.anthropic_service import generate_section_content
from utils.report_generator import generate_report_with_progress, get_prompts, load_section_index, get_editor_prompt
import json

report = Blueprint('report', __name__)

@report.route('/generate_report', methods=['GET', 'POST'])
def generate_report():
    try:
        session_vote_data = session.get('vote_data', {})
        vote_data = session_vote_data.get('human_readable', {})
        if not vote_data:
            return render_template('error.html', error="No vote data found in session"), 400

        print("\n--- Vote Data ---")
        print(json.dumps(vote_data, indent=2))
        print("--- End of Vote Data ---\n")

        # Ensure text elements are present
        text_elements = ['company', 'industry', 'ai-usage']
        for element in text_elements:
            if element not in vote_data or not vote_data[element]:
                vote_data[element] = "Not provided"
                print(f"Warning: {element} is missing or empty in vote_data")

        def generate():
            prompts = {}
            section_index = load_section_index()
            total_steps = len(section_index) * 2 + 1  # Prompts generation + Content generation + Editor prompt
            current_step = 0

            # Generate prompts
            for status, progress in generate_report_with_progress(vote_data):
                current_step += 1
                yield f"data: {json.dumps({'status': status, 'progress': min(99, (current_step / total_steps) * 100)})}\n\n"
                if status.startswith("Generating"):
                    section_title = status.split("Generating ")[1].split(" prompt")[0]
                    prompts[section_title] = get_prompts(vote_data)[section_title]

            # Generate the actual report using the prompts
            report_sections = {}
            for section_title, prompt in prompts.items():
                yield f"data: {json.dumps({'status': f'Generating content for {section_title}', 'progress': min(99, ((current_step + 0.5) / total_steps) * 100)})}\n\n"
                print(f"\n--- Generating content for {section_title} ---")
                print(f"Prompt: {prompt[:500]}...")  # Print the first 500 characters of the prompt
                section_content = generate_section_content(prompt, vote_data)
                report_sections[section_title] = section_content
                current_step += 1
                yield f"data: {json.dumps({'status': f'Generated {section_title} section', 'progress': min(99, (current_step / total_steps) * 100)})}\n\n"

            # Render the report template with the generated content
            rendered_report = render_template('report_template.html', report_content=report_sections)

            # Generate editor prompt
            yield f"data: {json.dumps({'status': 'Generating editor prompt', 'progress': 99})}\n\n"
            editor_prompt = get_editor_prompt(vote_data, rendered_report)

            # Store the editor prompt in the session for later use
            session['editor_prompt'] = editor_prompt

            yield f"data: {json.dumps({'status': 'complete', 'progress': 100, 'report': rendered_report})}\n\n"

        return Response(stream_with_context(generate()), content_type='text/event-stream')
    except Exception as e:
        error_message = f"An error occurred while generating the report: {str(e)}"
        print(f"{error_message}\n\nTraceback:\n{traceback.format_exc()}")
        return render_template('error.html', error=error_message), 500

@report.route('/report_template')
def report_template():
    return render_template('report_template.html')

@report.route('/get_editor_prompt')
def get_stored_editor_prompt():
    editor_prompt = session.get('editor_prompt', '')
    return jsonify({'editor_prompt': editor_prompt})
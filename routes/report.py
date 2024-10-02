from flask import Blueprint, render_template, session, Response, stream_with_context, request, jsonify
import traceback
from services.anthropic_service import generate_section_content
from utils.report_generator import generate_report_with_progress, get_prompts, load_section_index, get_editor_prompt
import json

report = Blueprint('report', __name__)

@report.route('/generate_report', methods=['GET', 'POST'])
def generate_report():
    try:
        vote_data = session.get('vote_data', {})
        if not vote_data:
            return render_template('error.html', error="No vote data found in session"), 400

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
                section_content = generate_section_content(prompt)
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
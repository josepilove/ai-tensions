from flask import Blueprint, render_template, session, Response, stream_with_context, request, jsonify
import traceback
from services.anthropic_service import generate_section_content
from utils.report_generator import generate_report_with_progress, get_prompts
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
            for status, progress in generate_report_with_progress(vote_data):
                yield f"data: {json.dumps({'status': status, 'progress': progress})}\n\n"
                if status.startswith("Generating"):
                    prompt_name = status.split("Generating ")[1].split(" prompt")[0].replace(" ", "_")
                    prompts[prompt_name] = get_prompts(vote_data)[prompt_name]

            # Generate the actual report using the prompts
            report_sections = {}
            for section_name, prompt in prompts.items():
                section_content = generate_section_content(prompt)
                report_sections[section_name] = section_content
                yield f"data: {json.dumps({'status': f'Generated {section_name} section', 'progress': 90})}\n\n"

            # Render the report template with the generated content
            rendered_report = render_template('report_template.html', report_content=report_sections)
            yield f"data: {json.dumps({'status': 'complete', 'report': rendered_report})}\n\n"

        return Response(stream_with_context(generate()), content_type='text/event-stream')
    except Exception as e:
        error_message = f"An error occurred while generating the report: {str(e)}"
        print(f"{error_message}\n\nTraceback:\n{traceback.format_exc()}")
        return render_template('error.html', error=error_message), 500

@report.route('/report_template')
def report_template():
    return render_template('report_template.html')
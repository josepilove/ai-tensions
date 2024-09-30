from flask import Blueprint, render_template, request, session
from config.config import TENSIONS

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', tensions=TENSIONS)

@main.route('/confirmation', methods=['POST'])
def confirmation():
    original_vote_data = request.form.to_dict()
    
    # Create new dictionaries for processed data
    vote_data = {}
    human_readable_data = {}
    
    # Process the form data
    for key, value in original_vote_data.items():
        if key.startswith('tension'):
            tension_number = key[7:]  # Get the number after 'tension'
            original_value = int(value)
            human_readable_value = original_value - 6
            vote_data[f'tension_{tension_number}'] = str(original_value)
            human_readable_data[f'tension_{tension_number}'] = str(human_readable_value)
        else:
            vote_data[key] = value
            human_readable_data[key] = value
    
    # Store both original and human-readable data in the session
    session['vote_data'] = {
        'original': vote_data,
        'human_readable': human_readable_data
    }
    
    return render_template('confirmation.html', 
                           vote_data=vote_data, 
                           human_readable_data=human_readable_data, 
                           tensions=TENSIONS)
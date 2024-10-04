# Variables Reference for Report Prompts

The following variables are available for use in the report prompts. Each variable is accompanied by an example of the data it might contain:

1. `{formatted_vote_data}`: A formatted string containing the tension balances for each AI tension. Each line represents a tension and its corresponding vote.

Example:
```
On a scale of -5 to 5, where -5 is as focused on Safe, Comfortable, & Compliant as possible while still doing a bit of Keeping Up with Rapid Pace of Change, and 5 is as focused on Keeping Up with Rapid Pace of Change as possible while still doing a bit of Safe, Comfortable, & Compliant, we're operating at 2.
On a scale of -5 to 5, where -5 is as focused on Amplify Output Quantity as possible while still doing a bit of Amplify Output Quality, and 5 is as focused on Amplify Output Quality as possible while still doing a bit of Amplify Output Quantity, we're operating at -3.
On a scale of -5 to 5, where -5 is as focused on Innovative & Flexible Usage as possible while still doing a bit of Safe, Secure, Compliant, Unbiased Usage, and 5 is as focused on Safe, Secure, Compliant, Unbiased Usage as possible while still doing a bit of Innovative & Flexible Usage, we're operating at 1.
```

2. `{vote_data}`: A dictionary containing various pieces of information about the organization and the tension votes.

Example:
```python
{
    'company': 'TechCorp',
    'industry': 'Software Development',
    'ai-usage': 'We plan to use AI for automating code reviews and optimizing our development pipeline.',
    'email': 'contact@techcorp.com',
    'tension_1': 2,
    'tension_2': -3,
    'tension_3': 1,
    'tension_4': 0,
    'tension_5': -2,
    'tension_6': 4,
    'tension_7': -1,
    'tension_8': 3,
    'tension_10': 2
}
```

Accessing individual items:
- `{company}` or `{vote_data.get('company', 'Not provided')}` might return: `TechCorp`
- `{industry}` or `{vote_data.get('industry', 'Not provided')}` might return: `Software Development`
- `{ai_usage}` or `{vote_data.get('ai-usage', 'Not provided')}` might return: `We plan to use AI for automating code reviews and optimizing our development pipeline.`
- `{email}` or `{vote_data.get('email', 'Not provided')}` might return: `contact@techcorp.com`

3. `{TENSIONS}`: A list of tension pairs, each represented as a dictionary with 'id' and 'description' keys. This is imported from the config file.

Example:
```python
[
    {"id": 1, "description": "Safe, Comfortable, & Compliant vs. Keeping Up with Rapid Pace of Change"},
    {"id": 2, "description": "Amplify Output Quantity vs. Amplify Output Quality"},
    {"id": 3, "description": "Innovative & Flexible Usage vs. Safe, Secure, Compliant, Unbiased Usage"},
    {"id": 4, "description": "Speedy Implementation vs. Safe Implementation"},
    {"id": 5, "description": "Goal: Maximize Reward vs. Goal: Minimize Risk"},
    {"id": 6, "description": "Short Term Gains vs. Long Term Gains"},
    {"id": 7, "description": "Efficient Governance vs. Inclusive Governance"},
    {"id": 8, "description": "Maximize Reward vs. Uphold Organization's Ethical Principles"},
    {"id": 10, "description": "Human Flourishing vs. Nature Flourishing"}
]
```

4. `{report_content}`: This variable is used in the editor prompt and contains the generated report content that needs to be edited.

Note: The actual values for these variables will be populated at runtime when generating the report. The examples above are illustrative and show the structure and type of data you can expect for each variable.

When using these variables in prompts, make sure to use the correct format:
- For direct access: `{variable_name}`
- For dictionary access with a default value: `{vote_data.get('key', 'Default Value')}`

Remember that the `format_votes` function in `utils/report_generator.py` creates the `formatted_vote_data` string, which formats each tension vote into a human-readable sentence.
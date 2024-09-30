# Variables Reference for Report Prompts

The following variables are available for use in the report prompts. Each variable is accompanied by an example of the data it might contain:

1. `{formatted_vote_data}`: A formatted string containing the tension balances for each AI tension. Each line represents a tension and its corresponding vote.

Example:
```
On a scale of -5 to 5, where -5 is as focused on Speed as possible while still doing a bit of Accuracy, and 5 is as focused on Accuracy as possible while still doing a bit of Speed, we're operating at 2.
On a scale of -5 to 5, where -5 is as focused on Automation as possible while still doing a bit of Human Control, and 5 is as focused on Human Control as possible while still doing a bit of Automation, we're operating at -3.
On a scale of -5 to 5, where -5 is as focused on Innovation as possible while still doing a bit of Reliability, and 5 is as focused on Reliability as possible while still doing a bit of Innovation, we're operating at 1.
```

2. `{vote_data}`: A dictionary containing various pieces of information about the organization.

Example:
```python
{
    'company': 'TechCorp',
    'industry': 'Software Development',
    'ai-usage': 'We plan to use AI for automating code reviews and optimizing our development pipeline.',
    'email': 'contact@techcorp.com',
    'tension_1': 2,
    'tension_2': -3,
    'tension_3': 1
}
```

Accessing individual items:
- `{company}` or `{vote_data.get('company', 'Not provided')}` might return: `TechCorp`
- `{industry}` or `{vote_data.get('industry', 'Not provided')}` might return: `Software Development`
- `{ai_usage}` or `{vote_data.get('ai-usage', 'Not provided')}` might return: `We plan to use AI for automating code reviews and optimizing our development pipeline.`
- `{email}` or `{vote_data.get('email', 'Not provided')}` might return: `contact@techcorp.com`

3. `{TENSIONS}`: A list of tension pairs, each represented as a string in the format "Left Aim vs. Right Aim". This is imported from the config file.

Example:
```python
[
    "Speed vs. Accuracy",
    "Automation vs. Human Control",
    "Innovation vs. Reliability"
]
```

Note: The actual values for these variables will be populated at runtime when generating the report. The examples above are illustrative and show the structure and type of data you can expect for each variable.
from langsmith import traceable
from react import get_client
client = get_client()
@traceable
def format_prompt(user_prompt):
    return [
        {
            'role' : 'system',
            'content' : 'You are a helpful assistant.'
        },
        {
            'role' : 'user',
            'content' : f'Generate three good names for an online store that sells {user_prompt}.'
        }
    ]
@traceable(run_type='llm')
def invoke_llm(messages):
    return client.invoke(
        messages    
    )
@traceable
def run_pipeline():
    messages = format_prompt('origami paper')
    response = invoke_llm(messages)
    return response
run_pipeline()
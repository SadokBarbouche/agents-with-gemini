from .react_agent import Agent
from .react_prompt import prompt
import re
from .tools import known_actions

# Manual
# abot = Agent(prompt)
# result = abot("How much does a toy poodle weigh?")
# print(result)
# next_prompt = "Observation: {}".format(result)
# result = abot(next_prompt)
# print(result)

action_re = re.compile('^Action: (\w+): (.*)$')


def query(question, max_turns=5):
    i = 0
    bot = Agent(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [
            action_re.match(a) 
            for a in result.split('\n') 
            if action_re.match(a)
        ]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return
        
question = """I have 2 dogs, a border collie and a scottish terrier. \
What is their combined weight"""
query(question)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

from react import get_client

generation_prompt = ChatPromptTemplate.from_messages([
    (
        'system',
        '''You are a twitter expert assigned to craft outstanding tweets.
        Generate the most engaging and impactful tweet possible based on the user's request.
        If the user provides feedback, refine and enhance your previous attemps accordingly for maximum engagement.'''
    ),
    MessagesPlaceholder(variable_name='messages')
])

llm = get_client()

generation_chain =  generation_prompt | llm | StrOutputParser()

tweet = ''
request = HumanMessage(
    content="El Kef, Tunisia"
)
for chunk in generation_chain.stream(
    {
        'messages': [request]
    }
):
    print(chunk, end="")
    tweet += chunk
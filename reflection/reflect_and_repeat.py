from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from react import get_client
from langchain_core.output_parsers import StrOutputParser
from reflection.generate import request, generation_chain

tweet = "Immerse yourself in the captivating tapestry of El Kef, Tunisia! 🏰 Explore ancient ruins that tell tales of bygone eras, wander through vibrant souks bursting with local treasures, and savor the delectable flavors of traditional cuisine. #ElKef #TunisiaUnveiled #CulturalImmersion"

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            '''You are a twitter influencer known for engaging content and sharp insights.
            Review and critique the user's tweet.
            Provide constructive feedback, focusing on enhancing its depth, style, and overall impact.
            Offer specific suggestions to make the tweet more compelling and engaging for their audience.'''
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

llm = get_client()

reflection_chain = reflection_prompt | llm | StrOutputParser()

if __name__ == '__main__':

    reflection = ''

    for chunk in reflection_chain.stream(
        {
            'messages' : [request, HumanMessage(content=tweet)]
        }
    ):
        print(chunk, end="")
        reflection += chunk

    print("\n")
    print("-" * 50)

    for chunk in generation_chain.stream(
        {
            'messages': [request, AIMessage(content=tweet), HumanMessage(content=reflection)]
        }
    ):
        print(chunk, end="")
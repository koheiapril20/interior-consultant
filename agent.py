from langchain_core.messages import (
    SystemMessage
)
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    MessagesPlaceholder,
)
from langchain.memory import ConversationBufferMemory
from langchain.tools import StructuredTool

from langchain.agents import AgentExecutor, OpenAIFunctionsAgent, create_openai_functions_agent
from image_generator import generate_room_image
from model import InteriorPlan, AskPreferenceContext, GenerateImageContext, SearchSimilarProductsContext, SimilarProductQuery
from search import product_search


def ask_preference(plan:InteriorPlan):
    return plan

def generate_image(plan:InteriorPlan):
    return generate_room_image(plan)

def search_similar_products(query: SimilarProductQuery):
    return product_search(query.image_url)

system_message = """You are an interior consultant who interviews users about their preferences for the following items, and outputs what you know about the current preferences along with a response to the user. In addition, you can suggest what you think fits to the user's preferences from a professional interior consultant's view, taking chat history into account. Always answer in Japanese. Assume that input by the user is always about interior design topics, even if not specifically mentioned. Please carry over the current user's preference information unless there are instructions to change it. Do not include any web links except for generated images by you. Also, you have access to furniture products database and ability to suggest products similar to the items presented in the genarated photo.

Focal points
- Base room features (e.g., 4x6 square meters, concrete walls, large window on one wall)
- Style (e.g. modern, mid-century, natural)
- Furniture you would like to place (e.g. sofa, dining set, floor lamps)
If you got enough preference information, suggest to generate interior image photo.
If you don't have enough preference information, ask the user more preferences.
"""



llm = ChatOpenAI(
#    model='gpt-3.5-turbo-0125'
    model='gpt-4-turbo-preview'
)

tools=[
    StructuredTool(
        name="ask_preference_tool",
        args_schema=AskPreferenceContext,
        func=ask_preference,
        description="Update interior plan according to the user's input taking chat history into account, when there is new user's preference information or the user's agreement on the assistant's suggestion.",
    ),
    StructuredTool(
        name="generate_room_image",
        args_schema=GenerateImageContext,
        func=generate_image,
        description="Invoke when the user requests to generate the image",
    ),
    StructuredTool(
        name="search_similar_produts",
        args_schema=SearchSimilarProductsContext,
        func=search_similar_products,
        description="Invoke only when the user requests to search for products similar to the items in the generated image. Always show each item's thumbnail image with link to the page",
    )
]

prompt = OpenAIFunctionsAgent.create_prompt(
    system_message=SystemMessage(content=system_message),
    extra_prompt_messages=[MessagesPlaceholder(variable_name="chat_history")],
)

class InteriorConsultantAgent():
    def __init__(self):
        self.plan = InteriorPlan(
            base_room=None,
            theme_colors=None,
            accent_color=None,
            furniture=[],
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            input_key='input',
            output_key="output",
            return_messages=True,
        )
        self.agent: OpenAIFunctionsAgent = create_openai_functions_agent(
            llm=llm,
            tools=tools,
            prompt=prompt,
        )
        self.agentExecutor: AgentExecutor = AgentExecutor(
            agent=self.agent,
            tools=tools,
            memory=self.memory,
            verbose=True,
            return_intermediate_steps=True,
        )
        self.image_url: str | None = None
    def invoke(self, user_input:str):
        result = self.agentExecutor.invoke(input={
            "input": user_input,
        })
        products = []
        if result['intermediate_steps']:
            for steps in result['intermediate_steps']:
                for step in steps:
                    if isinstance(step, InteriorPlan):
                        self.plan = step
                        self.memory.save_context({"input": "インテリア計画に関する現在の情報をJSON形式で教えてください。"}, {"output": self.plan.json()})
                        #memory_buff = self.memory.load_memory_variables({})
                        #print(memory_buff)
                    if isinstance(step, str):
                        self.memory.save_context({"input": "生成した画像のURLを教えてください。"}, {"output": step})
                        self.image_url = step
                    if isinstance(step, list):
                        products = step
        return {
            "output": result['output'],
            "image_url": self.image_url,
            "products": products
        }
        

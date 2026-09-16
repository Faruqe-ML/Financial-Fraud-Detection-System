from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from .prompts import system_prompt
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri(
    "mysql+pymysql://root:12345678@localhost:3306/financial_fraud_db"
)

model = ChatGroq(
    model="openai/gpt-oss-20b"
)

toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model
)

toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model
)

tools = toolkit.get_tools()



memory = InMemorySaver()

agent = create_agent(
    model=model,
    tools=tools,
    checkpointer=memory,
    system_prompt=system_prompt
)

def ask_chatbot(prompt, thread_id="1"):

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        {
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    result = response["messages"][-1].content

    return result

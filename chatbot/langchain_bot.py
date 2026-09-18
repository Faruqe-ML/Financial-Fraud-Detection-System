import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from .prompts import system_prompt
from langchain_community.utilities import SQLDatabase

db_user = quote_plus(os.getenv("DB_USER", "root"))
db_password = quote_plus(os.getenv("DB_PASSWORD", ""))
db_host = os.getenv("DB_HOST", "127.0.0.1")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME", "financialfraud")

db = SQLDatabase.from_uri(
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

model = ChatGroq(
    model="openai/gpt-oss-20b"
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

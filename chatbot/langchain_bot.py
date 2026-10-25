
import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL

from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

from .prompts import system_prompt

load_dotenv()

# Database configuration
db_user = os.getenv("DB_USER", "fraud_app")
db_password = os.environ["DB_PASSWORD"]
db_name = os.getenv("DB_NAME", "financial_fraud_db")

if os.getenv("CLOUD_RUN", "false").lower() == "true":
    # Cloud Run + Cloud SQL
    connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

    db_uri = URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_password,
        host="localhost",
        database=db_name,
        query={
            "unix_socket": f"/cloudsql/{connection_name}"
        },
    )
else:
    # Local development
    db_uri = URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_password,
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=db_name,
    )

# Create database connection
db = SQLDatabase.from_uri(db_uri)

# LLM configuration
model = ChatGroq(
    model="openai/gpt-oss-20b"
)

# SQL tools
toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model
)

tools = toolkit.get_tools()

# Conversation memory
memory = InMemorySaver()

# Create agent
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

    return response["messages"][-1].content

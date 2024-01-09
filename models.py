from typing import Any, Dict, List, Optional, Union
import os
from langchain_experimental.agents.agent_toolkits import create_csv_agent

# from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

# from langchain.chat_models import ChatOpenAI
# import requests
import os


os.environ["GOOGLE_API_KEY"] = "AIzaSyBv6A0mzzKHry7TbT6xInbRjRgu9H8_P5o"
llm = ChatGoogleGenerativeAI(model="gemini-pro")


def initializeAgent(csv_filename):
    return create_csv_agent(llm, csv_filename, verbose=True)


# import langchain type definitons

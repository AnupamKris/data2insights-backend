from typing import Any, Dict, List, Optional, Union
import os
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = "<put your openai key here>"


def initializeAgent():
    return create_csv_agent(OpenAI(temperature=0),
                            'data.csv',
                            verbose=True)


# import langchain type definitons

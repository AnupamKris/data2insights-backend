import pandas as pd
from typing import Any, Dict, List, Optional, Union
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from models import initializeAgent
app = Flask(__name__)
CORS(app)

actionss = []
file = ''
agent = None

df = None


class BaseCallbackHandler:
    """Base callback handler that can be used to handle callbacks from langchain."""
    # add ignore_agent property
    # add ignore_tool property
    # add ignore_chain property
    # add ignore_llm property

    # def __init__(self, actionss):
    #     self.actionss = actionss

    @property
    def ignore_agent(self) -> bool:
        """Ignore agent callbacks."""
        return False

    @property
    def ignore_tool(self) -> bool:
        """Ignore tool callbacks."""
        return False

    @property
    def ignore_chain(self) -> bool:
        """Ignore chain callbacks."""
        return False

    @property
    def ignore_llm(self) -> bool:
        """Ignore LLM callbacks."""
        return False

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""

    def on_llm_end(self, response, **kwargs: Any) -> Any:
        """Run when LLM ends running."""

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""

    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when chain errors."""

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running."""

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        """Run when tool ends running."""

    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when tool errors."""

    def on_text(self, text: str, **kwargs: Any) -> Any:
        """Run on arbitrary text."""

    def on_agent_action(self, action, **kwargs: Any) -> Any:
        """Run on agent action."""
        print("action")
        print(action)
        global actionss
        actionss.append(action)
        print(action[1])
        print(action["text"])

    def on_agent_finish(self, finish, **kwargs: Any) -> Any:
        """Run on agent end."""


@app.route('/getInference', methods=['POST'])
def getInference():
    data = request.get_json()
    print(data)
    global agent
    out = agent.run(data['message'],  callbacks=[BaseCallbackHandler()])
    print(actionss)
    while len(actionss) < 1:
        print(".", end="")
    mainAction1 = actionss.pop()
    mainAction = mainAction1[1]
    # print("main  ", mainAction1, "part \n\n\n\n", mainAction)

    # mainAction = "plot"
    # out = "out"
    if "plot" in mainAction:
        plot = eval(mainAction)
        plot.get_figure().savefig('plot.png')
        return send_file('plot.png', mimetype='image/png')
    else:
        return jsonify({'message': out})


@app.route('/uploadFile', methods=['POST'])
def uploadFile():
    data = request.files
    file = data['file']
    file.save('data.csv')
    global agent
    agent = initializeAgent()
    global df
    df = pd.read_csv('data.csv')
    return jsonify({'status': '200'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

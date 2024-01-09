import pandas as pd
from typing import Any, Dict, List, Optional, Union
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from models import initializeAgent

app = Flask(__name__)
CORS(app)

actionss = []
file = ""
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

    @property
    def ignore_chat_model(self) -> bool:
        """Ignore chat model callbacks."""
        return False

    @property
    def raise_error(self) -> bool:
        """Whether to raise an error on callback failure."""
        return False


@app.route("/getInference", methods=["POST"])
def getInference():
    data = request.get_json()
    print(data)
    global agent
    callback_handler = BaseCallbackHandler()
    out = agent.run(data["message"])  # , callbacks=[callback_handler])
    # print(actionss)
    # while len(actionss) < 1:
    #     print(".", end="")
    # mainAction1 = actionss.pop()
    # mainAction = mainAction1[1]
    # # print("main  ", mainAction1, "part \n\n\n\n", mainAction)

    # # mainAction = "plot"
    # # out = "out"
    # if "plot" in mainAction:
    #     plot = eval(mainAction)
    #     plot.get_figure().savefig('plot.png')
    #     return send_file('plot.png', mimetype='image/png')
    # else:
    return jsonify({"message": out})


import os

ALLOWED_EXTENSIONS = {"csv", "xlsx"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploadFile", methods=["POST"])
def uploadFile():
    global df

    data = request.files
    file = data["file"]

    if file and allowed_file(file.filename):
        # Save the uploaded file with a unique name
        base_filename, file_extension = os.path.splitext(file.filename)
        print(base_filename, file_extension)
        unique_filename = f"data{file_extension}"
        file.save(unique_filename)

        # Convert XLSX to CSV if the uploaded file is an XLSX file
        if file_extension.lower() == ".xlsx":
            csv_filename = f"data.csv"
            df = pd.read_excel(unique_filename)
            df.to_csv(csv_filename, index=False)
        else:
            csv_filename = unique_filename

        global agent
        agent = initializeAgent(csv_filename)
        df = pd.read_csv(csv_filename)
        print("Uploaded...")
        return jsonify({"status": "200"})
    else:
        return jsonify({"error": "Invalid file format. Allowed formats: CSV, XLSX"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)

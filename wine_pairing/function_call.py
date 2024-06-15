"""
https://platform.openai.com/docs/guides/function-calling

"""
import os

from langchain_openai import ChatOpenAI
from langchain.globals import set_verbose, set_debug
from dotenv import load_dotenv

load_dotenv()

set_debug(True)
set_verbose(True)

# 환경 변수 읽기
llm = ChatOpenAI(model='gpt-4o', api_key=os.getenv('OPENAI_API_KEY'), temperature=0, max_tokens=4096)

json_schema = {
    "title": "joke",
    "description": "Joke to tell user.",
    "type": "object",
    "properties": {
        "setup": {
            "type": "string",
            "description": "The setup of the joke",
        },
        "punchline": {
            "type": "string",
            "description": "The punchline to the joke",
        },
        "rating": {
            "type": "integer",
            "description": "How funny the joke is, from 1 to 10",
        },
    },
    "required": ["setup", "punchline"],
}
structured_llm = llm.with_structured_output(json_schema)

structured_llm.invoke("Tell me a joke about cats")
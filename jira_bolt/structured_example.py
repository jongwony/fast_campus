import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()


class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")


model = ChatOpenAI(model="gpt-4o", api_key=os.environ["OPENAI_API_KEY"])
structured_llm = model.with_structured_output(Joke)
structured_llm.invoke("Tell me a joke about cats")

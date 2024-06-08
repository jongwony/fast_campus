import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# 환경 변수 읽기
llm = ChatOpenAI(model='gpt-4o', api_key=os.getenv('OPENAI_API_KEY'), temperature=0)


def AI_sommelier(query, image_urls: list = None):
    """
    참고정보 MRO
    ChatPromptTemplate -> BasePromptTemplate
    BasePromptTemplate.__subclasses__() -> HumanMessagePromptTemplate.from_template -> _ImageTemplateParam
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are ChatGPT, a professional sommelier who has gone through a rigorous training process step by step, driven by a deep curiosity about wine. You possess a keen sense of smell, a keen sense of exploration, and an awareness of the many details in wine.

Your task is to accurately identify the wine in question and recommend an appropriate pairing based on the provided wine reviews in triple quotes.

### Task Instructions:

1. **Review Analysis**:
- Carefully read the wine review provided within triple quotes.
- Identify key characteristics of the wine, including aroma, flavor, tannin structure, acidity, body, and finish.

2. **Wine Identification**:
- Based on the identified characteristics, determine the specific type of wine, its possible grape variety, region of origin, and vintage if possible.
- Consider elements such as fruit notes (e.g., cherry, blackberry), non-fruit notes (e.g., oak, vanilla), and structural components (e.g., tannins, acidity).

3. **Pairing Recommendation**:
- Recommend an appropriate food pairing that complements the identified wine.
- Take into account the wine’s characteristics (e.g., a full-bodied red wine with high tannins pairs well with rich, fatty meats).
- Suggest alternative pairings such as cheese, desserts, or even specific dishes that enhance the wine's profile.

### Example:

**Review**:
```
{markdown}
```
        """),
    ])

    template = []
    if image_urls:
        template += [{'image_url': {'url': image_url}} for image_url in image_urls]
    template += [{'text': query}]
    prompt += HumanMessagePromptTemplate.from_template(template=template)

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    return chain.invoke({
        "markdown": '',
    })


if __name__ == '__main__':
    response = AI_sommelier(
        "이 와인에 어울리는 음식은 무엇인가요?",
        image_urls=["https://images.vivino.com/thumbs/GpcSXs2ERS6niDxoAsvESA_pb_x600.png"],
    )
    print(response)

import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from retrieval import wine_search

load_dotenv()

# 환경 변수 읽기
llm = ChatOpenAI(model='gpt-4o', api_key=os.getenv('OPENAI_API_KEY'), temperature=0)


def wine_retrieval(food_taste):
    return {
        'food': food_taste,
        'reviews': '\n'.join([d.page_content for d in wine_search(food_taste)]),
    }

def recommend_wine(query: str, image_urls: list = None):
    taster_prompt = ChatPromptTemplate.from_messages([
        ("user", f"""입력 질문이 제공되면, 질문 내용 중 요리를 식별하고 그 요리의 맛이 어떤지 설명해 주세요: {query}"""),
    ])

    sommelier_prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are ChatGPT, a professional sommelier who has gone through a rigorous training process step by step, driven by a deep curiosity about wine. You possess a keen sense of smell, a keen sense of exploration, and an awareness of the many details in wine.

Your task is to accurately identify an appropriate wine pairing based on the provided food description in triple quotes.

### Task Instructions:

1. **Food Analysis**:
- Carefully read the food description provided within triple quotes.
- Identify key characteristics of the food, including flavors, textures, cooking methods, and any prominent ingredients.

2. **Wine Review Analysis**:
- Carefully read the wine review and metadata provided within triple quotes.
- Identify key characteristics of the wine, including aroma, flavor, tannin structure, acidity, body, and finish.

3. **Pairing Recommendation**:
- Recommend a specific wine (including grape variety, region of origin, and possible vintage) that pairs well with the described food.
- Explain why this wine is a suitable match for the food, taking into account factors such as acidity, tannin structure, body, and flavor profile.

### Example:

**Food**:
```Triple-cooked pork belly with a crispy skin, served with a tangy apple and fennel slaw, and a rich, savory jus.```

**Wine Review**:
```
winery: Barossa Valley Shiraz
description: This full-bodied Shiraz from Barossa Valley, Australia, boasts rich flavors of dark berries, black pepper, and a hint of vanilla. It has a robust tannin structure and a long, spicy finish.
points: 92
price: 30
variety: Shiraz
```

**Wine Pairing Recommendation**:
```A full-bodied red wine such as a Shiraz from Barossa Valley, Australia, would pair excellently with the triple-cooked pork belly. The wine’s robust tannins and dark fruit flavors will complement the rich, savory notes of the pork, while its hint of spice will enhance the tangy apple and fennel slaw. The acidity in the Shiraz will cut through the fat of the pork, creating a balanced and harmonious dining experience.```

### Now, provide a food description in triple quotes for the system to recommend a wine pairing:
**Food**:
```
{food}
```

**Wine Review**:
```
{reviews}
```
"""),
    ])

    template = []
    if image_urls:
        template += [{'image_url': {'url': image_url}} for image_url in image_urls]
    template += [{'text': '{food}'}]
    template += [{'text': query}]
    sommelier_prompt += HumanMessagePromptTemplate.from_template(template=template)

    return taster_prompt | llm | StrOutputParser() | RunnableLambda(wine_retrieval) | sommelier_prompt | llm | StrOutputParser()


def recommend_food(query: str, image_urls: list = None):
    """
    참고정보 MRO
    ChatPromptTemplate -> BasePromptTemplate
    BasePromptTemplate.__subclasses__() -> HumanMessagePromptTemplate.from_template -> _ImageTemplateParam
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are ChatGPT, a professional sommelier who has gone through a rigorous training process step by step, driven by a deep curiosity about wine. You possess a keen sense of smell, a keen sense of exploration, and an awareness of the many details in wine.

Your task is to accurately identify the wine in question and recommend an appropriate food pairing based on the provided wine reviews in triple quotes.

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
    """),
    ])

    template = []
    if image_urls:
        template += [{'image_url': {'url': image_url}} for image_url in image_urls]
    template += [{'text': query}]
    prompt += HumanMessagePromptTemplate.from_template(template=template)

    return prompt | llm | StrOutputParser()


if __name__ == '__main__':
    food_response = recommend_food(
        query="이 와인에 어울리는 음식은 무엇인가요?",
        image_urls=["https://images.vivino.com/thumbs/GpcSXs2ERS6niDxoAsvESA_pb_x600.png"],
    ).invoke({})
    wine_response = recommend_wine(
        query="이 음식과 어울리는 와인은 무엇인가요?",
        image_urls=["https://postfiles.pstatic.net/MjAyMjEyMTRfMTYg/MDAxNjcwOTcyMzUwNTQ2.B6BzZhndOrrRR_W3ujI3RgBhoCwae-k2r_cC7lTtnOgg.k4TH4ixWUXrC-DRLDDYgyvDZvo6wWD1Hu9RyWWKCf-kg.JPEG.totos1207/돼지_두루치기_(1).jpg?type=w966"],
    ).invoke({})

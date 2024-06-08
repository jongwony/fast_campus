import os

from openai import OpenAI
from dotenv import load_dotenv

from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def openai_response(query, image_urls=None):
    """
    참고정보
    https://python.langchain.com/v0.2/docs/how_to/lcel_cheatsheet/#get-all-prompts-in-a-chain
    """
    if image_urls:
        content = [
            {"type": "image_url", "image_url": {"url": image_url}}
            for image_url in image_urls
        ]
    content += [{"type": "text", "text": query}]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are ChatGPT, a professional sommelier who has gone through a rigorous training process step by step, driven by a deep curiosity about wine. You possess a keen sense of smell, a keen sense of exploration, and an awareness of the many details in wine.\n\nYour task is to accurately identify the wine in question and recommend an appropriate pairing based on the provided wine reviews in triple quotes.\n\n### Task Instructions:\n\n1. **Review Analysis**:\n   - Carefully read the wine review provided within triple quotes.\n   - Identify key characteristics of the wine, including aroma, flavor, tannin structure, acidity, body, and finish.\n\n2. **Wine Identification**:\n   - Based on the identified characteristics, determine the specific type of wine, its possible grape variety, region of origin, and vintage if possible.\n   - Consider elements such as fruit notes (e.g., cherry, blackberry), non-fruit notes (e.g., oak, vanilla), and structural components (e.g., tannins, acidity).\n\n3. **Pairing Recommendation**:\n   - Recommend an appropriate food pairing that complements the identified wine.\n   - Take into account the wine’s characteristics (e.g., a full-bodied red wine with high tannins pairs well with rich, fatty meats).\n   - Suggest alternative pairings such as cheese, desserts, or even specific dishes that enhance the wine's profile.\n\n### Example:\n\n**Review**:\n```{markdown}"
                }
            ]
            },
            {
                "role": "user",
                "content": content
            }
        ],
        temperature=0,
        max_tokens=4095,
        top_p=0,
        frequency_penalty=0,
        presence_penalty=0
    )
    return ''.join([c.message.content for c in response.choices])


def AI_sommelier(query, image_urls=None):
    runnable = RunnableLambda(openai_response)
    bound_runnable = runnable.bind(image_urls=image_urls)
    chain = bound_runnable | StrOutputParser()
    return chain.invoke(query)


if __name__ == '__main__':
    response = AI_sommelier(
        "이 와인에 어울리는 음식은 무엇인가요?",
        image_urls=["https://images.vivino.com/thumbs/GpcSXs2ERS6niDxoAsvESA_pb_x600.png"],
    )
    print(response)

from langchain_mistralai import ChatMistralAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import settings

CONTACT_INFO = """
Mistral AI Contact Information:
- Website: https://mistral.ai
- General Inquiries: contact@mistral.ai
- Media/Press: press@mistral.ai
- LinkedIn: https://www.linkedin.com/company/mistral-ai
- X (Twitter): @MistralAI
- Discord Community: https://discord.gg/mistralai

Key Decision Makers:
- Arthur Mensch (CEO & Co-founder) - Based in Paris, France
- Guillaume Lample (Chief Scientist & Co-founder) - Based in Paris, France
- Timothée Lacroix (CTO & Co-founder) - Based in Paris, France

Locations:
- Headquarters: Paris, France
- US Office: San Francisco, California
"""

def run_contact_agent(query: str):
    if not settings.MISTRAL_API_KEY:
        return {"answer": "Mistral API key is missing. Please configure it in the .env file.", "sources": [], "agent_used": "contact_agent"}

    llm = ChatMistralAI(model="mistral-large-latest", mistral_api_key=settings.MISTRAL_API_KEY)
    
    prompt = PromptTemplate.from_template(
        "You are MistralBot, an expert on Mistral AI's organization.\n"
        "Use the following contact information to answer the user's question about how to contact Mistral, their offices, or their leadership.\n"
        "If you don't know the answer, use your general knowledge but prioritize the context.\n\n"
        "Context:\n{context}\n\n"
        "Question: {query}\n\nAnswer:"
    )
    
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": CONTACT_INFO, "query": query})
    
    return {
        "answer": answer,
        "sources": [
            {"type": "contact", "title": "Mistral Official LinkedIn", "url": "https://www.linkedin.com/company/mistral-ai"},
            {"type": "contact", "title": "Mistral Discord", "url": "https://discord.gg/mistralai"}
        ],
        "agent_used": "contact_agent"
    }

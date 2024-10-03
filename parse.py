from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Prompt template for parsing text based on user's request
prompt_template = (
    "Analyze the given text data: {content_chunk}. "
    "Please extract information based on the following description: {instructions}. "
    "Follow these rules: \n"
    "1. Extract only what matches the given description. \n"
    "2. Do not include any extra text. \n"
    "3. If nothing matches, return an empty string. \n"
    "4. Only return the requested data."
)

# Initialize the LLaMA model
ai_model = OllamaLLM(model="llama3")

def process_with_ai(content_chunks, description):
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | ai_model

    results = []

    # Process each content chunk
    for idx, chunk in enumerate(content_chunks, start=1):
        response = chain.invoke({"content_chunk": chunk, "instructions": description})
        print(f"Processing chunk {idx} of {len(content_chunks)}")
        results.append(response)

    return "\n".join(results)

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

result = llm.invoke("What is the capital of France?")
print(result)
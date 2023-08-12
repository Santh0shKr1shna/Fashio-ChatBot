import os

from langchain import LLMChain
from langchain import PromptTemplate
from langchain import OpenAI
from langchain.schema import (
  AIMessage,
  HumanMessage,
  SystemMessage
)
from langchain.chat_models import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "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"
chat = ChatOpenAI(temperature=0.9)  # model_name="text-davinci-003"


def feed (prompt):
  sys_msg = """Let's suppose you are a fashion assistant. Generate some fashion recommendations after
            reading through some of my characteristics. I am a 20 year old guy who loves to dress
            subtle. My previous purchases are a pair of Nike Air Jordans, H&M plain t-shirts,
            Baggy jeans. I love lighter colours like beige, cream, and sky blue. Now, answer relevantly
            and straight to the point in less than 50 words """
            
  print("System Message: ", sys_msg)
  print("Human Message: ", prompt)
  
  messages = [
    SystemMessage(content="Let's suppose you are a fashion assistant. Generate some fashion recommendations after "
                          "reading through some of my characteristics. I am a 20 year old guy who loves to dress "
                          "subtle. My previous purchases are a pair of Nike Air Jordans, H&M plain t-shirts, "
                          "Baggy jeans. I love lighter colours like beige, cream, and sky blue. Now, answer relevantly "
                          "and straight to the point in less than 50 words"),
    HumanMessage(content=prompt)
  ]
  
  print("From chatgpt: ", chat(messages).content)

if __name__ == "__main__":
  prompt = input("Enter prompt: ")
  feed(prompt)
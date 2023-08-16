import os
from dotenv import load_dotenv

from Api import WebScrapper

from langchain import LLMChain, PromptTemplate
from langchain.prompts import (
  ChatPromptTemplate,
  MessagesPlaceholder,
  SystemMessagePromptTemplate,
  HumanMessagePromptTemplate
)
from langchain.memory import ConversationBufferMemory
from langchain.schema import (
  AIMessage,
  HumanMessage,
  SystemMessage
)
from langchain import HuggingFaceHub
from langchain.chat_models import ChatOpenAI

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACE_API_TOKEN")

# llms init
repo_id = "google/flan-t5-xxl"

hug_llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.75, "max_length": 64}
)

# model_name="text-davinci-003"
chat = ChatOpenAI(temperature=0.9)


def extract_products (chat_reply):
  template = "From the given statement extract the clothing items and return them as " \
             "comma separated individual articles without losing any details"
  
  prompt = PromptTemplate(template=template, input_variables=["question"])
  
  llm_chain = LLMChain(prompt=prompt, llm=hug_llm)
  
  res = llm_chain.run(chat_reply) # return string
  
  print()

def conversation(query):
  prompt = ChatPromptTemplate(
    messages=[
      SystemMessagePromptTemplate.from_template(
        "Let's suppose you are a fashion assistant. Generate some fashion recommendations after "
        "reading through some of my characteristics. I am a 20 year old guy who loves to dress "
        "subtle. My previous purchases are a pair of Nike Air Jordans, H&M plain t-shirts, "
        "Baggy jeans. I love lighter colours like beige, cream, and sky blue. Now, answer relevantly "
        "and straight to the point in less than 50 words"
      ),
      MessagesPlaceholder(variable_name="chat_history"),
      HumanMessagePromptTemplate.from_template("{question}")
    ]
  )
  
  memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
  convo = LLMChain(
    llm=chat,
    prompt=prompt,
    verbose=True,
    memory=memory
  )
  
  res = convo({"question": query})
  print(type(res))
  print(res.get('text'))

def feed(prompt):
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
  # prompt = input("Enter prompt: ")
  # feed(prompt)
  conversation(input("Enter prompt: "))

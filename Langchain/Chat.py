import os
from dotenv import load_dotenv

from Scrapper import WebScrapper

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
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

load_dotenv()

class Chat(object):
  chat = None
  openAI_llm = None
  
  def __init__(self):
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACE_API_TOKEN")

    # llms init
    
    self.openAI_llm = OpenAI(temperature=0.9)
    
    # model_name="text-davinci-003"
    self.chat = ChatOpenAI(temperature=0.9)

  
  def fetch_results (self, product_list: list):
    scrapper = WebScrapper()
    
    for item in product_list:
      l = scrapper.scrape(item, 3)
      print(item, ": ", l)

  def extract_products (self, chat_reply: str):
    template = "From the given statement carefully extract the clothing items with their specific details such as colour, design patterns or occasion and return them as " \
               "comma separated text" \
               "Statement: {question}"
    
    prompt = PromptTemplate(template=template, input_variables=["question"])
    
    llm_chain = LLMChain(prompt=prompt, llm=self.openAI_llm)
    
    res = llm_chain.run(chat_reply) # return string
    
    print("Result from llm: ", res)
    
    l = res.split(",")
    l = [i.strip().strip('.') for i in l]
    
    return l

  def conversation(self, query: str):
    characteristics = self.db.load_convo()
    
    prompt = ChatPromptTemplate(
      messages=[
        SystemMessagePromptTemplate.from_template(
          "Let's suppose you are my fashion assistant. Properly generate some fashion recommendations after "
          "carefully reading through my characteristics given below. Greet the user passively."
          "Do not answer any questions that are not relevant to fashion in any manner unless it is casual chatting"
          f"Characteristics: {characteristics}"
          "Now, answer relevantly and straight to the point in less than 50 words"
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
      ]
    )
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    convo = LLMChain(
      llm=self.chat,
      prompt=prompt,
      verbose=True,
      memory=memory
    )
    
    res = convo({"question": query})
    
    print(res.get('text'))
    return res.get('text')
  
  def summarize(self, text, token_limit):
    summrzr = OpenAI()
    
    return summrzr(f"Summarize the following paragraph within {token_limit} tokens"
                   f"without losing details and the integrity."
                   f"Content: {text}")


if __name__ == "__main__":
  pass
  # ai_reply = conversation(input("Enter prompt: "))
  # print(ai_reply)
  # prods = extract_products(ai_reply)
  # print(prods)
  # fetch_results(prods)
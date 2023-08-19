import os
from dotenv import load_dotenv

from langchain import HuggingFaceHub
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain

load_dotenv()

os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACE_API_TOKEN")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# template = "List out the the clothing articles along with their attributes in the given statement: {question}"

template = "From the given statement carefully extract the clothing items with their specific details such as colour, design patterns or occasion and return them as " \
           "comma separated text" \
           "Statement: {question}"

prompt = PromptTemplate(template=template, input_variables=["question"])

repo_id = "google/flan-t5-xxl"

# llm = HuggingFaceHub(
#     repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
# )

llm = OpenAI(temperature=0.9)

llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "A pair of tinted sunglasses, and a beige coloured trouser. Finish this outfit with an oversized blue coloured beachy shirt."

res = llm_chain.run(question)
print(question)
print(res)
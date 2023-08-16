import os
from dotenv import load_dotenv

from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain

load_dotenv()

os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACE_API_TOKEN")

# template = """Let's suppose you are a fashion assistant. Generate some fashion recommendations after
#             reading through some of my characteristics. I am a 20 year old guy who loves to dress
#             subtle. My previous purchases are a pair of Nike Air Jordans, H&M plain t-shirts,
#             Baggy jeans. I love lighter colours like beige, cream, and sky blue. Now, answer relevantly
#             and straight to the point in less than 50 words.
#             Question: {question}"""

template = "From the given statement carefully extract the clothing items with their specific details such as colour, design patterns or occasion and return them as " \
           "comma separated text" \
           "Statement: {question}"

prompt = PromptTemplate(template=template, input_variables=["question"])

repo_id = "google/flan-t5-xxl"

llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
)

llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "A pair of tinted sunglasses, and a beige coloured trouser. Finish this outfit with an oversized blue coloured beachy shirt."

res = llm_chain.run(question)
print(question)
print(res)
# Fashion-ChatBot: Flipkart GRiD 5.0 Software Development Track
Submission made by Santhosh Krishna S, Sairam R and Shershon A J

## Problem Statement
Generative AI has been changing the landscape of almost every domain, especially conversational chatbots. Can this be incorporated into the realm of online shopping? Our problem statement aims to find out just that. We have been asked to develop a *Gen AI-powered fashion outfit generator* for Flipkart that can take the experience of online shopping to the next level.

## Our solution
A conversational chatbot built using GenAI to help with your fashion needs.

## Tech Stack

## Modules
### Chatbot using LLM
We have one main chat model from OpenAI dedicated for the conversation and one general use llm also from OpenAI which is used for many purposes such as the summarizer, context analyzer, etc.

We have built this project completely on python using the LangChain library which provides ample support for building llm powered application with high customizations and accessibilities.

### Trending sites scrapping

This comprehensive Python-based fashion trend analysis system employs a series of libraries to collect data. Instaloader captures recent posts from fashion influencers on Instagram, while Pinscraper retrieves trending posts from Pinterest using fashion keywords. BeautifulSoup4 is utilized to scrape fashion images from prominent magazines' websites. Additionally, Pytrends taps into the Google Trends API to provide the chatbot with the top 5 trending fashion search queries, factoring in user location for a tailored experience.

### Virtual Try-On
The Virtual Try-On module was developed using the implementation of HR-VITON research paper, which aims to synthesis the image of a person wearing a specific piece of clothing item.

This helps the user to try on the fashion outfits that is recommended by the LLM and is taken from the Flipkart site.



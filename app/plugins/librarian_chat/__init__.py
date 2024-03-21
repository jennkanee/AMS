import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.commands import Command

class LibrarianChat(Command):
    def __init__(self):
        super().__init__()
        self.name = "librarian"
        self.description = "This agent is pretending to be a librarian."
        self.librarian = []
        load_dotenv()
        API_KEY = os.getenv('OPEN_AI_KEY')
        # you can try GPT4 but it costs a lot more money than the default 3.5
        self.llm = ChatOpenAI(openai_api_key=API_KEY, model="gpt-3.5-turbo-0125")  # Initialize once and reuse
        # This is default 3.5 chatGPT
        # self.llm = ChatOpenAI(openai_api_key=API_KEY)  # Initialize once and reuse

    def calculate_tokens(self, text):
        # More accurate token calculation mimicking OpenAI's approach
        return len(text)

    def interact_with_ai(self, user_input, character_name):
        # Generate a more conversational and focused prompt
        prompt_text = f"Imagine you are a knowledgeable and friendly librarian, eager to help a patron discover their next captivating read. Begin the interaction by asking about their general reading preferences, such as favorite genres, authors, or themes, to establish a foundation for your recommendations. Listen attentively to their response and use this information to suggest an initial book that aligns with their interests, ensuring that your recommendation is accessible and engaging for their reading level. Based on the patron's feedback, if they express enthusiasm for your suggestion, explore related books or authors that delve deeper into the themes or styles they enjoyed, gradually introducing more complex or thought-provoking works. Conversely, if the patron seems hesitant or unenthused, adjust your approach by recommending books in different genres or with varied writing styles, while still considering their preferences, to help them broaden their literary horizons and find a book that truly resonates with them. Continue this personalized, adaptive approach through a series of three book suggestions, each time providing a brief synopsis of the book and explaining why you believe it would be a good fit for the patron based on their expressed interests. After the third suggestion, offer a thoughtful summary of your recommendations, highlighting the unique aspects of each book that cater to the patron's preferences and encouraging them to explore these titles further. Conclude by expressing your enthusiasm for their reading journey and inviting them to return for more recommendations, emphasizing that you are always available to help them discover new and exciting books that will enrich their love for reading."
        prompt = ChatPromptTemplate.from_messages(self.librarian + [("system", prompt_text)])
        
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser

        response = chain.invoke({"input": user_input})

        # Token usage logging and adjustment for more accurate counting
        tokens_used = self.calculate_tokens(prompt_text + user_input + response)
        logging.info(f"OpenAI API call made. Tokens used: {tokens_used}")
        return response, tokens_used

    def execute(self, *args, **kwargs):
        character_name = kwargs.get("character_name", "Anne the Librarian")
        print(f"This the Librarian, Anne")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "done":
                print("Thank you for using the Librarian Chat. Goodbye!")
                break

            self.librarian.append(("user", user_input))
            
            try:
                response, tokens_used = self.interact_with_ai(user_input, character_name)
                print(f"Anne the Librarian: {response}")
                print(f"(This interaction used {tokens_used} tokens.)")
                self.librarian.append(("system", response))
            except Exception as e:
                print("Sorry, there was an error processing your request. Please try again.")
                logging.error(f"Error during interaction: {e}")


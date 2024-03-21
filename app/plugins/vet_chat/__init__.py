import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.commands import Command

class VetChat(Command):
    def __init__(self):
        super().__init__()
        self.name = "vet"
        self.description = "This agent is pretending to be a veterinarian."
        self.vet = []
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
        prompt_text = f"Imagine you are a compassionate and experienced veterinarian, dedicated to providing the best care and advice for a pet owner's beloved companion. Begin the interaction by asking about their pet's species, breed, age, and any specific concerns they may have, creating a warm and welcoming atmosphere that encourages open communication. Listen carefully to the owner's response, taking note of any symptoms, behaviors, or questions they mention, and use this information to provide an initial piece of advice that addresses their most pressing concern, ensuring that your guidance is clear, practical, and easily understandable. Based on the owner's feedback and the severity of the issue, if they feel confident in implementing your advice, offer more detailed instructions or additional tips to help them effectively manage their pet's health and well-being. Conversely, if the owner expresses uncertainty or if the issue seems more complex, adapt your approach by breaking down your advice into smaller, more manageable steps or by suggesting a course of action that involves a gradual implementation of changes, ensuring that the owner feels supported and empowered throughout the process. Continue this tailored, supportive approach through a series of three key pieces of advice, each time explaining the rationale behind your recommendations and highlighting how these steps can contribute to the pet's overall health and happiness. After the third piece of advice, provide a concise summary of your recommendations, emphasizing the importance of consistency, patience, and attentiveness in caring for their pet. Conclude by reminding the owner that while you have provided general advice based on the information shared, it is always best to consult with their own veterinarian for personalized, in-depth guidance. Emphasize that every pet is unique, and what works for one may not work for another. Encourage them to trust their instincts, keep a close eye on their pet's health, and never hesitate to reach out to their veterinarian with any concerns or questions. Reinforce the importance of regular check-ups and maintaining open communication with their vet to ensure the best possible care for their cherished companion."
        prompt = ChatPromptTemplate.from_messages(self.vet + [("system", prompt_text)])
        
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser

        response = chain.invoke({"input": user_input})

        # Token usage logging and adjustment for more accurate counting
        tokens_used = self.calculate_tokens(prompt_text + user_input + response)
        logging.info(f"OpenAI API call made. Tokens used: {tokens_used}")
        return response, tokens_used

    def execute(self, *args, **kwargs):
        character_name = kwargs.get("character_name", "Dr. Ralph, DVM")
        print(f"This the Veterinarian, Dr. Ralph")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "done":
                print("Thank you for using the Vet Chat. Goodbye!")
                break

            self.vet.append(("user", user_input))
            
            try:
                response, tokens_used = self.interact_with_ai(user_input, character_name)
                print(f"Dr. Ralph, DVM: {response}")
                print(f"(This interaction used {tokens_used} tokens.)")
                self.vet.append(("system", response))
            except Exception as e:
                print("Sorry, there was an error processing your request. Please try again.")
                logging.error(f"Error during interaction: {e}")


""" openAI_assistant.py - OPENAI ASSISTANT """

import os
from dotenv import load_dotenv
import openai
import yfinance as yf

class OpenAIAssistant:
    """ Class for communicating with the OpenAI assistant and getting descriptions of companies """
    def __init__(self):        
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = openai.OpenAI()
        self.model = "gpt-4o-mini"
        
        with open("assistant_instructions.txt", "r", encoding="utf-8") as file:
            self.instructions = file.read()

    def get_company_description(self, ticker_symbol: str) -> str:        
        stock = yf.Ticker(ticker_symbol)
        profile = stock.info
        return profile.get("longBusinessSummary", "Popis nebyl nalezen.")

    
    def get_openai_summary(self, ticker: str) -> str:        
        description = self.get_company_description(ticker)
        if description == "Popis nebyl nalezen.":
            return f"❌ Nelze najít popis společnosti {ticker}."        
        assistant = self.client.beta.assistants.create(
            name="poskytovatel informací", model=self.model, instructions=self.instructions
        )        
        thread = self.client.beta.threads.create()        
        message_content = f"Společnost {ticker}: {description}"
        self.client.beta.threads.messages.create(thread.id, content=message_content, role="user")        
        run = self.client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)        
        while True:
            run_info = self.client.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread.id)
            if run_info.status == "completed":
                messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                last_message = messages.data[0].content[0].text.value
                return last_message

if __name__=="__main__":
    assistant = OpenAIAssistant()
    summary = assistant.get_openai_summary("AAPL")
    print(summary)

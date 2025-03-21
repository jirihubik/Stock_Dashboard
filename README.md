# Stock dashboard
Stock Dashboard is a Python-based financial analytics application built with Streamlit. It provides users with economic and stock market insights in Czech, powered by an AI assistant via an AI API. The application fetches financial data using Yahoo Finance and Finnhub, while the Streamlit frontend ensures an interactive user experience.  

### Features:  
- **AI-powered insights**: Users can enter a company ticker, and the AI assistant will provide key financial and stock-related information in Czech.  
- **STOCK price chart**: A line chart (based on closing prices) visualizing the selected company's stock movements over a user-defined period. Includes a SPY benchmark line for comparison.
- **Data source**: All stock market data is retrieved via the **Yahoo Finance API** and **FINNHUB API**.  

🚀 This tool provides users with essential company insights in Czech and an interactive stock chart with customizable parameters! 

## Installation
Ensure you have Python 3.x installed on your system. You can check your version by running:
```bash
python --version
```
If Python is not installed, download it from python.org.

To install the necessary dependencies, use the package manager pip.
```bash
pip install -r requirements.txt
```
You will also need to set up a .env file with your API keys.
```bash
OPENAI_API_KEY = "your-openai-api-key"
FINNHUB_API_KEY = "your-finnhub-api-key"
```

## Usage
### Run the Application:
Start the Streamlit app using the following command:
```bash
streamlit run main.py
```
### Interact with the App:
Enter the ticker of the company you are interested in.
Select the time period of the graph.
Select the Moving Average indicator parameter.
The App will generate profile&description of the company and the graph according to your selection.

## Project Structure
### main.py
Contains the main logic for running the Streamlit frontend and handling user interactions.
### openAI_assistant.py  
Manages the interaction with OpenAI's API, including sending prompts and receiving responses.  
It also processes stock market data retrieved using **yFinance** to provide AI-powered insights.  
### finnhubAPI_client.py
A client for fetching company data via FINNHUB API.
### assistant_instructions.txt
Contains the prompt along with examples to guide the OpenAI assistant's responses.
### requirements.txt
List of all Python dependencies needed for the project.
### database.py
Saves or updates ticker information in the database.

## Future
### Unit testing
Adding comprehensive unit tests to ensure the reliability and accuracy of the application's components.
### Improved visualization
replacement of the linear display with modern graphical look


## License

[MIT](https://choosealicense.com/licenses/mit/)
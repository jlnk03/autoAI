from langchain.llms import OpenAIChat, HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper, PythonREPL, DuckDuckGoSearchAPIWrapper, TextRequestsWrapper
from langchain.schema import HumanMessage, SystemMessage
from langchain import OpenAI
from langchain.agents import initialize_agent, Tool


def llm_bot_response(prompt):

    # OpenAI
    # llm = ChatOpenAI(temperature=0.1, model_name='gpt-3.5-turbo')
    llm = OpenAI(temperature=0.1)

    # Python tool
    python_repl = PythonREPL()
    python_tool = Tool(
        name='Python REPL',
        func=python_repl.run,
        description='A Python shell. Use this to execute python commands. Input should be a valid python command. If you expect output it should be printed out.',
    )

    # Wikipedia
    wikipedia = WikipediaAPIWrapper()
    wikipedia_tool = Tool(
        name='Wikipedia',
        func=wikipedia.run,
        description='A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, historical events, or other subjects. Input should be a search query.',
    )

    # DuckDuckGo
    duckduckgo = DuckDuckGoSearchAPIWrapper()
    duckduckgo_tool = Tool(
        name='DuckDuckGo',
        func=duckduckgo.run,
        description='A search engine. Useful for when you need to answer questions about current events. Input should be a search query.',
    )

    # TextRequests/Search a website
    text_requests = TextRequestsWrapper()
    text_requests_tool = Tool(
        name='TextRequests',
        func=text_requests.get,
        description='A portal to the internet. Use this when you need to get specific content from a site. Input should be a specific url, and the output will be all the text on that page.',
    )

    tools = [python_tool, wikipedia_tool, duckduckgo_tool, text_requests_tool]

    # Initialize agent
    agent = initialize_agent(
        agent='zero-shot-react-description',
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=10,
    )

    result = agent.run(prompt)

    return result

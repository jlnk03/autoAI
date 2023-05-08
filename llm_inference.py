from langchain.llms import OpenAIChat, HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper, PythonREPL
from langchain.schema import HumanMessage, SystemMessage

python_repl = PythonREPL()


def llm_response(prompt):
    # Prompt templates
    title_template = PromptTemplate(
        input_variables=['topic'],
        template='Write me a story title about {topic}.',
    )

    script_template = PromptTemplate(
        input_variables=['title', 'wikipedia_research'],
        template='Write me a super short story about {title}, based on the following research: {wikipedia_research}.',
    )

    # Memory
    title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
    script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')

    # Chains

    # MosaicML
    # llm = HuggingFaceHub(repo_id="mosaicml/mpt-7b", model_kwargs={'temperature': 0.1, 'max_length': 1000})

    # OpenAI
    llm = ChatOpenAI(temperature=0.1, model='gpt-3.5-turbo')
    title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
    script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)
    # sequential_chain = SequentialChain(chains=[title_chain, script_chain], verbose=True, input_variables=['topic'], output_variables=['title', 'script'])

    # Wikipedia
    wiki = WikipediaAPIWrapper()

    # title = title_chain.run(topic=prompt)
    # wikipedia_research = wiki.run(prompt)
    # script = script_chain.run(title=title, wikipedia_research=wikipedia_research)
    message = [HumanMessage(content=prompt)]
    result = llm(message).content
    print(result)
    print(type(result))

    return result

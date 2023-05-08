import dash
from dash_extensions.enrich import html, dcc, Input, Output, State, ClientsideFunction, no_update
import time
from llm_inference import llm_response
from llm_bot import llm_bot_response


def chat_bubble(text, is_user=False, loading=False):
    current_time = time.time()
    bubble_id = {'type': 'user-message', 'index': current_time} if is_user else {'type': 'bot-message', 'index': current_time}
    className = 'flex flex-col w-fit relative bg-blue-500 text-white rounded-2xl px-4 py-2 shadow-lg max-w-[90%]' if is_user else 'flex flex-col w-fit relative bg-gray-200 rounded-2xl px-4 py-2 shadow-lg max-w-[90%]'
    position = 'justify-end' if is_user else 'justify-start'
    if loading:
        className += ' animate-pulse'

    bubble = html.Div(
        className=f'flex flex-row flex-none w-full relative {position}',
        children=[
            dcc.Markdown(
                id=bubble_id,
                className=className,
                highlight_config={'theme': 'dark'},
                children=[
                    text
                ]
            ),
        ]
    )

    return bubble


def init_chat():
    layout = html.Div(

        id='main',
        className='flex flex-col w-full items-center pt-24 pb-28 relative overflow-hidden',

        children=[

            dcc.Dropdown(
                id='agent-true',
                className='w-20 h-12 fixed top-4 left-1/2 transform -translate-x-1/2 z-20',
                options=[
                    {'label': 'Chat', 'value': 'chat'},
                    {'label': 'Agent', 'value': 'agent'},
                ],
                clearable=False,
                value='chat',
            ),

            html.Div(
                id='chat-view',
                className='flex flex-col max-w-3xl w-full h-full font-normal text-base gap-4 relative overflow-y-auto -mx-4 px-4',
                children=[
                    html.Div(
                        id='initial-message',
                        className='flex w-fit relative bg-gray-200 rounded-2xl px-4 py-2 shadow-lg',
                        children=[
                            'Press start to begin creating your report.'
                        ]
                    )
                ]
            ),

            html.Div(
                id='input-view',
                className='fixed flex flex-row grow sm:gap-3 gap-1 bottom-10 max-w-3xl w-full font-normal text-base px-2',
                children=[

                    dcc.Upload(
                        id='upload-img',
                        className='w-20 h-12 bg-blue-500 text-white rounded-2xl flex-none w-12 shadow-lg items-center justify-center flex flex-row',
                        children=[
                            html.Img(src='assets/img.png', className='w-6 h-6 invert')
                        ],
                    ),

                    html.Button(

                        id='mic-button',
                        className='w-20 h-12 bg-blue-500 text-white rounded-2xl flex-none w-12 shadow-lg items-center justify-center flex flex-row animate-none',
                        children=[
                            html.Img(src='assets/mic.png', className='w-6 h-6 invert')
                        ],
                        n_clicks=0
                    ),

                    dcc.Input(
                        id='text-input',
                        className='w-full bg-white rounded-2xl px-4 py-2 shadow-lg min-h-12 grow',
                        placeholder='Write your text here...',
                        type='text',
                        value='',
                        disabled=False,
                        debounce=True,
                    ),
                    html.Button(

                        id='send-button',
                        className='w-20 h-12 bg-blue-500 text-white rounded-2xl w-12 flex-none shadow-lg items-center justify-center flex flex-row',
                        children=[
                            html.Img(src='assets/airplane.png', className='w-6 h-6 invert')
                        ],
                        n_clicks=0
                    ),
                ]
            ),
        ]
    )

    return layout


def init_callbacks(app):
    @app.callback(
        Output('chat-view', 'children', allow_duplicate=True),
        Input('send-button', 'n_clicks'),
        Input('text-input', 'n_submit'),
        State('text-input', 'value'),
        State('chat-view', 'children'),
        prevent_initial_call=True,
    )
    def update_chat_view(n_clicks, n_submit, text, children):
        if text is not None:
            # user view
            bubble_user = chat_bubble(text, is_user=True, loading=False)
            children.append(bubble_user)

            # loading view
            loading_text = 'Generating response...'
            bubble_bot = chat_bubble(loading_text, is_user=False, loading=True)
            children.append(bubble_bot)

        return children

    @app.callback(
        Output('text-input', 'value'),
        Input('send-button', 'n_clicks'),
        Input('text-input', 'n_submit'),
        prevent_initial_call=True
    )
    def clear_input(n_clicks, n_submit):
        return ''

    @app.callback(
        Output('chat-view', 'children'),
        Input('chat-view', 'children'),
        State('agent-true', 'value'),
        prevent_initial_call=True
    )
    def chat_inference(children, agent_true):
        prompt = children[-2]['props']['children'][0]['props']['children'][0]

        if agent_true == 'agent':
            response = llm_bot_response(prompt)
        else:
            response = llm_response(prompt)

        children.pop()
        # for i, text in enumerate(response):
        bubble_bot = chat_bubble(response, is_user=False, loading=False)
        children.append(bubble_bot)

        return children

    app.clientside_callback(
        ClientsideFunction(namespace='clientside', function_name='codeStyle'),
        Input('chat-view', 'children'),
    )

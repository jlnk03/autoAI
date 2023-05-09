from chat import init_chat, init_callbacks
# from dash import ctx, ALL, html, dcc, MATCH, ClientsideFunction, no_update, Dash
from dash_extensions.enrich import DashProxy, NoOutputTransform, Output, Input, State, html


# Initialize the app
app_server = DashProxy(__name__,
                       external_scripts=[{"src": "https://cdn.tailwindcss.com"}],
                       transforms=[NoOutputTransform()]
                       )
app_server.css.config.serve_locally = False
app_server.css.append_css({'external_url': '/assets/output.css'})
app_server.server.static_folder = 'assets'

app_server.title = 'autoAI'

app_server.layout = html.Div(
    [
        init_chat()
    ],
    className='flex flex-col bg overflow-hidden fixed top-12 bottom-24 left-0 right-0'
)

init_callbacks(app_server)

if __name__ == '__main__':
    server = app_server.server
    server.run(debug=False)
from chat import init_chat, init_callbacks
# from dash import ctx, ALL, html, dcc, MATCH, ClientsideFunction, no_update, Dash
from dash_extensions.enrich import DashProxy, NoOutputTransform, Output, Input, State, html


# Initialize the app
app = DashProxy(__name__,
                external_scripts=[{"src": "https://cdn.tailwindcss.com"}],
                transforms=[NoOutputTransform()]
                )
app.css.config.serve_locally = False
app.css.append_css({'external_url': '/assets/output.css'})
app.server.static_folder = 'assets'

app.title = 'autoAI'

app.layout = html.Div(
    [
        init_chat()
    ],
    className='flex flex-col w-full h-full bg'
)

init_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)

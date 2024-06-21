from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import base64
import requests

END_POINT = "https://neural-style-transfer-zekrs5pysa-uc.a.run.app/"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Neural Style Transfer", className="text-center"),
                width=12
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Form(
                    [
                        dcc.Upload(
                            id='content-upload',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select a Content Image')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px 0'
                            },
                            multiple=False
                        ),
                        dcc.Upload(
                            id='style-upload',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select a Style Image')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px 0'
                            },
                            multiple=False
                        ),
                        dbc.Button('Stylize Image', id='stylize-button', color='primary', className='mt-2')
                    ],
                    id='image-form'
                ),
                width=12
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.H2("Uploaded Images"),
                    html.Img(id='uploaded-content-image', style={'max-width': '45%', 'borderRadius': '8px', 'margin': '10px'}),
                    html.Img(id='uploaded-style-image', style={'max-width': '45%', 'borderRadius': '8px', 'margin': '10px'})
                ],
                width=12
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.H2("Stylized Image"),
                    dcc.Loading(html.Img(id='stylized-image', style={'max-width': '100%', 'borderRadius': '8px', 'margin-top': '20px'}))
                ],
                width=12
            )
        )
    ],
    className='text-center mt-5'
)

@app.callback(
    Output('uploaded-content-image', 'src'),
    Output('uploaded-style-image', 'src'),
    Input('content-upload', 'contents'),
    Input('style-upload', 'contents'),
    State('content-upload', 'filename'),
    State('style-upload', 'filename'),
)
def update_uploaded_images(content_img, style_img, content_filename, style_filename):
    if content_img is not None:
        content_img_src = content_img
    else:
        content_img_src = None

    if style_img is not None:
        style_img_src = style_img
    else:
        style_img_src = None

    return content_img_src, style_img_src

@app.callback(
    Output('stylized-image', 'src'),
    Input('stylize-button', 'n_clicks'),
    State('content-upload', 'contents'),
    State('style-upload', 'contents')
)
def stylize_image(n_clicks, content_img, style_img):
    if n_clicks is None or content_img is None or style_img is None:
        return None

    content_image_data = content_img.split(',')[1]
    style_image_data = style_img.split(',')[1]

    content_image_decoded = base64.b64decode(content_image_data)
    style_image_decoded = base64.b64decode(style_image_data)

    files = {
        'content_image': content_image_decoded,
        'style_image': style_image_decoded
    }

    response = requests.post(f'{END_POINT}stylize', files=files)

    if response.status_code == 200:
        stylized_image_data = base64.b64encode(response.content).decode('utf-8')
        return 'data:image/png;base64,{}'.format(stylized_image_data)
    else:
        return None


if __name__ == '__main__':
    app.run_server(debug=True)
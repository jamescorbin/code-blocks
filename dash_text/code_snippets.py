
table = (
    go.Table(
        header=dict(values=df.columns),
        cells=dict(values=df.iloc[:200].values.T.tolist()),
    )
)
go_table = go.Figure(data=table)
div_go_table = dcc.Graph(id='go_table', figure=go_table)


    '''
    div_columns = div_text_display.main(app)

    div_wc_l = html.Div(id='div_wc_l')

    @app.callback(
        Output('div_wc_l', component_property='children'),
        Input('text-dd-l', 'value'),
    )
    def _update_left_textbox(fbn):
        return (
            html.Img(src=_plot_wordcloud(fbn))
        )

    div_wc_r = html.Div(id='div_wc_r')

    @app.callback(
        Output('div_wc_r', component_property='children'),
        Input('text-dd-r', 'value'),
    )
    def _update_left_textbox(fbn):
        return (
            html.Img(src=_plot_wordcloud(fbn))
        )

    div_bigrams_l = dcc.Graph(id='div_bigrams_l')

    @app.callback(
        Output('div_bigrams_l', 'figure'),
        Input('text-dd-l', 'value'),
    )
    def _plot_bigrams_l(txt):
        return _plot_bigrams(txt)
    '''


    '''
    app.layout = (
        html.Div(
            id='body',
            children=[
                div_index,
                #div_columns,
                #div_wc_l,
                #div_wc_r,
                #div_bigrams_l,
            ],
        )
    )
    '''

def _plot_wordcloud(_id):
    fn = os.path.join(textnlp.default_ancillary_dir, f"{_id[:-len(TXT)]}{JSON}")
    if os.path.exists(fn):
        with open(fn, 'r') as f:
            counts = json.load(f)
        fig = visualization.plot_wordcloud(counts, os.path.basename(fn))
        tdir = tempfile.TemporaryDirectory()
        fig_fn = os.path.join(tdir.name, 'a.png')
        fig.savefig(fig_fn)

        with open(fig_fn, 'rb') as f:
            bs = f.read()
        bs64 = base64.b64encode(bs)
        src = 'data:image/png;base64,{}'.format(bs64.decode('ascii'))
    else:
        src = ''
    return src


def _plot_bigrams(_id):
    fn = os.path.join(textnlp.default_preprocessed_dir, f"{_id}")
    if os.path.exists(fn) and os.path.isfile(fn):
        with open(fn, 'r') as f:
            text = f.read()
        fig = visualization.plot_bigrams(text)
    else:
        fig = go.Figure()
    return fig



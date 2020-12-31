
table = (
    go.Table(
        header=dict(values=df.columns),
        cells=dict(values=df.iloc[:200].values.T.tolist()),
    )
)
go_table = go.Figure(data=table)
div_go_table = dcc.Graph(id='go_table', figure=go_table)

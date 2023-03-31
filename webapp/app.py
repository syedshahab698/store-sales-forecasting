import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Load your sales data
sales_data = pd.read_parquet('sales.parquet.gzip')

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

# Define the app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Sales Forecasting For Grocery Store', className='display-3 text-center')
        ], width=12)
    ], className='mb-5 mt-5'),
    dbc.Row([
        dbc.Col([
            html.Label('Select Date Range'),
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=sales_data['date'].min(),
                max_date_allowed=sales_data['date'].max(),
                start_date=sales_data['date'].min(),
                end_date=sales_data['date'].max(),
                className='form-control'
            ),
        ], width=4),
        dbc.Col([
            html.Label('Select Product Family'),
            dcc.Dropdown(
                id='product-family',
                options=[{'label': family, 'value': family} for family in sales_data['family'].unique()],
                value=sales_data['family'].iloc[0],
                className='form-control'
            ),
        ], width=4),
        dbc.Col([
            dbc.Button('Submit', id='submit-button', color='primary', className='mr-1',style = {'margin-top':'25px'})
        ], width=4),
    ], className='mb-5'),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sales-plot')
        ], width=12)
    ], className='mb-5')
])

# Define the app callback
@app.callback(
    dash.dependencies.Output('sales-plot', 'figure'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('date-range', 'start_date'),
     dash.dependencies.State('date-range', 'end_date'),
     dash.dependencies.State('product-family', 'value')]
)
def update_sales_plot(n_clicks, start_date, end_date, product_family):
    filtered_sales_data = sales_data[(sales_data['date'] >= start_date) & (sales_data['date'] <= end_date) & (sales_data['family'] == product_family)]
    sales_fig = go.Figure()
    sales_fig.add_trace(go.Scatter(x=filtered_sales_data['date'], y=filtered_sales_data['sales'], name='Sales', line=dict(color='#002B36', width=4)))
    sales_fig.update_layout(
        title=f'Sales of {product_family} family',
        xaxis_title='Date',
        yaxis_title='Sales',
        plot_bgcolor='#A9BDBD',
        paper_bgcolor='#A9BDBD',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    return sales_fig
if __name__ == '__main__':
    app.run_server(debug=True)

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
        ], width=8),
        dbc.Col([
            html.P('Group 3 Members:', className='lead'),
            html.Ul([
                html.Li('Somya Sachan'),
                html.Li('Geetha Murugan'),
                html.Li('Harsh Singh'),
                html.Li('Narasimha Reddy'),
                html.Li('Rahul Esiripally'),
                html.Li('Shahabuddin Syed'),
            ])
        ], width=4),
        
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
        ], width=3),
        dbc.Col([
            html.Label('Select Store Number'),
            dcc.Dropdown(
                id='store-number',
                options=[{'label': store_nbr, 'value': store_nbr} for store_nbr in sales_data['store_nbr'].unique()],
                value=sales_data['store_nbr'].iloc[0],
                className='form-control'
            ),
        ], width=3),
        dbc.Col([
            html.Label('Select Product Family'),
            dcc.Dropdown(
                id='product-family',
                options=[{'label': family, 'value': family} for family in sales_data['family'].unique()],
                value=sales_data['family'].iloc[0],
                className='form-control'
            ),
        ], width=3),
        dbc.Col([
            html.Label('Future Forecast (Days)'),
            dcc.Input(
                id='forecast-days',
                type='number',
                min=1,
                max=60,
                value=30,
                className='form-control'
            ),
        ], width=3),
        dbc.Col([
            dbc.Button('Submit', id='submit-button', color='primary', className='mr-1 col-md-12 text-center',style = {'margin-top':'25px'})
        ], width=12),
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
     dash.dependencies.State('product-family', 'value'),
     dash.dependencies.State('forecast-days', 'value'),
     dash.dependencies.State('store-number', 'value')]
)
def update_sales_plot(n_clicks, start_date, end_date, product_family, forecast_days, store_nbr):
    filtered_sales_data = sales_data[(sales_data['date'] >= start_date) & (sales_data['date'] <= end_date) & (sales_data['family'] == product_family) & (sales_data['store_nbr'] == store_nbr)]
    filtered_sales_data = filtered_sales_data.sort_values('date')

    d = filtered_sales_data.date.max()
    d_r = pd.date_range(start = d, periods=forecast_days, freq = 'd')
# Calculate forecasted sales data using a simple moving average
    sales_data_forecast = filtered_sales_data.copy()
    sales_data_forecast['sales'] = sales_data_forecast['sales'].rolling(window=7).mean()
    sales_data_forecast = sales_data_forecast.tail(forecast_days)
    sales_data_forecast = sales_data_forecast.sort_values('date')
    print(d_r)
    sales_data_forecast.date = d_r

    sales_fig = go.Figure()
    sales_fig.add_trace(go.Scatter(x=filtered_sales_data['date'], y=filtered_sales_data['sales'], name='Sales', line=dict(color='#002B36', width=4)))
    sales_fig.add_trace(go.Scatter(x=sales_data_forecast['date'], y=sales_data_forecast['sales'], name='Sales Forecasts', line=dict(color='#557A95', width=4)))
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

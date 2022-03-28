import pandas as pd
import plotly.express as px 
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Div.
import pandas as pd
import numpy as np
import calendar

# Plotly
import plotly.express as px
import plotly.graph_objects as go

# Loading datas
xls = pd.ExcelFile('my_shop_data.xlsx')
df_customers = pd.read_excel(xls, 'customers')
df_orders = pd.read_excel(xls, 'order')
df_employees = pd.read_excel(xls, 'employee')
df_products = pd.read_excel(xls, 'products')

df_prod_order = pd.merge(df_orders, df_products[['product_id', 'productname', 'type']], on='product_id')
df_prod_order_cust = pd.merge(df_prod_order, df_customers[['customer_id', 'first_name', 'last_name', 'country']], on='customer_id')

df_prod_order_cust['sale'] = df_prod_order_cust['unitprice'] * df_prod_order_cust['quantity']

df_prod_order_cust['id_and_name'] = df_prod_order_cust['customer_id'].astype(str) + " - " + df_prod_order_cust['first_name'] + " " + df_prod_order_cust['last_name']

prod_order = df_prod_order_cust.groupby(by=['product_id', 'productname'])[['type', 'sale']].apply(sum)[['sale']].reset_index().sort_values(by=['sale'], ascending=False)

prod_order_fig = px.bar(prod_order, x='sale', y='productname', template="plotly_dark", title="Top Selling Products")

#prod_order_fig.show()
df_employees["full_name"] = df_employees["firstname"] + df_employees["lastname"]

df_ordersEM = pd.merge(df_prod_order_cust, df_employees, on= "employee_id")
df_ordersEM = df_ordersEM.groupby(by=['full_name'])[['sale']].apply(sum)[['sale']].reset_index().sort_values(by=['sale'], ascending=False)

prod_orderEM_fig = px.bar(df_ordersEM, x='sale', y='full_name', template="plotly_dark", title="Top Selling Employees")

#prod_orderEM_fig.show()
#print(df_ordersEM)

dash_app = dash.Dash(__name__)
app = dash_app.server

# ***************************************
# Layout
# ***************************************
dash_app.layout = html.Div(
    children=[
        html.Div(className='row',
                children=[
                   
                    html.Div(className='eight columns div-for-charts bg-grey',
                            children=[
                                dcc.Graph(id="sales_employee", figure=prod_orderEM_fig)
                            ]
                    ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                            children=[
                                dcc.Graph(id="sales_product", figure=prod_order_fig)
                            ]
                    ),
                ]
            )
        ]
)

# ***************************************
# Run the app
# ***************************************
if __name__ == '__main__':
    dash_app.run_server(debug=True)

from flask_sqlalchemy import _EngineConnector
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from flask import render_template, request, url_for, flash
from flask_sqlalchemy.utils import sqlalchemy_version
from models import Stock_list,Transactions
from app import app
from forms import NewItem, StockUpdate, SelectView
from models import db

sort_on="days"
days_for_burn_rate=14
stocks_df=pd.read_sql_table('stock_list',con=db.engine, index_col="id")
stocks_df["total_stock"]=stocks_df["kitchen_stock"] + stocks_df["garage_stock"]
stocks_df.drop(["kitchen_stock","garage_stock","barcode"],axis=1, inplace=True)
transactions_df=pd.read_sql_table("transactions", con=db.engine)
transactions_df_f1=transactions_df.loc[(transactions_df.action =="Use garage stock") |  (transactions_df.action == "Use kitchen stock") &  (transactions_df.date > datetime.utcnow()-timedelta(days=days_for_burn_rate))].reset_index()
transactions_df_f1.drop(['index','id','action','date'], axis=1, inplace=True)
transactions_df_f2=transactions_df_f1.groupby(['item']).sum().reset_index()
combined_df=pd.merge(stocks_df, transactions_df_f2, on="item", how='outer')
combined_df['percent_min']=combined_df['total_stock']/combined_df['minimum_stock']*100
combined_df['days_to_min']=combined_df['total_stock']*days_for_burn_rate/combined_df['number_actioned']
combined_df.drop(['minimum_stock','number_actioned'],axis=1,inplace=True)
combined_df.fillna(0)
if sort_on == "percent":
    combined_df.sort_values(by='percent_min', inplace=True)
elif sort_on =="days":
    combined_df.sort_values(by='days_to_min', inplace=True)
else: 
    combined_df.sort_values(by='item', inplace=True)
r_combined_df=combined_df.round({'percent_min':0, 'days_to_min':0}).reset_index()
rf_combined_df=r_combined_df.fillna(0)
output_dict=rf_combined_df.to_dict('records')
print(rf_combined_df)
print (output_dict)


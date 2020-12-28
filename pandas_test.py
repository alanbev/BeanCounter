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


stocks_df=pd.read_sql_table('stock_list',con=db.engine, index_col="id")


print(stocks_df)
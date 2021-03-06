from datetime import datetime, timedelta
from flask import render_template, request, url_for, flash
from flask_sqlalchemy.utils import sqlalchemy_version
from pandas.io.pytables import PossibleDataLossError
from models import Stock_list,Transactions
from app import app
from forms import ChangeItem, DeleteItem, Dummyform, NewItem, SelectEdit, SortShopList, StockUpdate, SelectView, SortShopList
from models import db
import numpy as np
import pandas as pd
from sorted_list import generate_sorted_list ,generate_shopping_list_for_printing


@app.route('/', methods=('GET','POST'))
@app.route('/update_stock', methods=('GET','POST'))
def update_stock():
    form = StockUpdate()
    if Stock_list.query.all() is None:
        item_choices = []
    else:   
        item_choices = Stock_list.query.order_by(Stock_list.item).all()


    each_item=[]
    for choice in item_choices:
        each_item.append(choice.item)
    form.item_name.choices=each_item
    if request.method =='POST':
        if form.validate_on_submit():   
            item_actioned = request.form['item_name']
            item_quantity = int(request.form['item_quantity'])
            print(type(item_quantity))
            action = request.form['actions']
            item_to_add = Transactions(action=action, number_actioned=item_quantity, item=item_actioned)
            db.session.add(item_to_add)
            db.session.commit()
            entry_to_change = Stock_list.query.filter_by(item=item_actioned).first()

            if action == 'New stock to kitchen':
                entry_to_change.kitchen_stock += item_quantity
                entry_to_change.to_buy = 0

            elif action == 'New stock to garage':
                entry_to_change.garage_stock += item_quantity
                entry_to_change.to_buy = 0

            elif action == 'Move from kitchen to garage':
                entry_to_change.kitchen_stock -= item_quantity
                entry_to_change.garage_stock += item_quantity

            elif action == 'Move from garage to kitchen':
                entry_to_change.kitchen_stock += item_quantity
                entry_to_change.garage_stock -= item_quantity

            elif action =='Use kitchen stock':
                    entry_to_change.kitchen_stock -= item_quantity

            else:
                entry_to_change.garage_stock -= item_quantity

            if entry_to_change.kitchen_stock < 0 or entry_to_change.garage_stock < 0:
                flash(f"You appear to have used or moved more {item_actioned} than were recorded as being at that location. \n Please check and re-enter")
            else:
                db.session.commit()
                flash (f"Stock level of {item_actioned} successfully updated. \n There are {entry_to_change.kitchen_stock} {item_actioned} left in the kitchen \n and {entry_to_change.garage_stock} left in the garage") 
        else:
            flash('Invalid Entry')

    return render_template("update_stock.html", form=form)



@app.route('/show_stock', methods=('GET','POST'))
def show_stock():
    
    form = SelectView()
    if Stock_list.query.all() is None:
        item_choices = []
    else:  
        item_choices=Stock_list.query.order_by(Stock_list.item).all()
    each_item=[]
    for choice in item_choices:
        each_item.append(choice.item)
    form.item_name.choices=each_item
    all_stock = []
    item_summary = []
    item_transactions =[]
    view_option = ""
    if request.method == 'POST':
        if form.validate_on_submit():
            each_item_dict = {}
            if request.form['options'] == 'Show all items':
                items_from_bd = Stock_list.query.order_by(Stock_list.item).all()
                for item in items_from_bd:
                    total_stock = item.kitchen_stock + item.garage_stock
                    each_item_dict ={'item':item.item, 'kitchen_stock':item.kitchen_stock, 'garage_stock':item.garage_stock, 'minimum_stock':item.minimum_stock, 'total_stock':total_stock}
                    all_stock.append(each_item_dict)
                    view_option ="all"
            else:
                item_to_display = request.form['item_name']
                time_to_show = request.form['time_to_show']
                if time_to_show == "week":
                    days_to_show = 7
                elif time_to_show == 'month':
                    days_to_show = 31
                elif time_to_show == "year":
                    days_to_show = 365
                else:
                    days_to_show = 100000
                if Transactions.query.all() is None:
                    flash("No Tranactions to show")
                    item_tranaactions = []
                else:  
                    item_from_bd = Stock_list.query.filter_by(item=item_to_display).first()
                    total_stock = item_from_bd.kitchen_stock + item_from_bd.garage_stock
                    item_summary={'item':item_from_bd.item, 'kitchen_stock':item_from_bd.kitchen_stock, 'garage_stock':item_from_bd.garage_stock,'total_stock':total_stock, 'time_to_show':time_to_show, 'min_stock':item_from_bd.minimum_stock}

                    transactions_from_db = Transactions.query.filter(Transactions.item==item_to_display, Transactions.date > datetime.utcnow()-timedelta(days=days_to_show )).order_by(Transactions.date).all()
                    for transact in transactions_from_db:
                        transact_dict={'date':transact.date, 'number':transact.number_actioned, 'action':transact.action}
                        item_transactions.append(transact_dict)
                    view_option ="single"
        
            

    return render_template("show_stock.html", form=form, view_option=view_option, all_stock=all_stock, item_summary=item_summary,transactions=item_transactions)


@app.route('/new_item', methods=('GET','POST'))
def new_item():

    form1=SelectEdit()
    form=Dummyform()
    
    
    formtype='select' 
    if request.method =='POST':
        if request.form['submit']=='Select Change':
            if form1.validate_on_submit():    
                if request.form['options']=="new":
                    form = NewItem()
                    formtype='new'
                    
                elif request.form['options']=="remove":
                    form=DeleteItem()    
                    if Stock_list.query.all() is None:
                        item_choices = []
                    else:  
                        item_choices=Stock_list.query.order_by(Stock_list.item).all()
                    each_item=[]
                    for choice in item_choices:
                        each_item.append(choice.item)
                    form.item_name.choices=each_item
                    formtype='delete'

                else:
                    form = ChangeItem()
                    if Stock_list.query.all() is None:
                        item_choices = []
                    else:  
                        item_choices=Stock_list.query.order_by(Stock_list.item).all()
                    each_item=[]
                    for choice in item_choices:
                        each_item.append(choice.item)
                    form.item_name.choices=each_item
                    formtype='change'

        if request.form['submit'] == 'Store Item':
            if form.validate_on_submit():
                item_entered = request.form['item'].title()
                min_stock = request.form['min_stock']
                if not min_stock.isnumeric() or int(min_stock)<0:
                    min_stock = 0
                    flash('Invalid value entered for minimum stock - Minimum stock level set to 0:  ')
                duplicate_entry  = Stock_list.query.filter_by(item=item_entered).first()
                if duplicate_entry:
                    flash(f'New item - {item_entered} - is already in the the Stock List ')
                else:
                    item_to_add = Stock_list(item=item_entered, kitchen_stock=0, garage_stock=0, minimum_stock=min_stock, barcode=0)
                    db.session.add(item_to_add)
                    db.session.commit()
                    flash(f'New item - {item_entered} - entered successfully')
                
                

        if request.form['submit'] == 'Delete Item':
            if form.validate_on_submit():
                item_entered = request.form['item_name']
                Stock_list.query.filter_by(item=item_entered).delete()
                Transactions.query.filter_by(item=item_entered).delete()
                db.session.commit()
                flash(f'{item_entered} has been deleted')


        if request.form['submit'] == 'Edit Item':
            if form.validate_on_submit():
                item_entered = request.form['item_name']
                if request.form['new_name'] == "":
                    new_name = item_entered
                else:
                    new_name=request.form['new_name'].title()
                if request.form['new_min_stock'] == "":
                     min_stock=Stock_list.query.filter_by(item=item_entered).first().minimum_stock
                else:
                    min_stock=(request.form['new_min_stock'])
                    if  not min_stock.isnumeric() or int(min_stock)<0:
                        min_stock = 0 
                        flash('Invalid value entered for minimum stock - Minimum stock level set to 0:  ')
                entry  = Stock_list.query.filter_by(item=item_entered).first()
                entry.item = new_name
                entry.minimum_stock = min_stock
                db.session.commit()
                flash(f'item - {item_entered} - changed to {new_name} with minimum stock of {min_stock}')

        

        


    return render_template('new_item.html', formtype=formtype,form1=form1,form=form)

@app.route('/shopping_list', methods=('GET','POST'))
def shopping_list():
    data_dict={}
    select_form=SortShopList()
    if request.method == 'POST':
        if select_form.validate_on_submit():
            if request.form['submit']=='Choose Sorting Method':
                sort_on = request.form['options']
                data_dict=generate_sorted_list(sort_on)
        else:
            for key in request.form:
                entry_to_change = Stock_list.query.filter_by(item=key).first()
                change =request.form[key]
                if change == "":
                    change=0
                change=int(change)
                entry_to_change.to_buy = change
            db.session.commit()

    return render_template('shopping_list.html',form1=select_form, data=data_dict)


@app.route('/printable_shopping_list')
def printable_shopping_list():
    list_for_printing_dict = generate_shopping_list_for_printing()
    print(list_for_printing_dict)
    return render_template('printable_shopping_list.html',data=list_for_printing_dict)



    
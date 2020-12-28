from datetime import datetime, timedelta
from flask import render_template, request, url_for, flash
from flask_sqlalchemy.utils import sqlalchemy_version
from models import Stock_list,Transactions
from app import app
from forms import NewItem, StockUpdate, SelectView
from models import db


@app.route('/', methods=('GET','POST'))
@app.route('/update_stock', methods=('GET','POST'))
def update_stock():

    form = StockUpdate()
    item_choices=Stock_list.query.order_by(Stock_list.item).all()
    each_item=[]
    for choice in item_choices:
        each_item.append(choice.item)
    form.item_name.choices=each_item

    if form.validate_on_submit():   
        item_actioned = request.form['item_name']
        item_quantity = int(request.form['item_quantity'])
        print(type(item_quantity))
        action = request.form['actions']
        item_to_add = Transactions(action=action, number_actioned=item_quantity,stock_list_item=item_actioned)
        db.session.add(item_to_add)
        db.session.commit()
        entry_to_change = Stock_list.query.filter_by(item=item_actioned).first()

        if action == 'New stock to kitchen':
            entry_to_change.kitchen_stock += item_quantity

        elif action == 'New stock to garage':
            entry_to_change.garage_stock += item_quantity

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
        

    return render_template("update_stock.html", form=form)



@app.route('/show_stock', methods=('GET','POST'))
def show_stock():
    form = SelectView()
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
                    each_item_dict ={'item':item.item, 'kitchen_stock':item.kitchen_stock, 'garage_stock':item.garage_stock, 'total_stock':total_stock}
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

                item_from_bd = Stock_list.query.filter_by(item=item_to_display).first()
                total_stock = item_from_bd.kitchen_stock + item_from_bd.garage_stock
                item_summary={'item':item_from_bd.item, 'kitchen_stock':item_from_bd.kitchen_stock, 'garage_stock':item_from_bd.garage_stock,'total_stock':total_stock, 'time_to_show':time_to_show}

                transactions_from_db = Transactions.query.filter(Transactions.stock_list_item==item_to_display, Transactions.date > datetime.utcnow()-timedelta(days=days_to_show )).order_by(Transactions.date).all()
                for transact in transactions_from_db:
                    transact_dict={'date':transact.date, 'number':transact.number_actioned, 'action':transact.action}
                    item_transactions.append(transact_dict)
                view_option ="single"

            

    return render_template("show_stock.html", form=form, view_option=view_option, all_stock=all_stock, item_summary=item_summary,transactions=item_transactions)





@app.route('/new_item', methods=('GET','POST'))
def new_item():
    form = NewItem()
    if form.validate_on_submit():
        item_entered = request.form['item'].title()
        min_stock =request.form['min_stock']
        duplicate_entry  = Stock_list.query.filter_by(item=item_entered).first()
        if duplicate_entry:
            flash(f'New item - {item_entered} - is already in the the Stock List ')
        else:
            item_to_add = Stock_list(item=item_entered, kitchen_stock=0, garage_stock=0, minimum_stock=min_stock, barcode=0)
            db.session.add(item_to_add)
            db.session.commit()
            flash(f'New item - {item_entered} - entered successfully')
    return render_template('new_item.html', form=form)



    
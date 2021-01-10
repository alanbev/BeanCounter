from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators
from wtforms.fields.core import BooleanField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from models import Stock_list, db
from app import app

class Dummyform(FlaskForm):
    item=StringField('')

class SelectEdit(FlaskForm):
    options=RadioField(choices=[('new', 'Add New Item to Stock List'),('remove','Remove Item From Stock List'),('edit', 'Edit Name or Minimum Stock of Item')], default='new' ,validators=[DataRequired()])
    submit=SubmitField ('Select Change')

class NewItem(FlaskForm):
    """form for new item page"""
    item = StringField('Item_Description', validators=[DataRequired(), Length(min=2,max=100)])
    min_stock = IntegerField('Minimum Stock',validators=[DataRequired(),NumberRange(min=0)])
    submit = SubmitField('Store Item')

class DeleteItem(FlaskForm):
    item_name = SelectField('Item to Delete', validators=[DataRequired()])
    submit = SubmitField('Delete Item')
    confirm = BooleanField('Confirm Delete',validators=[DataRequired()])

class ChangeItem(FlaskForm):
    item_name = SelectField('Item to Edit',validators=[DataRequired()])
    new_name = StringField('New name for Item')
    new_min_stock = IntegerField('New Minimum Stock')
    submit = SubmitField('Edit Item')




class StockUpdate(FlaskForm):
    """"form for update stock view"""
    item_name = SelectField('Stock Item', validators=[DataRequired()])
    item_quantity =IntegerField('Quantity',validators=[DataRequired(),NumberRange(min=1)])
    actions = RadioField(choices=['New stock to kitchen', 'New stock to garage', 'Move from kitchen to garage', 'Move from garage to kitchen', 'Use kitchen stock','Use garage stock'],validators=[DataRequired()])

    submit = SubmitField('Enter', validators=[DataRequired()])

class SelectView(FlaskForm):
    options = RadioField(choices=['Show all items', 'Detailed view of single item'],validators =[DataRequired()])
    item_name = SelectField('Item to view') 
    time_to_show = RadioField('Show actions for last:',choices =['week', 'month', 'year','all'], default='week')
    submit = SubmitField('Show selection')

class SortShopList(FlaskForm):
    options = RadioField(choices=[('name','Sort by Item Name'), ('percent','Sort by percent of Minimum Stock'),('days','Sort by predicted days to minimum stock')], validators=[DataRequired()])
    submit = SubmitField('Choose Sorting Method')



    
    






    
    



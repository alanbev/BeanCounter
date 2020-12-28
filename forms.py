from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.fields.core import RadioField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from models import Stock_list, db
from app import app

class NewItem(FlaskForm):
    """form for new item page"""
    item = StringField('Item_Description', validators=[DataRequired(), Length(min=2,max=100)])
    min_stock = IntegerField('Minimum Stock',validators=[DataRequired()])
    submit = SubmitField('Store item')

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


    
    






    
    



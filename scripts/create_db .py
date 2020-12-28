import os,sys
sys.path.append(os.getcwd())
from main import db 
import models, config
from app import app


if __name__ == "__main__":
    db.create.all()

    

from app import app # import our Flask app
import views
import models

if __name__ == '__main__':
   
    app.run(debug=True)
    
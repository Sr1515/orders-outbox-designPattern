from main import app

@app.route('/reci/id')
def homePage():
    return "it's work!"
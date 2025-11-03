from flask import request, render_template
from main import app
from models.receipts import Receipts

@app.route('/receipts', methods=['POST'])
def showReceipts():
    
    data = request.get_json()
    
    print(data['id'])
    
    if not data:
        return "Missing receipt ID", 400
    
    if not data['id']:
        return "Missing receipt ID", 400
    
    receipt = Receipts.query.get(data['id'])
    
    if not receipt:
        return "Receipt not found", 404
    
    return render_template('receipt.html', receipt = receipt)
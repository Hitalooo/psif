from flask import Flask, request, render_template

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

@app.route('/', methods=['GET', 'POST'])
def index():
    total = 0
    checked_items = {}
    
    if request.method == 'POST':
      
        for key, value in request.form.items():
            try:
               
                total += float(value)
                checked_items[key] = True
            except ValueError:
               
                continue
    
    return render_template('index.html', total=total, checked_items=checked_items)


if __name__ == '__main__':
    app.run(debug=True)

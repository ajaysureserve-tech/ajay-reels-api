from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    # Ye line aapke naye index.html ko load karegi
    return render_template('index.html')

# Baki ka aapka purana download wala code yahan rehne dein
if __name__ == "__main__":
    app.run(debug=True)

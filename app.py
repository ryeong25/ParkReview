from flask import Flask, render_template


app = Flask(__name__)


@app.route('/detail')
def detail():
    return render_template("index.html")


@app.route('/')
def main():
    return render_template("mainpage.html")

@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/footer')
def footer():
    return render_template('footer.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
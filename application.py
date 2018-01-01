from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/catalog')
def showCatalog():
	return "All item in the catalog"

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)
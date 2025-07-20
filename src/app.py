from flask import Flask

# Create a Flask web server
app = Flask(__name__)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello, World from Kubernetes and Helm!\n'

if __name__ == '__main__':
    # Run the app on 0.0.0.0 to be publicly accessible from within the container
    app.run(host='0.0.0.0', port=8080)
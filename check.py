from flask import Flask
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Adjust the level as needed

@app.route('/')
def index():
    try:
        # Your code here
        return "Success"
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True)

from app import app
import logging

# Set up logging
logging.basicConfig(
    filename="flask_app.log",  # Log file name
    level=logging.INFO,  # Logging level
    format="%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
)

# Optionally redirect Flask's default logger to file
app.logger.addHandler(logging.FileHandler("flask_app.log"))
app.logger.setLevel(logging.INFO)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

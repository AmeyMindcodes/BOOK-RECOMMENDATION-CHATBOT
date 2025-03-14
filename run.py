from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Use environment variables for port if available (for production)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=os.environ.get("DEBUG", "True") == "True", 
            host='0.0.0.0', 
            port=port) 
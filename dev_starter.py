from app import create_app
"""
Run this file to start the app in the IDE without flask support
"""
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

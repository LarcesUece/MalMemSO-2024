from src import create_app, initialize

app = create_app()
initialize()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

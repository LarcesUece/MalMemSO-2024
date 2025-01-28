from flask import Flask

app = Flask(__name__)
app.config.from_object("config.Config")

from src import views, report

report.create_report_file()

if __name__ == "__main__":
    app.run(debug=True)

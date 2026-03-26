from flask import Flask

app = Flask("serverv2", static_url_path="/", static_folder="../docs")

@app.route('/')
def index():
    print(app.static_folder)
    print(app.static_url_path)
    return app.send_static_file('index.html')

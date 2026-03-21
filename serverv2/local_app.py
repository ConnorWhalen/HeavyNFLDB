from flask import Flask

app = Flask("serverv2")

@app.route('/')
def index():
    print(app.static_folder)
    print(app.static_url_path)
    return app.send_static_file('index.html')

from flask import Flask, send_from_directory
from resources.threads_serve import views
app = Flask(__name__, template_folder='./assets/templates/', static_url_path='/assets')

app.config['images'] = './threads'

app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/<board>/<no>', view_func=views.thread)

@app.route('/threads/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['images'], filename)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
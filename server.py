from flask import Flask, request, send_from_directory, jsonify
import os

from mod_updater import version_exists, update_jar

app = Flask(__name__, static_folder='frontend', static_url_path='')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/update', methods=['POST'])
def update():
    jar = request.files.get('jar')
    target_version = request.form.get('version', '').strip()
    modrinth_id = request.form.get('modrinth_id', '').strip()
    curse_id = request.form.get('curse_id', '').strip()
    curse_key = request.form.get('curse_key', '').strip()

    if not all([jar, target_version, modrinth_id, curse_id]):
        return 'Missing parameters', 400

    os.makedirs('uploads', exist_ok=True)
    tmp_path = os.path.join('uploads', jar.filename)
    jar.save(tmp_path)

    if version_exists(modrinth_id, curse_id, target_version, curse_key):
        return jsonify({'status': 'exists'})

    out_path = update_jar(tmp_path, target_version)
    return send_from_directory(os.path.dirname(out_path), os.path.basename(out_path), as_attachment=True)


if __name__ == '__main__':
    app.run(port=5000, debug=True)

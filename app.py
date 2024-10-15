import os
import hashlib
from flask import Flask, request, render_template, redirect

app = Flask(__name__)
UPLOADS_FOLDER = 'C:\\Users\\Dell\\Edi project\\static\\uploads'

def get_file_hash(file_path):
    """Generate a hash for a given file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicate_files(folder_path):
    """Find duplicate files based on their content within the given folder."""
    file_hashes = {}
    duplicate_files = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_hash = get_file_hash(file_path)
            if file_hash in file_hashes:
                duplicate_files.append(file_path)
            else:
                file_hashes[file_hash] = file_path

    return duplicate_files

def delete_files(file_paths):
    """Delete the given files."""
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except OSError as e:
            print(f"Error deleting file: {file_path}")
            print(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        folder_path = request.form.get('folder_path')

        if folder_path and os.path.isdir(folder_path):
            file_paths = []
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    file_paths.append(file_path)

            duplicate_files = find_duplicate_files(folder_path)

            if duplicate_files:
                return render_template('results.html', duplicate_files=duplicate_files)

    return render_template('index.html')

@app.route('/delete_duplicates', methods=['POST'])
def delete_duplicates():
    duplicate_files = request.form.getlist('duplicate_files')
    file_names = [os.path.basename(file_path) for file_path in duplicate_files]
    return render_template('confirm_delete.html', file_names=file_names, duplicate_files=duplicate_files)

@app.route('/confirm_deletion', methods=['POST'])
def confirm_deletion():
    file_paths = request.form.getlist('file_paths')
    delete_files(file_paths)
    return redirect('/delete_success')

@app.route('/delete_success')
def delete_success():
    return render_template('delete_success.html')

# Custom filter to zip two lists
@app.template_filter('zip_lists')
def zip_lists(a, b):
    return zip(a, b)

if __name__ == '__main__':
    app.run(debug=True)

import os, shutil
from flask import Flask, render_template, request, make_response
from werkzeug import secure_filename


# Setting up the relative directories
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
CERTS_FOLDER = os.path.join(APP_ROOT, 'Certs')
USED_CERTS_FOLDER = os.path.join(APP_ROOT, 'Used_Certs')

# Creating the app
app = Flask(__name__)

# Putting the directory names in app.config ... not sure why :-|
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CERTS_FOLDER'] = CERTS_FOLDER
app.config['USED_CERTS_FOLDER'] = USED_CERTS_FOLDER

def get_first_cert():
    # Find the first file in alphanumeric order in the Certs folder
    files = os.listdir(path=app.config['CERTS_FOLDER'])
    first_cert = ''
    for file in sorted(files):
        if file.endswith('.txt'):
            first_cert = file
            break

    if first_cert == '':
        print('No cert found!')
        return  first_cert

    # Returning the name of the file found, empty if not found
    return first_cert


def transform(text_file_contents):
    # Find the next available Cert
    first_cert = get_first_cert()

    # Somehow combine cert and uploaded file contents
    text_file_contents = text_file_contents.replace("=", ",")

    # Move Cert from New to Used directory
    shutil.move(os.path.join(app.config['CERTS_FOLDER'], first_cert), os.path.join(app.config['USED_CERTS_FOLDER'], first_cert))

    # Return a string with the new file contents
    return text_file_contents


@app.route("/")
def form():
    return render_template('page.html')


@app.route('/transform', methods=["POST"])
def transform_view():
    # Get the uploaded file from the Post
    file = request.files['data_file']
    if not file:
        print("No file")
        return "No file"

    # Save the file to uploads, not necessary since we're streaming on the next line, but just in case
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

    # Read the entire file contents into a string
    file_contents = file.stream.read().decode("utf-8")

    # Combine the file with a Cert
    result = transform(file_contents)

    # Make a response that contains the result in a file
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.txt"

    return response


if __name__ == "__main__":
    app.run(debug =True)

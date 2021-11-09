from flask import Flask, render_template, Response,send_from_directory, request
import os, cv2
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from exercises.dumbell_press_video import dumbell_press
#Initialize the Flask app
app = Flask(__name__)

@app.route('/output', methods=['POST','GET'])
def output():
    if request.method == 'POST':
        
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        print(file_path)

        vid_name = dumbell_press(file_path)
        vid_name = vid_name.split('/')[-1]
        
        return render_template('output.html',video_out=vid_name)


@app.route('/uploads/<filename>')
def upload_vid(filename):
    return send_from_directory('uploads', filename)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

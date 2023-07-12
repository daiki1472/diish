
#anacondaで行う
#conda create -n flasktest python=3.9
#conda activate flasktest
#conda install flask
#conda install tensorflow
#conda install keras
#conda install pillow
#conda install beautifulsoup
#conda install  requests

import os
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image
import numpy as np

classes = ['fugucuisine','nabe','nimono','okonomiyaki','osushi','soba','tonkatsu','udon','yakiniku','yakisoba','yakitori','yakiudon']
image_size = 150
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = load_model('./model.h5')#学習済みモデルをロード

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/geek', methods=['GET', 'POST'])
def geek():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            img = image.load_img(filepath,target_size=(image_size,image_size))
            img = image.img_to_array(img)
            img = img / 255.0 
            data = np.array([img])
            result = model.predict(data)[0]
            predicted = result.argmax()
            pred_answer = "これは " + classes[predicted] +  " の画像です"
            predicted_class = classes[predicted]  # これはモデルの予測結果です
            ingredients = ingredients_dict[predicted_class]
            imagefile_path = f"./static/images/{classes[predicted]}.jpg"
    return render_template('geek.html',answer=pred_answer,imagefile=filepath, answer_image=imagefile_path,ingredients=ingredients)


ingredients_dict = {
    'nimono': ['レンコン', '椎茸', '卵', 'ニンジン', '醤油', '砂糖', 'みりん'],
    'fugucuisine': ['材料7', '材料8', '材料9'],
    'nabe': ['材料4', '材料5', '材料6'],
    'okonomiyaki': ['材料1', '材料2', '材料3'],
    'osushi': ['材料1', '材料2', '材料3'],
    'soba': ['材料1', '材料2', '材料3'],
    'tonkatsu': ['材料1', '材料2', '材料3'],
    'udon': ['材料1', '材料2', '材料3'],
    'yakisoba': ['材料1', '材料2', '材料3'],
    'yakitori': ['材料1', '材料2', '材料3'],
    'yakiudon': ['材料1', '材料2', '材料3'],
    # 他の料理も同様に...
}


if __name__ == "__main__":
    app.run(debug=True)
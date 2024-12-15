import os
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, redirect
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Initialize Flask app
app = Flask(__name__)

# Configuration paths
UPLOAD_FOLDER = 'uploads'
MODEL_PATH = 'model3.h5'
CSV_PATH = 'solutions.csv'

# Create upload folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load model and solutions
model = load_model(MODEL_PATH)
solutions_df = pd.read_csv(CSV_PATH)

# Preprocess input image
def preprocess_image(image_path):
    img = load_img(image_path, target_size=(128, 128))  # Resize image to model input
    img_array = img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Predict and get solution
def get_prediction(image_path):
    processed_img = preprocess_image(image_path)
    prediction = model.predict(processed_img)
    class_index = np.argmax(prediction)
    confidence = np.max(prediction)

    # Map prediction to class labels and solution
    class_labels = solutions_df['Label'].unique()
    disease_label = class_labels[class_index]
    solution_row = solutions_df[solutions_df['Label'] == disease_label]

    if not solution_row.empty:
        disease_name = solution_row['Disease Name'].values[0]
        crop_name = solution_row['Crop Name'].values[0]
        solution = solution_row['Solution'].values[0]
    else:
        disease_name = "Unknown Disease"
        crop_name = "Unknown Crop"
        solution = "No solution available."

    return crop_name, disease_name, solution, confidence

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle image upload
        if 'image' not in request.files:
            return redirect(request.url)
        
        image = request.files['image']
        if image.filename == '':
            return redirect(request.url)
        
        if image:
            image_path = os.path.join(UPLOAD_FOLDER, image.filename)
            image.save(image_path)

            # Get prediction
            crop_name, disease_name, solution, confidence = get_prediction(image_path)

            return render_template("index.html", 
                                   crop_name=crop_name, 
                                   disease_name=disease_name, 
                                   solution=solution,
                                   confidence=confidence,
                                   image_path=image_path)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

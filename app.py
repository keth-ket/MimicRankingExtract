from PIL import Image
import pytesseract
from wand.image import Image as Img 
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import numpy as np 
from collections import Counter
import os
import cv2
import re
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Define where to save uploaded videos
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS_VIDEO = {'mp4'}
ALLOWED_EXTENSIONS_TEXT = {'txt'}

#return true if the file has the required extension
def allowed_file_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_VIDEO

def allowed_file_text(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_TEXT

def cleanup_uploads():
    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)
        os.remove(file_path)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files or 'members' not in request.files:
        return "No file part"

    video = request.files['video']
    members = request.files['members']
    
    if video.filename == '' or members.filename == '':
        return "No selected file"

    if video and allowed_file_video(video.filename) and members and allowed_file_text(members.filename):
        # Cleanup previous uploads
        cleanup_uploads()
        
        # Save video file
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
        video.save(video_path)

        # Save text file
        text_path = os.path.join(app.config['UPLOAD_FOLDER'], members.filename)
        members.save(text_path)
        
        members_attacked, score_result = analyzing_everything(video_path, text_path)
        
        # Return a response with links to the uploaded files
        return f"""
            <h2>Data analyzing successfully!</h2>
            <h4>Members Attacked: </h4>
            <pre>{members_attacked}</pre>
            <h4>Score: </h4>
            <pre>{score_result}</pre>
        """
    
    return "Invalid file type"

#name path to image frames
image_frames = 'image_frames'
def files(fileName):
    #remove if the folder exists
    try:
        os.remove(image_frames)
    except OSError:
        pass
    
    #make a new one if there's not one
    if not os.path.exists(image_frames):
        os.makedirs(image_frames)
        
    #create video capture object
    src_vid = cv2.VideoCapture(fileName)
    return (src_vid)
    
def process(src_vid):
    index = 0 
    while src_vid.isOpened():
        ret, frame = src_vid.read()
        if not ret:
            break
        #name each frame and save as png
        name = './image_frames/frame' + str(index) + '.png'
        
        #save every 50th frame
        if index % 50 == 0:
            print('Extracting frames...' + name)
            cv2.imwrite(name, frame)
            
        index = index + 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    src_vid.release()
    cv2.destroyAllWindows()

def get_text():
    all_text = []
    for i in os.listdir(image_frames):
        my_image = Image.open(image_frames + "/" + i)
        text = pytesseract.image_to_string(my_image, lang='eng') 
        # Split text into lines and remove empty ones
        filtered_lines = [line for line in text.split("\n") if line.strip()]
        
        all_text.extend(filtered_lines)  # Append non-empty lines

    return all_text

#read the member file a return a dictionary with members name are key
def readMembers(fileName):
    with open(fileName, "r", encoding="utf-8") as file:
        return {line.strip(): [] for line in file if line.strip()}

#member with name that can only partially scanned due to weird font   
def nameExist(name, name_map):
    if "NN3" in name:
        return (True, "MNN3")
    elif "aXe" in name:
        return (True, "FaXe")
    elif name == "Rusrks" or name == "Ruerks":
        return (True, "RUBIKS")
    
    for member in name_map:
        if member.lower() in name.lower():
            return (True, member)
    return (False, "") 

def processData(textData, name_map):   
    
    #process everyline
    for i in range(0, len(textData)):
        name = textData[i].strip()
        #make sure it's not out of bound
        if i + 1 < len(textData):
            value_str = textData[i + 1].strip()
        else:
            continue
        
        #take only the last word and get rid of , and M
        cleaned_value = value_str.split()[-1].replace(',', '').replace('M', '')
        
        #the the cleaned value is only digit, our data is good to further process
        if cleaned_value.isdigit():
            #convert to int for easier comparison
            value = int(cleaned_value)
            # Check if the name exists in the name_map
            exists, matched_name = nameExist(name, name_map)
            if exists:
                # If name exists, append the value to the corresponding name's list
                name_map[matched_name].append(value)

#there will be repeated value due to screen short overlaped 
#might contains wrong value due to noise
#only take the most repeated value as final result
def most_repeated_number(name_map):
    result = {}
    
    for name, values in name_map.items():
        if values:  # Only process non-empty lists
            count = Counter(values)  # Count the occurrences of each value
            most_common = count.most_common(1)  # Get the most common value
            result[name] = most_common[0][0]  # Store the most repeated number  
            
    # Sort the result based on the size of the most common number
    sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=True)

    # Convert sorted result back into a dictionary
    sorted_result_dict = dict(sorted_result)
    
    return sorted_result_dict              

def analyzing_everything(video_path, text_path):
    #process the vid and the members file
    vid = files(video_path)
    process(vid)
    
    text = get_text()
    
    name_map = readMembers(text_path)
    processData(text, name_map)
    
    final_result = most_repeated_number(name_map)      
    members_attacked = ""
    score_result = ""
    index = 1
    for name, score in final_result.items():
        members_attacked += name + "\n" 
        score_result += str(score) + "\n"
        index += 1
    total = "Total member attacked: " + str(index - 1) + "\n"
    members_attacked += total
    
    return(members_attacked, score_result)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # For example, using port 1000

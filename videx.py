from PIL import Image
import pytesseract
from wand.image import Image as Img 
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import numpy as np 

import os
import cv2
import re

from collections import Counter

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
            #print('Extracting frames...' + name)
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

if __name__ == '__main__':
    
    #process video
    vid = files("recordingVideo.mp4")
    process(vid)
    
    text = get_text()
    #print(text)       
    name_map = readMembers("members.txt")
    processData(text, name_map)

    final_result = most_repeated_number(name_map)
    with open("Result_Name.txt", "w", encoding="utf-8") as nameFile, open("Result_Score.txt", "w", encoding="utf-8") as resultFile:
        index = 1
        for name, score in final_result.items():
            nameFile.write(name + "\n") 
            resultFile.write(str(score) + "\n")  
            index += 1
        total = "Total member attacked: " + str(index - 1) + "\n"
        nameFile.write(total)
             
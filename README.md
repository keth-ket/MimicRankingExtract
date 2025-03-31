# Mimic Ranking Extraction from Recording Videos
## Overview
This program extracts text from a recording video, using OCR. Right now, it only supports .mp4 video. 
## Features
- Scan the video and take a snapshot every 2 seconds.
- Scan through the images and extract all the text
- Refine the data with provided information from members.txt
- Output final data to text files in suitable format
## Installation
### Windows
There's a built in .exe file in dist folder that is compatible with Windows. You can simply use it
### Windows/Linux/MacOS
In the case you want to run the python script.
1. Clone the repo using git
   ```sh
   git clone https://github.com/keth-ket/MimicRankingExtract.git
   ```  
   OR download the zip file and unzip it to a suitable folder
2. Install all the neccesary dependencies: first install `pip` and `python 3.x` then
   ```sh
   pip install pillow pytesseract wand nltk numpy opencv-python
   ```  
3. Install ImageMagik for wand
     
4. Verify you can run the program 
  ```sh
  python videx.py
```  
## Usage
### Using .exe file
Copy your recording video to dist folder and rename it to "recordingVideo.mp4" 
Copy your members data, each member should be on a newline to "members.txt"
Double click the .exe to run
Once it's done running, you can check "Result_Names.txt" and "Result_Scores.txt", they are in descending order of Damage.
### Using python script
Copy your recording video to dist folder and rename it to "recordingVideo.mp4" 
Copy your members data, each member should be on a newline to "members.txt"
In command line
```sh
python videx.py
```
Once it's done running, you can check "Result_Names.txt" and "Result_Scores.txt", they are in descending order of Damage.
## Author's note
This program is developed by Ket (Alice) and only refined for SaltyHearts current members. The program is designed for SOULS game and not for anything else. 
You might need to refine the program to your own usage. 
If there's any issues, please report.
## License
This project is for **personal and non-commercial use only**.  
Unauthorized commercial usage, distribution, or modification is not permitted.  

For inquiries regarding commercial use, please contact.

   
  

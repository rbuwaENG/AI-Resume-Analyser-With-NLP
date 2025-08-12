# **AI Resume Analyser With NLP on Streamlit**

![Python 3.6](https://img.shields.io/badge/Python-3.6-brightgreen.svg)

• Please do ⭐ the repository, if it helped you in anyway.

## Preview
![Click HERE To View](https://github.com/Akash1070/AI-Resume-Analyser-With-NLP/blob/main/Screenshot.png)

## Deployment
 
    1. Model Building and Tuning
    2. Building Flask API
   
## Installation

To install the libraries used in this project. Follow the 
below steps:

```bash

#SET UP:

# 1. INSTALL BELOW LIBRARIES

        #pip install -r requirements.txt

        # pip install nltk

        # pip install spacy==2.3.5

        # pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz

        # pip install pyresparser

# 2. CREAT A FOLDER AND NAME IT (e.g. resume)

        #2.1 create two more folders inside this folder (Logo and Uploaded_Resumes)
        #2.2 create two python files (App.py and Courses.py)

# 3. START YOUR SQL DATABASE


# 4. CONTINUE WITH THE FOLLOWING CODE...

import streamlit as st
import pandas as pd
import base64,random
import time,datetime
#libraries to parse the resume pdf files
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos
import pafy #for uploading youtube videos
import plotly.express as px #to create visualisations at the admin session
import nltk
nltk.download('stopwords')

```
    
## Running Flask Api

To run tests, run the following command

```bash
  python app.py
```


   

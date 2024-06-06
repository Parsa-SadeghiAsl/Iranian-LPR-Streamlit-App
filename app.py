import streamlit as st
import cv2
import pandas as pd
from settings import settings
import numpy as np
import math
from src.sort import *
import cvzone
import torch
from src.PlateGen import PlateGen
from src.plate_reader import PlateReader
from pathlib import Path
from ultralytics import YOLO
from datetime import datetime
from src.SQLManager import DatabaseManager
import base64
from io import BytesIO

# Setting page layout
st.set_page_config(

    page_title="Computer-Vision LPR",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Main page heading
st.title("Computer-Vision LPR")

# Database connection and initialization
db_manager = DatabaseManager('data/database.db')
db_manager.create_recognized_plates_table()

# Sidebar
st.sidebar.header("Settings")

# Model Loader
def load_model(model_path):
    model = YOLO(model_path)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    return model


PlateDetectionModelPath = Path(settings.DETECTION_MODEL)
PlateReaderModelPath = Path(settings.READER_MODEL)

try:
    PlateDetectionModel = load_model(PlateDetectionModelPath)
    PlateReaderModelPath = load_model(PlateReaderModelPath)
    CLASS_NAMES_DICT = PlateReaderModelPath.model.names
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {PlateDetectionModelPath} and {PlateReaderModelPath}")
    st.error(ex)


DetectionConfidence = float(st.sidebar.slider(
    "Select Plate Detection Confidence", 25, 100, 45)) / 100

ReaderConfidence = float(st.sidebar.slider(
    "Select Plate Reader Confidence", 25, 100, 45)) / 100
DataFrameCheck = st.sidebar.checkbox('Show Data Frame')
st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

#-----------------------------Tracking---------------------------
def Track(tracker, OriginalImg, detections, original_height, original_width):
    resultTracker = tracker.update(detections)
    for res in resultTracker:
        x1, y1, x2, y2, id= res
        x1, y1, x2, y2= int(x1), int(y1), int(x2), int(y2)
        w,h = x2-x1, y2-y1

        # Calculate scaling factors
        scale_x = original_width / 640
        scale_y = original_height / 640

        # Scale the coordinates
        x1_original = int(x1 * scale_x)
        y1_original = int(y1 * scale_y)
        x2_original = int(x2 * scale_x)
        y2_original = int(y2 * scale_y)
        cropped_image = OriginalImg[y1_original:y2_original, x1_original:x2_original]
        if id in PlatesId:
            continue
        else:
            try:
                platenum = PlateReader(PlateReaderModelPath, cropped_image, ReaderConfidence)
                if platenum != False:
                    
                    PlatesId.append(id)
                    OrgPlateFrame.image(cropped_image, 'Original Plate Picture', use_column_width=True)
                    PlateFrame.image(PlateGen(platenum), 'Generated Plate Number', use_column_width=True)
                    db_manager.save_recognized_plate(platenum[:2]+'-'+platenum[2]+'-'+platenum[3:-2]+'-'+platenum[-2:])
            except:
                continue
#--------------------------------------------------------------------

#----------------------------Plate Detection ------------------------
PlatesId = list()
def PlateDetection(image, tracker,conf):
    
    detections = np.empty((0,5))
    image = cv2.resize(image, (640,640))
    results = PlateDetectionModel(image, stream=True, verbose=False)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
            w,h = x2-x1, y2-y1

            # conf score
            ConfOfBox = math.ceil(box.conf[0]*100)/100
            if ConfOfBox > conf:
                currentArray = np.array([x1,y1,x2,y2,conf])
                detections = np.vstack((detections, currentArray))
                cvzone.cornerRect(image, (x1,y1,w,h), l=9, rt=1, colorR=(255,0,255))
    return tracker, detections, image
#--------------------------------------------------------------------

#----------------------------Video Is Selected-----------------------
if  source_radio == settings.VIDEO:

    col1, col2 = st.columns(2)
    ccol1, ccol2, ccol3 = st.columns(3)
    with ccol1:
        OrgPlateFrame = st.empty()
    with ccol2:
        st.write('')
    source_vid = st.sidebar.selectbox(
    "Choose a video...", settings.VIDEOS_DICT.keys())

    with open(settings.VIDEOS_DICT.get(source_vid), 'rb') as video_file:
      video_bytes = video_file.read()
    if video_bytes:
        with ccol3:
            PlateFrame = st.empty()
        with col1:
            st.video(video_bytes)

    if st.sidebar.button('Detect Video Objects'):
        with col2:
            try:
                vid_cap = cv2.VideoCapture(
                    str(settings.VIDEOS_DICT.get(source_vid)))
                st_frame = st.empty()
                tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
                while (vid_cap.isOpened()):
                    success, image = vid_cap.read()
                    if success:


                        # Plot the detected objects on the video frame
                        tracker, detections, res_plotted= PlateDetection(image,tracker, DetectionConfidence)
                        frame_width = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        frame_height = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        Track(tracker, image, detections, frame_height, frame_width)
                        res_plotted = cv2.resize(res_plotted, (720, 540))
                        st_frame.image(res_plotted,
                                    caption='',
                                    channels="BGR",
                                    use_column_width=True,
                                    )
                    else:
                        vid_cap.release()
                        break
            except Exception as e:
                st.sidebar.error("Error loading video: " + str(e))
#--------------------------------------------------------------------
#----------------------------Webcam Is Selected------------------------

elif source_radio == settings.WEBCAM:
    col1, col2 = st.columns(2)
    ccol1, ccol2, ccol3 = st.columns(3)
    with ccol1:
        OrgPlateFrame = st.empty()
    with ccol2:
        st.write('') 
    source_webcam = settings.WEBCAM_PATH
    if st.sidebar.button('Detect Objects'):
        try:
            img_file_buffer = st.camera_input('Take a picture')
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            vid_cap = cv2.VideoCapture(source_webcam)
            with col1:
                raw_frame = st.empty()
            with col2:
                st_frame = st.empty()
            tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    raw = cv2.resize(cv2_img, (720, 540))
                    raw_frame.image(raw,
                                caption='',
                                channels="BGR",
                                use_column_width=True,
                                )
                
                    # Plot the detected objects on the video frame
                    tracker, detections, res_plotted= PlateDetection(cv2_img,tracker, DetectionConfidence)
                    frame_width = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    frame_height = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    Track(tracker, cv2_img, detections, frame_height, frame_width)
                    res_plotted = cv2.resize(res_plotted, (720, 540))
                    st_frame.image(res_plotted,
                                caption='',
                                channels="BGR",
                                use_column_width=True,
                                )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))

#--------------------------------------------------------------------
            

#----------------------------RTSP Is Selected-----------------------

elif source_radio == settings.RTSP:

    col1, col2 = st.columns(2)
    ccol1, ccol2, ccol3 = st.columns(3)
    with ccol1:
        OrgPlateFrame = st.empty()
    with ccol2:
        st.write('') 
    with ccol3:
        PlateFrame = st.empty()
        
    source_rtsp = st.sidebar.text_input("RTSP stream url:")
    st.sidebar.caption('Example URL: rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101')
    if st.sidebar.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_rtsp)
            with col1:
                raw_frame = st.empty()
            with col2:
                st_frame = st.empty()
            tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    raw = cv2.resize(image, (720, 540))
                    raw_frame.image(raw,
                                caption='',
                                channels="BGR",
                                use_column_width=True,
                                )
                
                    # Plot the detected objects on the video frame
                    tracker, detections, res_plotted= PlateDetection(image,tracker, DetectionConfidence)
                    frame_width = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    frame_height = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    Track(tracker, image, detections, frame_height, frame_width)
                    res_plotted = cv2.resize(res_plotted, (720, 540))
                    st_frame.image(res_plotted,
                                caption='',
                                channels="BGR",
                                use_column_width=True,
                                )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            vid_cap.release()
            st.sidebar.error("Error loading RTSP stream: " + str(e))
#--------------------------------------------------------------------
else:
    st.error("Please select a valid source type!")
#--------------------------------------------------------------------
def create_download_link(df, filename, link_text):
    # Create a BytesIO buffer for the Excel file
    excel_buffer = BytesIO()
    
    # Use openpyxl as the engine for Excel format
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    # Encode Excel data in base64
    b64 = base64.b64encode(excel_buffer.getvalue()).decode()
    
    # Create the download link
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{link_text}</a>'
    
    return href
# Show data table
if DataFrameCheck:
    lcol1, lcol2, lcol3 = st.columns(3)
    with lcol1:
        st.write('')
    with lcol3:
        st.write('') 
    with lcol2:
        st.subheader("DataBase Table ")

        dataframe = db_manager.get_all_recognized_plates()
        dataframe = dataframe.drop('id', axis=1)
        df = dataframe.copy(True)
        df['plate_text'] = df['plate_text'].str.split('-')
        # Display DataFrame table
        st.dataframe(df, use_container_width=True)

        # Create a download link for Excel
        download_link_excel = create_download_link(dataframe, 'PlateNumbersdata.xlsx', 'Download Excel')

        # Display the download link in the Streamlit app
        st.markdown(download_link_excel, unsafe_allow_html=True)

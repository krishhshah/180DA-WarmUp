import os
import cv2
import numpy as np
import pickle
import face_recognition as fr
import pyttsx3

engine = pyttsx3.init()


def main():

# generate encodings for similarity and recognition
    encodings, names = generate_encodings('./people/')
    # with open('people_encodings.pkl', 'rb') as f:
    #     encodings, names = pickle.load(f)
    print('generated encodings')
    print(encodings)

# start videocam
    # 0 for phone, 0 for macbook, 1 for external webcam
    video = cv2.VideoCapture(0)
    _, image_frame = video.read()
    cv2.imshow('Video', image_frame)

    while video.isOpened():

        _, image_frame = video.read()

# get resolution of the frame
        frame_width = int(video.get(3))
        frame_height = int(video.get(4))

        print('video ratio: ',frame_height,'x',frame_width)

# look for face
        if not has_face(image_frame):
            print('no face')
            cv2.imshow('Video', image_frame)
            continue
        
# check for similarity between encoded faces if face is found
        image_frame, encoding, (top, right, bottom, left) = find_face(image_frame) 
        results = fr.face_distance(encodings, encoding)
        match_i, similarity = np.argmin(results), 1 - np.min(results)
        
        if similarity < 0.5:
            cv2.imshow('Video', image_frame)
            continue
        print(names[match_i])
        
        cv2.putText(image_frame, f'{names[match_i]} ({100 * similarity:.2f}%)', (left, top - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,0), 2)
         
# face tracking relative to middle of frame
        face_midpoint = -((right + left)/2 - (frame_width/2))
        
        print('face coords: ',top,left)
        print('x midpoint: ', face_midpoint)

# dictate name of person found
        engine.setProperty('rate', 150) 
        engine.say(f'Hello {names[match_i]}!')
        engine.runAndWait()
                  
        cv2.imshow('Video', image_frame)
                          
        if cv2.waitKey(1) & 0xff == ord('q'):              
            break



def generate_encodings(directory, verbose=False):
    encodings, names = [], []
#encode all images with people in './people'
    for i,filename in enumerate(os.listdir(directory)):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            print(filename)
            _, enc, _ = find_face(fr.load_image_file(f))
            encodings.append(enc)
            names.append(filename.split('.')[0])
    return encodings, names

def has_face(img):
#check how many faces are in frame and return true if there is at least 1
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return len(fr.face_locations(img)) > 0

def find_face(img, name=None):
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#get all faces in the frame
    faces = fr.face_locations(img)
    if len(faces) == 0:
        return None, None
    biggest_i = 0
    biggest_face = 0

# calculate area of all the faces, and find which one is the biggest (~closest to camera)
    for i,(top,right,bottom,left) in enumerate(faces):
        face = (bottom - top) * (right - left)
        if face > biggest_face:
            biggest_face = face
            biggest_i = i
    encoding = fr.face_encodings(img)[biggest_i]
    top, right, bottom, left = faces[biggest_i]
    cv2.rectangle(img, (left, top), (right, bottom), (255,0,255), 2)
    return img, encoding, (top, right, bottom, left)

if __name__ == '__main__':
    main()
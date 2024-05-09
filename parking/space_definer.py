'''
Author: K.Tanjim Ahammad
Date:27.04.2024
Purpose: Creating rectangle from a image by clicking the left button of mouse and save the
rectangle position in a pickle file for futher use
paremeter: left click creat rectangle and right click delete the rectangle if mistake make 

'''
import cv2
import pickle
# size of the rectangle
width, height = 105, 48

# creaating pickle file to save
try:
    with open('area.pkl', 'rb') as f:
        pos_list = pickle.load(f)
except FileNotFoundError:
    pos_list = []

# saving fution
def save_positions():
    """Save the positions to a pickle file."""
    with open('area.pkl', 'wb') as f:
        pickle.dump(pos_list, f)
# manually identified the parking place 
def manual_pos(event, x, y, flags, params):
    """Handle mouse events to add or remove positions."""
    if event == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))
        save_positions()
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(pos_list):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                pos_list.pop(i)
                save_positions()
                break  # Stop loop after removing an item
# Loading the image 
while True:
    img = cv2.imread('example_image.png')
    if img is None:
        print("Failed to load image.")
        break

    for pos in pos_list:
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 2)

    cv2.imshow('test', img)
    cv2.setMouseCallback('test', manual_pos)
    if cv2.waitKey(1) & 0xFF == 27:  # Exit loop on pressing ESC
        break

cv2.destroyAllWindows()

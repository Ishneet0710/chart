import numpy as np
import cv2

def face_bbox(coords):
    keypoints_to_consider = [0, 1, 2, 3, 4, 5, 6, 11, 12]
    y_coords = [coords[::3][idx] for idx in keypoints_to_consider]
    x_coords = [coords[1::3][idx] for idx in keypoints_to_consider]

    x_body_range = max(x_coords) - min(x_coords)
    y_body_range = max(y_coords) - min(y_coords)
    ratio = x_body_range / y_body_range

    x_face = x_coords[:5]
    y_face = y_coords[:5]
    x_bar = np.mean(x_coords[:5])
    y_bar = np.mean(y_coords[:5])

    # Get largest |x_i - x_bar|
    x_max = -1
    for x_i in x_face:
        temp = abs(x_i - x_bar)
        if temp > x_max:
            x_max = temp

    # Get largest |y_i - y_bar|
    y_max = -1
    for y_i in y_face:
        temp = abs(y_i - y_bar)
        if temp > y_max:
            y_max = temp

    if ratio > 1:
        h_head = 2.5 * y_max
        w_head = 1.5 * h_head
    else:
        w_head = 2.5 * x_max
        h_head = 1.5 * w_head

    return (int(x_bar - 0.5*w_head), int(y_bar - 0.5*h_head), int(x_bar + 0.5*w_head), int(y_bar + 0.5*h_head))

def blur_face(frame, coords):
    x1, y1, x2, y2 = face_bbox(coords)
    range_to_blur = frame[y1:y2, x1:x2]
    range_to_blur = cv2.GaussianBlur(range_to_blur, (23, 23), 30)
    frame[y1:y2, x1:x2] = range_to_blur
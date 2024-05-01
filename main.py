import time

import cv2
import numpy as np


def task_1():
    img = cv2.imread('images/variant-6.png')  
    w, h = img.shape[:2]  
    w_new, h_new = map(lambda coord: coord * 2, [w, h])  
    img_new = cv2.resize(img, (w_new, h_new)) 
    cv2.imshow('New scaled image', img_new)  


def task_2():
    cap = cv2.VideoCapture(0)  
    down_points = (640, 480) 
    r_count, l_count, i = 0, 0, 0 
    while True:  
        ret, frame = cap.read() 
        if not ret:  
            break

 
        frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0: 
            c = max(contours, key=cv2.contourArea)  
            x, y, w, h = cv2.boundingRect(c)  
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  
           
            cv2.putText(frame, f'Слева: {l_count}', (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, f'Справа: {r_count}', (down_points[0] - 90, 20), cv2.FONT_HERSHEY_COMPLEX,
                        0.5, (0, 0, 0), 1, cv2.LINE_AA)
            if i % 10 == 0:  
            
                if x + (w // 2) > down_points[0] // 2:
                    r_count += 1
                elif x + (w // 2) < down_points[0] // 2:
                    l_count += 1

        
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break

        time.sleep(0.1)
        i += 1  

    cap.release() 


def extra_task():
    cap = cv2.VideoCapture(0)  
    down_points = (640, 480)  
    r_count, l_count, i = 0, 0, 0 
    fly = cv2.imread('fly64.png', cv2.IMREAD_UNCHANGED)  

    while True:  
        ret, frame = cap.read() 
        if not ret:  
            break

        frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0: 
            c = max(contours, key=cv2.contourArea)  
            x, y, w, h = cv2.boundingRect(c) 

            new_fly = cv2.resize(fly, (w if x + w < down_points[0] else down_points[0] - x,
                                       h if y + h < down_points[1] else down_points[1] - y))
            alpha_channel, fly_colors = new_fly[:, :, 3] / 255, new_fly[:, :, :3]  
       
            alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
            h_fly, w_fly = new_fly.shape[:2]  
            background_subsection = frame[y:(y + h_fly), x:(x + w_fly)]  
            
            composite = background_subsection * (1 - alpha_mask) + fly_colors * alpha_mask
            frame[y:(y + h_fly), x:(x + w_fly)] = composite  

          
            cv2.putText(frame, f'Слева: {l_count}', (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, f'Справа: {r_count}', (down_points[0] - 90, 20), cv2.FONT_HERSHEY_COMPLEX,
                        0.5, (0, 0, 0), 1, cv2.LINE_AA)
            if i % 10 == 0:  
              
                if x + (w // 2) > down_points[0] // 2:
                    r_count += 1
                elif x + (w // 2) < down_points[0] // 2:
                    l_count += 1

    
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break

        time.sleep(0.1)
        i += 1  

    cap.release()  


if __name__ == '__main__':
    task_1()
    # task_2()
    # extra_task()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

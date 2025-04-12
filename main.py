import cv2
import numpy as np
import pytesseract
import yt_dlp
import time
from PIL import Image

def extract_num(url_youtube, x, y, width, height, interval):
    try:
        # setting up yt-dlp to grab the stream url
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True 
        }
        
        # get stream url without downloading it 
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url_youtube, download=False)
            stream_url = info['url']
        
        print("stream url obtained successfully. yay.")
        
        # open the stream with OpenCV
        cap = cv2.VideoCapture(stream_url)
        
        if not cap.isOpened():
            raise Exception("couldnt open the stream, yt being yt prob.")
            
        print(f"stream started. extracting numbers in region ({x}, {y}, {width}, {height})...")
        print(f"updating every {interval} seconds. hit 'q' to quit.")
        
        next_check_time = time.time() + interval
        last_num = ""
        
        while True:
            current_time = time.time()
            
            # grab a new frame each loop so it looks smooth and doesnt freeze up
            ret, frame = cap.read()
            if not ret:
                print("couldnt read the frame oh god.")
                # tries to reconnect to the stream
                cap.release()
                time.sleep(1)
                cap = cv2.VideoCapture(stream_url)
                continue
            
            # extract the region of interest (ROI)
            roi = frame[y:y+height, x:x+width]
            
            # show the marked area (roi) (useful to debug)
            cv2.imshow('ROI', roi)
            
            # verifies if its time to do the ocr thing
            if current_time >= next_check_time:
                print(f"[{time.strftime('%H:%M:%S')}] processing OCR...")
                
                # puts the captured frame in b&w
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                
                # make it a pil image cause tesseract
                pil_img = Image.fromarray(gray)
                
                # extract text using OCR
                texto = pytesseract.image_to_string(pil_img, config='--psm 7 -c tessedit_char_whitelist=0123456789')
                
                # clean up the text since i only want numbers
                num = ''.join(c for c in texto if c.isdigit())
                
                # schedule the next check
                next_check_time = current_time + interval
                
                # if it finds a new number, updates it
                if num and num != last_num:
                    print(f"[{time.strftime('%H:%M:%S')}] detected number: {num}")
                    last_num = num
                
                cv2.imshow('grayscale image', gray)
            
            # verifies if q was pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # little pause to keep cpu from having a meltdown
            time.sleep(0.05)
            
        # freeing resources
        cap.release()
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    url_live = "" # replace with your youtube livestream URL
    
    x = 17
    y = 73
    width = 458
    height = 73
    interval = 10
    # setting to 10, but effective interval may be 20 due to processing time

    extract_num(url_live, x, y, width, height, interval)

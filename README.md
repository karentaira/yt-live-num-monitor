#YouTube Live Stream Number Monitor

Ok, so I made this program to monitor a Youtube live stream and capture a number shown-on-screen from a specific area of the video frame.
Along with it, there is a python script to grab a frame from your stream - extra useful because you'll need the parameters it returns (x, y, width and height) to use the main program.

Used:
- OpenCV for handling the video stream and grabbing frames;
- Tesseract to read the number from the image;

Why Python and not C++? 💔
- I chose Python totally against my will, but it's definitely a better choice since the code is WAY shorter and, in my case, I don't need to count every single second, so the advantages of using CPP would be kinda useless (still way more fun and prettier tho)
- If you need to count every second for your program, i highly recommend switching to CPP
- I'll use Firebase as the server/backend of an app that will store the detected number, and doing this in CPP would be EXTRA PAINFUL for no real benefit

How it works:
1. Use yt-dlp to grab the YouTube stream URL
2. OpenCV opens the stream and crops the region of interest (ROI)
3. Every X seconds, it captures a frame from that region
4. Turns the image grayscale and gives it to Tesseract (in a PIL image) to extract the digits
5. If it detects a new number, it logs it
6. You can press 'q' anytime to quit the program/stream.

⚠️ FYIs:
- this is meant for chill, non-intensive monitoring. if u want millisecond precision, this ain't it.
- my comments are indeed informal, but if u see this code and hate that, feel free to change it (ur boring tho)
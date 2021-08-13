# Ping Pong CV Referee
I used computer vision through OpenCV Libraries in order to track ping pong ball. Next, I attempt to calculate a homography using the edges of the table. Lastly, I apply the Delaunay effect for visuals and implement scorekeeping. All you need is a webcam and compter and you have got yourself an automated ping-pong referee.

## 1) Finding the lower and upper bounds based off of the color of the ball:
    -> Run range2.py with your respective image file and move sliders to keep relevant parts only

![Before](/images/before.jpeg?raw=true "Title")
![After](/images/after.jpeg?raw=true "Title")

## 2) Track the moving ping pong ball:
    -> Run ball_tracking.py with updated lower and upper values that were just found, run with respective video in arguments

![ExampleTracking](/images/bounceResult.gif?raw=true "Title")
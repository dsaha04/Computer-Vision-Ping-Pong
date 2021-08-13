# Ping Pong CV Referee
I used computer vision through OpenCV Libraries in order to track ping pong ball. Next, I attempt to calculate a homography using the edges of the table. Lastly, I apply the Delaunay effect for visuals and implement scorekeeping. All you need is a webcam and compter and you have got yourself an automated ping-pong referee.

## 1) Finding the lower and upper bounds based off of the color of the ball:
    -> Run range2.py with your respective image file and move sliders to keep relevant parts only

<div className="justify-content-between items-center">
<center>
    <img src="/images/before.jpeg" alt="Before" width="200"/>
    <span width="200"> </span>
    <img src="/images/after.jpeg" alt="After" width="200"/>
</center>
</div>



## 2) Track the moving ping pong ball:
    -> Run ball_tracking.py with updated lower and upper values that were just found, run with respective video in arguments

<div className="justify-content-between items-center">
<center>
    <img src="/images/bounceResult.gif" alt="Bounce" width="200"/>
    <img src="/images/bounceWall.gif" alt="Wall Bounce" width="600"/>
</center>
</div>

Here one can see that by finetuning the color bounds with `range2.py` the tracking algorithm is able to differentiate between the red paddle and orange ping pong ball. Furthermore, the tracking algorithm is also able to pick up on the ball again after it has left the frame once as shown in the second gif which is integral to this project.

## 3) Applying Delaunay Effect to Tracking using Bowyer-Watson algorithm for visual effects:
    -> Run ball_tracking_delaunay.py to see tracking with the effect included!
<div className="justify-content-between items-center">
<center>
    <img src="/images/delaunayBounces.gif" alt="Delaunay Bounce" width="200"/>
    <img src="/images/delaunayWall.gif" alt="Delaunay Wall Bounce" width="600"/>
</center>
</div>
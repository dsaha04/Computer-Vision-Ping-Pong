import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import time

boundingBOX = ()
cap = cv2.VideoCapture(0)

tracker = cv2.TrackerCSRT_create()
success, img = cap.read()
bbox, labels, conf = cv.detect_common_objects(img)

# output_image = draw_bbox(img, bbox, labels, conf)
# plt.imshow(output_image)
# plt.show()

try:
    i = tuple(labels).index("sports ball")
    newBBOX = (bbox[i][0], bbox[i][1], bbox[i][2] - bbox[i][0], bbox[i][3] - bbox[i][1])
    boundingBOX = newBBOX
except:
    print("billy")
    bbox = cv2.selectROI("Tracking", img, False)
    boundingBOX = bbox

print(labels)

tracker.init(img, boundingBOX)


def drawbox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


while True:
    # Capture the video frame
    # by frame
    timer = cv2.getTickCount()
    success, img = cap.read()

    success2, bbox = tracker.update(img)
    print(success2)
    if success2:
        drawbox(img, bbox)
    else:
        cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        time.sleep(5.0)
        bbox = cv2.selectROI("Tracking", img, False)
        tracker.init(img, bbox)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(img, 'Ball', (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()

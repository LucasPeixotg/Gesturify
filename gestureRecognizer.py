import cv2
import time
import mediapipe as mp

model_path = 'gesture_recognizer.task'


class GestureRecognizer:
    def __init__(self, debug=False):
        self.current_gesture = 'None'
        self.hand_landmarks = []
        self.fps = 0
        self.__debug=debug
        
        BaseOptions = mp.tasks.BaseOptions
        GestureRecognizer = mp.tasks.vision.GestureRecognizer
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode
    
        options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.__result_callback
        )
    
        self.mp_recognizer = GestureRecognizer.create_from_options(options)
        self.current_gesture = 'None'
        
    def __result_callback(self, result, output_image: mp.Image, timestamp_ms: int):
        if result.gestures:
            self.current_gesture = result.gestures[0][0].category_name
            self.hand_landmarks = result.hand_landmarks[0]
        else:
            self.current_gesture = 'None'
        
    def process(self, img, timestamp_ms: int, draw=False):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
        self.mp_recognizer.recognize_async(mp_image, timestamp_ms=timestamp_ms)
        
    def start(self, camera=0):
        cap = cv2.VideoCapture(camera)

        # time necessary for FPS
        ptime = 0
        ctime = 0
        
        initial_time = time.time() * 1000
        while True:
            success, img = cap.read()

            # FPS
            ctime = time.time()
            self.fps = 1/(ctime-ptime)
            ptime = ctime
                
            # detects gesture
            timestamp = int(ctime * 1000 - initial_time)
            self.process(img, timestamp)
            
            # draw image for debug
            if self.__debug:              
                if self.current_gesture:  
                    cv2.putText(img, self.current_gesture, (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 1)

                    # draw hand landmarks
                    for _, lm in enumerate(self.hand_landmarks):
                        h, w, _ = img.shape
                        
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        cv2.circle(img, (cx, cy), 3, (0, 0, 255), -1)
                
                cv2.imshow('Hand Tracker Debugging', img)

                key = cv2.waitKey(1)
                if key == ord('q'):
                    cap.release()
                    break

        cap.release()
        cv2.destroyAllWindows()


def main():    
    recognizer = GestureRecognizer(debug=True)
    recognizer.start()
                

if __name__ == "__main__":
    main()

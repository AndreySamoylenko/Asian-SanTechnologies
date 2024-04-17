from vidgear.gears import CamGear
import cv2

try:

  stream = CamGear(source='rtsp://192.168.0.100:8554/live', stream_mode = True, logging=True).start() #Open stream with CamGear

  while True:
      frame = stream.read()
      if frame is None:
          break

      cv2.imshow("Video Stream", frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
          break


  stream.stop() #Stop stream

except Exception as e:
  print(f"An error occurred: {e}")


cv2.destroyAllWindows()

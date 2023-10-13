import rclpy
from rclpy.node import Node
import cv2
import numpy as np

class WebcamNode(Node):

    def __init__(self):
        super().__init__('webcam_node')
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
        self.cap = cv2.VideoCapture(2)

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.imshow('Webcam Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cap.release()
                cv2.destroyAllWindows()
                self.destroy_node()
                rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = WebcamNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


import rclpy
from rclpy.node import Node
import gi
import threading
gi.require_version('Gst', '1.0')
from gi.repository import Gst

class CSICameraNode(Node):

    def __init__(self):
        super().__init__('csi_camera_node')
        Gst.init(None)

        self.pipeline = Gst.parse_launch("nvarguscamerasrc sensor-id=0 ! "
                                         "video/x-raw(memory:NVMM),width=1280, height=720, framerate=30/1, format=NV12 ! "
                                         "nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! nveglglessink")

        self.pipeline.set_state(Gst.State.PLAYING)
        self.get_logger().info("CSI Camera Node is running...")

        # Schedule a function to stop the pipeline after 10 seconds
        threading.Timer(10.0, self.shutdown_pipeline).start()

    def shutdown_pipeline(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.get_logger().info("CSI Camera Node is shutting down...")
        rclpy.shutdown()

def spin(node):
    rclpy.spin(node)

def main(args=None):
    rclpy.init(args=args)
    node = CSICameraNode()

    try:
        thread = threading.Thread(target=spin, args=(node,))
        thread.start()
        thread.join()
    except KeyboardInterrupt:
        pass

    node.destroy_node()

if __name__ == '__main__':
    main()



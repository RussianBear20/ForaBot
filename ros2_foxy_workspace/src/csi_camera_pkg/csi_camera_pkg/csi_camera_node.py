import rclpy
from rclpy.node import Node
import gi
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

    def __del__(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.get_logger().info("CSI Camera Node is shutting down...")

def main(args=None):
    rclpy.init(args=args)
    node = CSICameraNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



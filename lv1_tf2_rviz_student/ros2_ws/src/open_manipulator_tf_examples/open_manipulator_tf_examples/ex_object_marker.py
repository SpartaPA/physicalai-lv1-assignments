"""TF2 listener로 물체 자세를 조회해 RViz2 Marker로 발행하는 예제."""

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from visualization_msgs.msg import Marker

from .frame_utils import clean_frame_id


class ObjectMarker(Node):
    def __init__(self) -> None:
        super().__init__('object_marker')
        self.declare_parameter('fixed_frame', 'world')
        self.declare_parameter('source_frame', 'detected_object')
        self.declare_parameter('marker_topic', '/detected_object_marker')

        self.fixed_frame = clean_frame_id(self.get_parameter('fixed_frame').value)
        self.source_frame = clean_frame_id(self.get_parameter('source_frame').value)
        marker_topic = self.get_parameter('marker_topic').value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.publisher = self.create_publisher(Marker, marker_topic, 10)
        self.last_warning_ns = 0
        self.timer = self.create_timer(0.05, self.publish_marker)

    def publish_marker(self) -> None:
        try:
            # Time()은 TF buffer가 가진 가장 최신의 공통 시각을 요청합니다.
            transform = self.tf_buffer.lookup_transform(
                self.fixed_frame,
                self.source_frame,
                Time(),
            )
        except TransformException as error:
            now_ns = self.get_clock().now().nanoseconds
            if now_ns - self.last_warning_ns >= 2_000_000_000:
                self.get_logger().warning(
                    f'cannot transform {self.source_frame} -> {self.fixed_frame}: {error}'
                )
                self.last_warning_ns = now_ns
            return

        marker = Marker()
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.header.frame_id = self.fixed_frame
        marker.ns = 'detected_object'
        marker.id = 0
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        marker.pose.position.x = transform.transform.translation.x
        marker.pose.position.y = transform.transform.translation.y
        marker.pose.position.z = transform.transform.translation.z
        marker.pose.orientation = transform.transform.rotation
        marker.scale.x = 0.060
        marker.scale.y = 0.035
        marker.scale.z = 0.025
        marker.color.r = 0.95
        marker.color.g = 0.25
        marker.color.b = 0.10
        marker.color.a = 1.0
        self.publisher.publish(marker)

        # TODO(student): 특정 timestamp 조회를 추가하고 extrapolation 오류와 차이를 비교하세요.


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ObjectMarker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()

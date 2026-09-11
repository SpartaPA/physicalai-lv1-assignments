"""camera_link -> detected_object 동적 변환 예제."""

import math

from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from tf2_ros.transform_broadcaster import TransformBroadcaster

from .frame_utils import quaternion_from_euler, validate_frame_pair


class DetectedObjectBroadcaster(Node):
    def __init__(self) -> None:
        super().__init__('detected_object_broadcaster')
        self.declare_parameter('parent_frame', 'camera_link')
        self.declare_parameter('child_frame', 'detected_object')
        self.declare_parameter('base_xyz', [0.180, 0.000, 0.050])
        self.declare_parameter('amplitude', 0.030)
        self.declare_parameter('frequency', 0.20)
        self.declare_parameter('publish_rate', 20.0)

        self.parent_frame, self.child_frame = validate_frame_pair(
            self.get_parameter('parent_frame').value,
            self.get_parameter('child_frame').value,
        )
        self.base_xyz = [float(value) for value in self.get_parameter('base_xyz').value]
        if len(self.base_xyz) != 3:
            raise ValueError('base_xyz must contain three values')
        self.amplitude = float(self.get_parameter('amplitude').value)
        self.frequency = float(self.get_parameter('frequency').value)
        publish_rate = float(self.get_parameter('publish_rate').value)
        if publish_rate <= 0.0:
            raise ValueError('publish_rate must be positive')

        self.broadcaster = TransformBroadcaster(self)
        self.start_ns = self.get_clock().now().nanoseconds
        self.timer = self.create_timer(1.0 / publish_rate, self.publish_transform)

    def publish_transform(self) -> None:
        now = self.get_clock().now()
        elapsed = (now.nanoseconds - self.start_ns) * 1e-9
        phase = 2.0 * math.pi * self.frequency * elapsed

        transform = TransformStamped()
        transform.header.stamp = now.to_msg()
        transform.header.frame_id = self.parent_frame
        transform.child_frame_id = self.child_frame
        transform.transform.translation.x = self.base_xyz[0]
        transform.transform.translation.y = self.base_xyz[1] + self.amplitude * math.sin(phase)
        transform.transform.translation.z = self.base_xyz[2]

        # 물체의 움직임이 좌표축으로도 보이도록 z축 자세를 천천히 흔듭니다.
        qx, qy, qz, qw = quaternion_from_euler(0.0, 0.0, 0.25 * math.sin(phase))
        transform.transform.rotation.x = qx
        transform.transform.rotation.y = qy
        transform.transform.rotation.z = qz
        transform.transform.rotation.w = qw
        self.broadcaster.sendTransform(transform)

        # TODO(student): 비교 실험에서는 elapsed 또는 transform.header.stamp를 report.md에 기록하세요.


def main(args=None) -> None:
    rclpy.init(args=args)
    node = DetectedObjectBroadcaster()
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

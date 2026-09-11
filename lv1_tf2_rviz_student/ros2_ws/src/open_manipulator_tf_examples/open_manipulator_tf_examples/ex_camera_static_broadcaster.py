"""link5 -> camera_link 정적 변환 예제.

StaticTransformBroadcaster는 움직이지 않는 센서 장착 위치처럼 한 번만 알려도 되는
변환에 사용합니다. ROS 2는 이 변환을 transient-local QoS의 /tf_static에 보관하므로
나중에 시작한 listener도 받을 수 있습니다.
"""

from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster

from .frame_utils import quaternion_from_euler, validate_frame_pair


class CameraStaticBroadcaster(Node):
    def __init__(self) -> None:
        super().__init__('camera_static_broadcaster')
        self.declare_parameter('parent_frame', 'link5')
        self.declare_parameter('child_frame', 'camera_link')
        self.declare_parameter('xyz', [0.060, 0.000, 0.040])
        self.declare_parameter('rpy', [0.0, 0.523599, 0.0])

        parent, child = validate_frame_pair(
            self.get_parameter('parent_frame').value,
            self.get_parameter('child_frame').value,
        )
        xyz = [float(value) for value in self.get_parameter('xyz').value]
        rpy = [float(value) for value in self.get_parameter('rpy').value]
        if len(xyz) != 3 or len(rpy) != 3:
            raise ValueError('xyz and rpy parameters must each contain three values')

        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = parent
        transform.child_frame_id = child
        transform.transform.translation.x = xyz[0]
        transform.transform.translation.y = xyz[1]
        transform.transform.translation.z = xyz[2]

        qx, qy, qz, qw = quaternion_from_euler(*rpy)
        transform.transform.rotation.x = qx
        transform.transform.rotation.y = qy
        transform.transform.rotation.z = qz
        transform.transform.rotation.w = qw

        self.broadcaster = StaticTransformBroadcaster(self)
        self.broadcaster.sendTransform(transform)
        self.get_logger().info(
            f'published static transform {parent} -> {child}: xyz={xyz}, rpy={rpy}'
        )

        # TODO(student): camera_link를 없는 parent에 연결해 lookup 실패를 재현한 뒤 복구하세요.


def main(args=None) -> None:
    rclpy.init(args=args)
    node = CameraStaticBroadcaster()
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

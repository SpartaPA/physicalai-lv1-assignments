"""OpenManipulator-X URDF, TF2 예제 노드, RViz2를 한 번에 실행한다."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    package_share = FindPackageShare('open_manipulator_tf_examples')
    urdf_file = PathJoinSubstitution(
        [package_share, 'urdf', 'open_manipulator_x_lab.urdf.xacro']
    )
    params_file = PathJoinSubstitution([package_share, 'config', 'frames.yaml'])
    rviz_file = PathJoinSubstitution(
        [package_share, 'rviz', 'open_manipulator_tf_lab.rviz']
    )
    robot_description = Command([FindExecutable(name='xacro'), ' ', urdf_file])

    use_gui = LaunchConfiguration('use_gui')
    use_rviz = LaunchConfiguration('use_rviz')
    object_frequency = LaunchConfiguration('object_frequency')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_gui',
            default_value='true',
            description='joint_state_publisher_gui를 실행할지 여부',
        ),
        DeclareLaunchArgument(
            'use_rviz',
            default_value='true',
            description='RViz2를 실행할지 여부',
        ),
        DeclareLaunchArgument(
            'object_frequency',
            default_value='0.20',
            description='검출 물체의 사인 운동 주파수. 직접 계산 비교 시 0.0으로 고정',
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen',
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            condition=IfCondition(use_gui),
            output='screen',
        ),
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            condition=UnlessCondition(use_gui),
            parameters=[{
                'zeros.joint1': 0.30,
                'zeros.joint2': -0.40,
                'zeros.joint3': 0.20,
                'zeros.joint4': 0.50,
                'zeros.gripper_left_joint': 0.0,
            }],
            output='screen',
        ),
        Node(
            package='open_manipulator_tf_examples',
            executable='ex_camera_static_broadcaster',
            name='camera_static_broadcaster',
            parameters=[params_file],
            output='screen',
        ),
        Node(
            package='open_manipulator_tf_examples',
            executable='ex_detected_object_broadcaster',
            name='detected_object_broadcaster',
            parameters=[params_file, {'frequency': ParameterValue(object_frequency, value_type=float)}],
            output='screen',
        ),
        Node(
            package='open_manipulator_tf_examples',
            executable='ex_object_marker',
            name='object_marker',
            parameters=[params_file],
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_file],
            condition=IfCondition(use_rviz),
            output='screen',
        ),
        # TODO(student): 학생 패키지에서는 package와 executable 이름에서 ex_를 제거하세요.
    ])

# OpenManipulator-X TF2·RViz2 추가 문제 학생용 템플릿

`추가문제_OpenManipulator-X_TF2_RViz2.md`를 풀 때 참고하는 ROS 2 Humble 예제입니다. 공식 ROBOTIS URDF/Xacro를 불러오고, 그 트리에 카메라와 검출 물체 프레임을 TF2로 추가해 RViz2에서 확인합니다.

> 이 폴더의 `open_manipulator_tf_examples`는 참고용 완성 예제입니다. 제출할 때는 패키지 이름을 `open_manipulator_tf`로 바꾸고, 코드의 `TODO` 실험과 `report_template.md`의 빈칸을 직접 채우세요. 예제 코드만 복사한 제출물에는 비교·관찰·진단 점수가 없습니다.

## 제공되는 것과 직접 할 것

| 제공되는 것 | 직접 해야 하는 것 |
|---|---|
| 공식 OpenManipulator-X macro를 불러오는 wrapper Xacro | `joint1`~`joint4`의 parent·child·axis 분석 |
| 정적 카메라 TF와 동적 물체 TF broadcaster 예제 | 학생 패키지로 옮기고 고정 이름·수치로 재구현 |
| TF2 listener가 Marker를 발행하는 예제 | 프레임 누락·시간 오류를 재현하고 예외 처리 설명 |
| 모든 노드와 RViz2를 띄우는 launch·RViz 설정 | 노드·토픽·TF 트리 검증 및 캡처 |
| 쿼터니언 유틸리티와 pytest | URDF 기반 직접 행렬 합성 대 TF2 결과 비교 테스트 |

## 폴더 구성

```text
lv1_tf2_rviz_student/
├── README.md
├── report_template.md
├── open_manipulator_humble.repos
└── ros2_ws/src/open_manipulator_tf_examples/
    ├── package.xml, setup.py, setup.cfg
    ├── resource/open_manipulator_tf_examples
    ├── open_manipulator_tf_examples/
    │   ├── frame_utils.py
    │   ├── ex_camera_static_broadcaster.py
    │   ├── ex_detected_object_broadcaster.py
    │   └── ex_object_marker.py
    ├── launch/open_manipulator_tf_lab.launch.py
    ├── config/frames.yaml
    ├── urdf/open_manipulator_x_lab.urdf.xacro
    ├── rviz/open_manipulator_tf_lab.rviz
    └── test/test_frame_utils.py
```

## 1. 설치

Ubuntu 22.04와 ROS 2 Humble Desktop을 기준으로 합니다.

```bash
sudo apt update
sudo apt install -y \
  ros-humble-open-manipulator-x-description \
  ros-humble-joint-state-publisher-gui \
  ros-humble-tf2-tools \
  liburdfdom-tools
```

배포 패키지를 설치할 수 없다면 공식 소스를 가져옵니다. `.repos` 파일은 확인한 Humble 커밋으로 고정되어 있습니다.

```bash
sudo apt install -y python3-vcstool
cd ros2_ws
vcs import src < ../open_manipulator_humble.repos
```

## 2. 빌드와 실행

```bash
cd ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install --packages-up-to open_manipulator_tf_examples
source install/setup.bash
ros2 launch open_manipulator_tf_examples open_manipulator_tf_lab.launch.py
```

apt로 description 패키지를 설치한 경우에는 학생 예제 패키지만 빌드되고, 소스로 가져온 경우에는 `--packages-up-to`가 description 패키지까지 필요한 순서로 빌드합니다.

GUI가 없는 환경에서는 다음처럼 RViz2와 슬라이더를 끄고 TF 노드만 확인할 수 있습니다.

```bash
ros2 launch open_manipulator_tf_examples open_manipulator_tf_lab.launch.py \
  use_gui:=false use_rviz:=false
```

직접 행렬 합성과 TF2 결과를 비교할 때는 headless joint publisher의 고정 관절값을 사용하고 물체 운동을 멈춥니다. 이 모드의 관절값은 `joint1=0.30`, `joint2=-0.40`, `joint3=0.20`, `joint4=0.50` rad입니다.

```bash
ros2 launch open_manipulator_tf_examples open_manipulator_tf_lab.launch.py \
  use_gui:=false object_frequency:=0.0
```

## 3. 확인 명령

```bash
ros2 node list
ros2 topic list
ros2 topic info -v /tf
ros2 topic info -v /tf_static
ros2 run tf2_ros tf2_echo link5 camera_link
ros2 run tf2_ros tf2_echo world detected_object
ros2 run tf2_tools view_frames
ros2 topic echo /detected_object_marker --once
```

Xacro와 URDF만 먼저 확인하려면 다음 명령을 사용합니다.

```bash
xacro install/open_manipulator_tf_examples/share/open_manipulator_tf_examples/urdf/open_manipulator_x_lab.urdf.xacro > /tmp/open_manipulator_x_lab.urdf
check_urdf /tmp/open_manipulator_x_lab.urdf
```

## 4. 파일별 읽는 순서

1. `urdf/open_manipulator_x_lab.urdf.xacro` — 공식 macro를 wrapper에서 불러오는 법
2. `launch/open_manipulator_tf_lab.launch.py` — URDF를 `robot_description`으로 전달하고 여러 노드를 묶는 법
3. `ex_camera_static_broadcaster.py` — 움직이지 않는 센서 프레임을 `/tf_static`에 한 번 발행하는 법
4. `ex_detected_object_broadcaster.py` — timestamp가 있는 동적 변환을 `/tf`에 주기적으로 발행하는 법
5. `ex_object_marker.py` — TF2 buffer에서 `world ← detected_object`를 조회하고 Marker로 바꾸는 법
6. `rviz/open_manipulator_tf_lab.rviz` — RobotModel·TF·Marker display의 고정 설정

## 5. 학생 패키지로 옮길 때

- 폴더와 패키지 이름: `open_manipulator_tf_examples` → `open_manipulator_tf`
- 실행 파일 이름에서 `ex_` 제거
- `setup.py`, `setup.cfg`, `package.xml`, resource marker, Python import 경로를 모두 함께 변경
- 고정 프레임·토픽·수치는 과제 지시문의 표를 유지
- `report_template.md`를 제출 폴더의 `report.md`로 복사해 실행 결과와 설명 작성

## 자주 나는 오류

| 증상 | 조치 |
|---|---|
| `Package 'open_manipulator_x_description' not found` | apt 설치 또는 `vcs import` 후 description 패키지를 빌드하고 새 터미널에서 source |
| mesh가 하얗거나 RobotModel이 비어 있음 | 공식 description 패키지의 `meshes/`가 install에 포함됐는지 확인 |
| `No transform from ... to world` | `/joint_states`, `robot_state_publisher`, 두 broadcaster의 frame 이름 확인 |
| Marker는 발행되는데 보이지 않음 | RViz2 Fixed Frame=`world`, Marker alpha·scale, 토픽 이름 확인 |
| joint slider가 뜨지 않음 | `ros-humble-joint-state-publisher-gui` 설치와 `use_gui:=true` 확인 |

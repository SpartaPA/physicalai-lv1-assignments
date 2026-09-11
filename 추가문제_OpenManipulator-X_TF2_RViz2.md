# 추가 문제 — OpenManipulator-X URDF 기반 TF2와 RViz2 시각화

> 연계 범위: 모듈 ② 문제 10의 TF 기초 + 모듈 ③ 문제 5·6의 동차변환·좌표 체인  
> 권장 소요: 6~8시간 · 독립 추가 과제 1개 (기존 Lv.1 공식 점수와 별도 운영)

## 과제 소개

모듈 ③에서는 `base → link → camera` 변환을 4×4 행렬로 직접 합성했습니다. 실제 ROS 2 로봇에서는 각 노드가 프레임 관계를 TF2에 발행하고, 필요한 노드가 원하는 시각의 변환을 조회합니다. 이번 추가 문제에서는 ROBOTIS의 공식 OpenManipulator-X URDF를 `robot_state_publisher`로 게시하고, 카메라와 검출 물체 프레임을 TF2로 연결한 뒤 RViz2에서 로봇 모델·좌표축·물체 마커를 함께 시각화합니다.

실물 로봇은 필요하지 않습니다. `joint_state_publisher_gui`의 슬라이더로 관절 상태를 바꾸며 TF 트리가 갱신되는 것을 관찰합니다.

## 과제 목표

- URDF/Xacro의 link·joint 트리와 `robot_state_publisher`의 역할을 설명할 수 있어요.
- `StaticTransformBroadcaster`와 `TransformBroadcaster`를 구분해 정적·동적 프레임을 발행할 수 있어요.
- `Buffer`와 `TransformListener`로 두 프레임 사이의 변환을 조회하고 예외를 처리할 수 있어요.
- OpenManipulator-X의 RobotModel, TF 트리, 검출 물체 Marker를 RViz2에서 동시에 확인할 수 있어요.
- 같은 좌표 체인을 직접 행렬로 합성한 결과와 TF2 조회 결과를 수치로 비교할 수 있어요.

## 사용 환경과 공식 모델

- Ubuntu 22.04 LTS + ROS 2 Humble Hawksbill
- Python 3.10 이상, `rclpy`, `tf2_ros`, `geometry_msgs`, `visualization_msgs`
- `robot_state_publisher`, `joint_state_publisher_gui`, `rviz2`, `xacro`, `tf2_tools`
- 공식 모델: ROBOTIS [`open_manipulator`](https://github.com/ROBOTIS-GIT/open_manipulator) 저장소 Humble 브랜치의 `open_manipulator_x_description`
- URDF/Xacro: `open_manipulator_x_description/urdf/open_manipulator_x.urdf.xacro`

템플릿은 공식 모델의 macro와 mesh를 그대로 참조합니다. ROBOTIS 파일을 수정하거나 복제하지 말고, 학생 패키지의 wrapper Xacro에서 불러와 사용하세요.

## 고정 규격

| 항목 | 값 |
|---|---|
| 학생 패키지 이름 | `open_manipulator_tf` (`ament_python`) |
| RViz2 Fixed Frame | `world` |
| URDF 기본 체인 | `world → link1 → link2 → link3 → link4 → link5 → end_effector_link` |
| 추가 정적 프레임 | `link5 → camera_link` |
| 카메라 위치·자세 | xyz = `(0.060, 0.000, 0.040)` m, rpy = `(0, 0.523599, 0)` rad |
| 추가 동적 프레임 | `camera_link → detected_object` |
| 물체 기준 위치 | xyz = `(0.180, 0.000, 0.050)` m |
| 물체 움직임 | y축 진폭 `0.030` m, 주파수 `0.20` Hz의 사인 운동 |
| Marker 토픽 | `/detected_object_marker` (`visualization_msgs/msg/Marker`) |
| 허용 오차 | 직접 합성값과 TF2 결과의 위치 오차 `1e-6 m` 이하 |

이름과 수치는 채점 스크립트와 캡처 기준으로 사용하므로 바꾸지 않습니다.

## 최종 결과물 제출 형식

```text
physicalai-lv1-<이름>/lv1_tf2_rviz/
├── report.md
├── ros2_ws/src/
│   └── open_manipulator_tf/
│       ├── package.xml
│       ├── setup.py
│       ├── setup.cfg
│       ├── resource/open_manipulator_tf
│       ├── open_manipulator_tf/
│       │   ├── __init__.py
│       │   ├── frame_utils.py
│       │   ├── camera_static_broadcaster.py
│       │   ├── detected_object_broadcaster.py
│       │   └── object_marker.py
│       ├── launch/open_manipulator_tf.launch.py
│       ├── config/frames.yaml
│       ├── urdf/open_manipulator_x_lab.urdf.xacro
│       ├── rviz/open_manipulator_tf.rviz
│       └── test/
└── screenshots/
    ├── 01_robot_model.png
    ├── 02_tf_tree.png
    ├── 03_joint_changed.png
    └── 04_marker.png
```

시작점은 `lv1_tf2_rviz_student/`입니다. 그 안의 `open_manipulator_tf_examples`는 동작 원리를 보여 주는 참고 패키지입니다. 학생은 패키지 이름을 `open_manipulator_tf`로 바꾸고, 각 파일의 `TODO` 항목과 보고서의 빈칸을 직접 완성합니다.

---

## 1. OpenManipulator-X URDF 구조 확인

### 구현 내용

- 공식 `open_manipulator_x_description` 패키지를 설치하거나 템플릿의 `.repos` 파일로 가져오세요.
- `xacro`로 wrapper 파일을 URDF로 펼친 뒤 `check_urdf`를 통과시키세요.
- URDF에서 `joint1`~`joint4`의 parent link, child link, 회전축을 표로 정리하세요.
- `world_fixed`와 `end_effector_joint`가 고정 관절인 이유를 설명하세요.
- `ros2 run tf2_tools view_frames`로 실행 중인 프레임 트리를 그림으로 저장하세요.

### 결과물

- URDF 검사 출력, link·joint 표, 트리 이미지 또는 PDF를 `report.md`의 문제 1 절에 넣습니다.

### 답안 템플릿

1. **`check_urdf` 결과**: `___`
2. **관절 표**: joint / parent / child / axis (4행)
3. **고정 관절의 역할**: `___`
4. **예상한 루트와 말단 프레임**: `___` / `___`

## 2. robot_state_publisher와 관절 상태 시각화

### 구현 내용

- wrapper Xacro를 `robot_description` 파라미터로 전달해 `robot_state_publisher`를 실행하세요.
- `joint_state_publisher_gui`와 RViz2를 같은 launch 파일에서 기동하세요.
- RViz2에 RobotModel과 TF display를 추가하고 Fixed Frame을 `world`로 설정하세요.
- 슬라이더로 `joint1`과 `joint2`를 움직여 로봇 모양과 `link5`, `end_effector_link` 축이 함께 바뀌는지 확인하세요.
- `/joint_states`, `/tf`, `/tf_static`의 발행자·주기·용도를 비교하세요.

### 결과물

- 기본 자세와 관절 변경 자세의 RViz2 캡처, `ros2 topic info -v` 결과를 제출합니다.

### 답안 템플릿

1. **실행 중인 노드 목록**: `___`
2. **기본 자세 캡처**: `screenshots/01_robot_model.png`
3. **관절 변경 캡처**: `screenshots/03_joint_changed.png`
4. **`/tf`와 `/tf_static` 차이**: `___`
5. **JointState가 RobotModel에 반영되는 흐름**: `___`

## 3. 카메라 정적 TF와 물체 동적 TF 발행

### 구현 내용

- `StaticTransformBroadcaster`로 `link5 → camera_link` 변환을 한 번 발행하는 노드를 작성하세요.
- `TransformBroadcaster`로 `camera_link → detected_object` 변환을 20 Hz로 발행하세요. 물체는 고정 규격의 사인 운동을 해야 합니다.
- Euler 각을 단위 쿼터니언으로 바꾸고, 쿼터니언의 norm이 1인지 테스트하세요.
- `ros2 run tf2_ros tf2_echo link5 camera_link`와 `ros2 run tf2_ros tf2_echo camera_link detected_object`로 값을 확인하세요.
- `view_frames` 결과에서 두 프레임이 기대한 parent-child 관계로 연결되는지 확인하세요.

### 결과물

- 두 broadcaster 소스, 파라미터 YAML, `tf2_echo` 출력, TF 트리 캡처를 제출합니다.

### 답안 템플릿

1. **정적 TF 발행 값**: translation `___` / quaternion `___`
2. **동적 TF 최소·최대 y 값**: `___` / `___`
3. **`tf2_echo` 출력**: `___`
4. **TF 트리 캡처**: `screenshots/02_tf_tree.png`
5. **정적·동적 broadcaster를 구분한 이유**: `___`

## 4. TF2 listener와 RViz2 Marker

### 구현 내용

- `tf2_ros.Buffer`와 `TransformListener`로 `world ← detected_object` 변환을 조회하세요.
- 조회한 위치와 자세로 방향을 구분할 수 있는 직육면체 Marker를 `/detected_object_marker`에 발행하세요. Marker의 `header.frame_id`는 `world`여야 합니다.
- 아직 프레임이 없거나 TF 트리가 끊긴 경우 노드가 종료되지 않고 경고를 남기도록 `TransformException`을 처리하세요.
- RViz2에 Marker display를 추가하고 로봇 모델, 전체 TF 축, 물체 마커가 동시에 보이게 하세요.
- 관절 슬라이더를 움직였을 때 마커가 로봇 팔의 링크 체인을 따라 함께 움직이는지 관찰하세요.

### 결과물

- listener·Marker 노드, RViz 설정 파일, 최종 RViz2 캡처를 제출합니다.

### 답안 템플릿

1. **조회한 변환 방향**: target `___` / source `___`
2. **Marker의 frame_id와 토픽**: `___` / `___`
3. **최종 RViz2 캡처**: `screenshots/04_marker.png`
4. **관절 변경 시 물체가 움직이는 이유**: `___`
5. **프레임 누락 시 경고 로그**: `___`

## 5. 직접 행렬 합성과 TF2 결과 비교

### 구현 내용

- `use_gui:=false object_frequency:=0.0`으로 launch를 다시 실행하세요. 템플릿의 headless joint publisher는 `joint1=0.30`, `joint2=-0.40`, `joint3=0.20`, `joint4=0.50` rad를 발행하고, 물체는 phase 0 위치에 고정됩니다.
- URDF의 각 joint origin과 현재 joint angle, 추가한 두 변환을 4×4 동차변환으로 만들고 `T_world_detected_object`를 직접 합성하세요.
- 같은 시점의 `lookup_transform('world', 'detected_object', ...)` 결과를 행렬로 바꾸어 직접 합성값과 비교하세요.
- 위치 오차와 회전 오차를 계산하세요. 위치 오차는 `1e-6 m` 이하여야 합니다.
- `camera_link` 이름을 일부러 잘못 바꿔 lookup 실패를 재현하고, 에러 종류·진단 순서·수정 내용을 기록한 뒤 원래대로 되돌리세요.

### 결과물

- 비교 코드와 수치, 실패·복구 로그, 테스트 결과를 `report.md`에 정리합니다.

### 답안 템플릿

1. **비교 모드 관절값과 물체 주파수**: `___` / `___`
2. **직접 합성한 위치**: `___`
3. **TF2로 조회한 위치**: `___`
4. **위치 오차**: `___` m / **회전 오차**: `___` 도
5. **프레임 이름 오류의 예외와 원인**: `___`
6. **진단 순서**: `ros2 node list` → `___` → `___` → `___`

---

## 채점 루브릭

| 수준 | 기준 |
|---|---|
| 1점 | 제출하지 않았거나 OpenManipulator-X·TF2와 무관한 결과물 |
| 2점 | URDF 또는 RViz2를 일부 실행했으나 TF 트리가 완성되지 않음 |
| 3점 | RobotModel과 추가 프레임 일부가 보이나 broadcaster·listener·Marker 중 하나 이상이 불완전함 |
| 4점 | 지시한 URDF, 정적·동적 TF, listener, Marker, launch, RViz2 캡처와 기본 검증을 모두 충족함 |
| 5점 | 4점 기준에 더해 직접 행렬 합성 대조, 시간·프레임 오류 재현과 진단, 관절 변경에 따른 관찰을 근거와 함께 설명함 |

## 자주 나는 오류

| 증상 | 확인할 것 |
|---|---|
| RobotModel이 보이지 않음 | `open_manipulator_x_description` 설치 여부, `/robot_description`, mesh 경로, RViz2 Fixed Frame |
| `world` 프레임이 없다고 나옴 | wrapper Xacro의 `world_fixed`, `robot_state_publisher`, `/joint_states` 발행 여부 |
| `camera_link`가 TF에 없음 | static broadcaster 실행 여부, `header.frame_id`와 `child_frame_id` 오탈자 |
| Marker가 보이지 않음 | Marker 토픽, `header.frame_id`, scale·alpha 값, `world ← detected_object` lookup 성공 여부 |
| `Lookup would require extrapolation` | 조회 timestamp와 TF buffer의 시간 범위가 맞는지 확인하고, 최신 변환 조회와 특정 시각 조회의 차이를 설명 |
| 관절을 움직여도 링크가 안 움직임 | `/joint_states` 토픽과 joint 이름이 URDF의 `joint1`~`joint4`와 일치하는지 확인 |

## 제출 전 체크리스트

- [ ] `colcon build --symlink-install --packages-up-to open_manipulator_tf` 통과
- [ ] launch 한 번으로 robot_state_publisher, joint_state_publisher_gui, 세 TF 예제 노드, RViz2 기동
- [ ] RViz2 Fixed Frame이 `world`
- [ ] RobotModel, TF, `/detected_object_marker`를 동시에 확인
- [ ] `/tf`와 `/tf_static` 차이를 실행 결과로 설명
- [ ] 직접 합성과 TF2 조회의 위치 오차가 `1e-6 m` 이하
- [ ] 프레임 누락 예외를 재현하고 복구
- [ ] `build/`, `install/`, `log/`를 커밋하지 않음

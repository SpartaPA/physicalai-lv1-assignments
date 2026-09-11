# OpenManipulator-X TF2와 RViz2 시각화 보고서

## 실행 환경

- Ubuntu 버전: `___`
- ROS 배포판: `___`
- `open_manipulator_x_description` 버전 또는 커밋: `___`
- 실행 환경: 네이티브 Ubuntu / VM / WSL2 / 기타 `___`

## 문제 1 OpenManipulator-X URDF 구조 확인

### URDF 검사 출력

```text
___
```

### 관절 구조

| joint | parent | child | axis |
|---|---|---|---|
| joint1 | `___` | `___` | `___` |
| joint2 | `___` | `___` | `___` |
| joint3 | `___` | `___` | `___` |
| joint4 | `___` | `___` | `___` |

- `world_fixed`와 `end_effector_joint`가 고정 관절인 이유: `___`
- 예상한 루트 프레임 / 말단 프레임: `___` / `___`
- URDF 또는 TF 트리 이미지: `___`

## 문제 2 robot_state_publisher와 관절 상태 시각화

### 노드와 토픽 확인

```text
ros2 node list
___

ros2 topic info -v /tf
___

ros2 topic info -v /tf_static
___
```

- 기본 자세 캡처: `screenshots/01_robot_model.png`
- 관절 변경 캡처: `screenshots/03_joint_changed.png`
- `/tf`와 `/tf_static` 차이: `___`
- `/joint_states`가 RobotModel에 반영되는 흐름: `___`

## 문제 3 카메라 정적 TF와 물체 동적 TF 발행

- `link5 → camera_link` translation: `___`
- `link5 → camera_link` quaternion: `___`
- `detected_object` y 최소·최대: `___` / `___`
- 정적·동적 broadcaster를 구분한 이유: `___`

```text
ros2 run tf2_ros tf2_echo link5 camera_link
___

ros2 run tf2_ros tf2_echo camera_link detected_object
___
```

- TF 트리 캡처: `screenshots/02_tf_tree.png`

## 문제 4 TF2 listener와 RViz2 Marker

- lookup target / source: `___` / `___`
- Marker frame_id / topic: `___` / `___`
- 관절 변경 시 Marker가 움직이는 이유: `___`
- 최종 캡처: `screenshots/04_marker.png`

### 프레임 누락 경고

```text
___
```

예외를 처리한 방법: `___`

## 문제 5 직접 행렬 합성과 TF2 결과 비교

- 관절값: `(0.30, -0.40, 0.20, 0.50)` rad
- 비교 실행 인자: `use_gui:=false object_frequency:=0.0`
- 비교 시 동적 물체 phase: `0`
- 직접 합성 위치: `___`
- TF2 조회 위치: `___`
- 위치 오차: `___` m
- 회전 오차: `___` 도
- 허용 오차 통과 여부: `___`

### 의도적인 프레임 이름 오류와 복구

```text
___
```

- 예외 종류와 원인: `___`
- 진단 순서: `ros2 node list` → `___` → `___` → `___`
- 수정 내용: `___`

## 테스트 결과

```text
pytest -v
___
```

## 최종 체크

- [ ] launch 한 번으로 전체 시스템 기동
- [ ] RobotModel·TF·Marker 동시 표시
- [ ] 고정 이름과 수치 준수
- [ ] 직접 합성 대 TF2 비교 통과
- [ ] 오류 재현 후 원상 복구
- [ ] build/install/log 제외

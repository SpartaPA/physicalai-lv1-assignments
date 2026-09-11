"""ROS에 의존하지 않는 프레임 계산 유틸리티.

학생 과제에서는 이 함수의 테스트를 출발점으로 삼고, URDF의 joint origin과
joint angle을 4x4 행렬로 바꾸는 함수를 추가해 TF2 결과와 비교합니다.
"""

from __future__ import annotations

import math


def quaternion_from_euler(roll: float, pitch: float, yaw: float) -> tuple[float, float, float, float]:
    """고정축 roll-pitch-yaw를 ROS 순서 (x, y, z, w) 쿼터니언으로 변환한다."""
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)

    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    w = cr * cp * cy + sr * sp * sy
    return x, y, z, w


def quaternion_norm(quaternion: tuple[float, float, float, float]) -> float:
    """쿼터니언의 유클리드 norm을 반환한다."""
    return math.sqrt(sum(component * component for component in quaternion))


def clean_frame_id(frame_id: str) -> str:
    """TF2 권장 형식에 맞춰 앞쪽 slash와 공백을 제거한다."""
    cleaned = frame_id.strip().lstrip('/')
    if not cleaned:
        raise ValueError('frame_id must not be empty')
    return cleaned


def validate_frame_pair(parent_frame: str, child_frame: str) -> tuple[str, str]:
    """parent와 child 이름을 정리하고 자기 자신을 잇는 변환을 거부한다."""
    parent = clean_frame_id(parent_frame)
    child = clean_frame_id(child_frame)
    if parent == child:
        raise ValueError('parent_frame and child_frame must be different')
    return parent, child

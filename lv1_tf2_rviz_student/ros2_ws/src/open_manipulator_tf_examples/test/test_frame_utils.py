import math

import pytest

from open_manipulator_tf_examples.frame_utils import (
    clean_frame_id,
    quaternion_from_euler,
    quaternion_norm,
    validate_frame_pair,
)


def test_zero_euler_is_identity_quaternion():
    assert quaternion_from_euler(0.0, 0.0, 0.0) == pytest.approx((0.0, 0.0, 0.0, 1.0))


def test_euler_result_is_unit_quaternion():
    quaternion = quaternion_from_euler(0.2, -0.5, 1.1)
    assert math.isclose(quaternion_norm(quaternion), 1.0, abs_tol=1e-12)


def test_clean_frame_id_removes_leading_slash_and_space():
    assert clean_frame_id('  /camera_link ') == 'camera_link'


def test_invalid_frame_pair_is_rejected():
    with pytest.raises(ValueError):
        validate_frame_pair('link5', '/link5')


# TODO(student): URDF joint origin + joint angle의 직접 행렬 합성과
# TF2 lookup 결과를 비교하는 테스트를 별도 파일에 추가하세요.

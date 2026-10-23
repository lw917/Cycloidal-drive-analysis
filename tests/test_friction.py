import numpy as np
import pytest

from src.friction import estimate_output_performance, frictional_power_loss


def test_frictional_power_loss_scalar_speed():
    loss = frictional_power_loss(np.array([10.0, 20.0]), 0.1, 0.02)
    assert np.isclose(loss, 0.06)


def test_frictional_power_loss_per_contact_speeds():
    loss = frictional_power_loss(np.array([10.0, 20.0]), 0.1, np.array([0.01, 0.02]))
    assert np.isclose(loss, 0.05)


def test_frictional_power_loss_invalid_inputs():
    with pytest.raises(ValueError):
        frictional_power_loss(np.array([-1.0]), 0.1, 0.01)
    with pytest.raises(ValueError):
        frictional_power_loss(np.array([1.0]), -0.1, 0.01)
    with pytest.raises(ValueError):
        frictional_power_loss(np.array([1.0, 2.0]), 0.1, np.array([0.01, 0.02, 0.03]))


def test_output_performance_power_balance():
    result = estimate_output_performance(1.0, 60.0, 30.0, 1.0)
    assert np.isclose(result["input_power_w"], 2 * np.pi)
    assert np.isclose(result["estimated_efficiency"], (2 * np.pi - 1) / (2 * np.pi))
    assert result["estimated_output_torque_nm"] < result["ideal_output_torque_nm"]


def test_loss_must_be_less_than_input_power():
    with pytest.raises(ValueError):
        estimate_output_performance(1.0, 60.0, 30.0, 10.0)

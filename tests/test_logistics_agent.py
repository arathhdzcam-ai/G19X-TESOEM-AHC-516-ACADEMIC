import pytest

from app.agents.logistics_agent import LogisticsAgent


def test_good_delivery_performance():
    result = LogisticsAgent().analyze(
        on_time_delivery_rate=0.98,
        lead_time_days=5,
        delay_days=0,
    )

    assert result["delivery_status"] == "on_time_performance_good"
    assert result["priority"] == "low"
    assert result["on_time_delivery_rate"] == 98


def test_delivery_delay_increases_priority():
    result = LogisticsAgent().analyze(
        on_time_delivery_rate=0.95,
        lead_time_days=5,
        delay_days=2,
    )

    assert result["delivery_status"] == "delayed"
    assert result["priority"] == "medium"


def test_long_delay_has_high_priority():
    result = LogisticsAgent().analyze(
        on_time_delivery_rate=0.95,
        lead_time_days=5,
        delay_days=3,
    )

    assert result["delivery_status"] == "delayed"
    assert result["priority"] == "high"


def test_low_delivery_rate_is_high_priority():
    result = LogisticsAgent().analyze(
        on_time_delivery_rate=0.79,
        lead_time_days=5,
        delay_days=0,
    )

    assert result["delivery_status"] == "delivery_risk"
    assert result["priority"] == "high"


@pytest.mark.parametrize("rate", [-1, 101])
def test_invalid_delivery_rate_is_rejected(rate):
    with pytest.raises(ValueError):
        LogisticsAgent().analyze(
            on_time_delivery_rate=rate,
            lead_time_days=5,
            delay_days=0,
        )


@pytest.mark.parametrize(
    "lead_time,delay",
    [
        (-1, 0),
        (5, -1),
    ],
)
def test_negative_delivery_times_are_rejected(lead_time, delay):
    with pytest.raises(ValueError):
        LogisticsAgent().analyze(
            on_time_delivery_rate=0.95,
            lead_time_days=lead_time,
            delay_days=delay,
        )

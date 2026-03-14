from app.schemas import AthleticMetricsInput
from app.services.scoring import calculate_athletic_score, get_benchmark_for_age


def build_metrics_for_age(age: int, include_optional: bool = True) -> AthleticMetricsInput:
    benchmark = get_benchmark_for_age(age)
    return AthleticMetricsInput(
        standing_height=62.0,
        body_weight=118.0,
        speed_10yd=benchmark.speed_10yd,
        speed_20yd=benchmark.speed_20yd if include_optional else None,
        speed_40yd=benchmark.speed_40yd,
        flying_10yd=benchmark.flying_10yd if include_optional else None,
        vertical_jump=benchmark.vertical_jump,
        broad_jump=benchmark.broad_jump,
        medicine_ball_throw=benchmark.medicine_ball_throw if include_optional else None,
        agility_shuttle=benchmark.agility_shuttle,
        l_drill=benchmark.l_drill if include_optional else None,
        reaction_time=benchmark.reaction_time,
        pullups=int(benchmark.pullups),
        pushups=int(benchmark.pushups),
        mobility_score=7 if include_optional else None,
        landing_control_score=7 if include_optional else None,
        single_leg_balance_left=14.2 if include_optional else None,
        single_leg_balance_right=13.9 if include_optional else None,
        squat_strength_ratio=benchmark.squat_strength_ratio if include_optional else None,
        endurance_300yd=benchmark.endurance_300yd,
        yoyo_endurance=benchmark.yoyo_endurance if include_optional else None,
    )


def test_benchmark_aligned_metrics_score_near_100():
    score = calculate_athletic_score(14, build_metrics_for_age(14))
    assert 99 <= score <= 101


def test_missing_optional_metrics_still_produce_a_stable_score():
    score = calculate_athletic_score(12, build_metrics_for_age(12, include_optional=False))
    assert 99 <= score <= 101


def test_younger_athletes_use_their_own_age_band_benchmarks():
    benchmark = get_benchmark_for_age(9)
    assert benchmark.speed_40yd == 5.85

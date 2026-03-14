def build_athlete_payload():
    return {
        "first_name": "Jordan",
        "last_name": "Smith",
        "date_of_birth": "2011-06-15",
        "age": 14,
        "height": 68,
        "weight": 145,
        "primary_sport": "Football",
        "secondary_sport": "Track",
        "team": "FlightTime Falcons",
        "coach": "Coach Carter",
    }


def build_baseline_payload(athlete_id: str):
    return {
        "athlete_id": athlete_id,
        "baseline_date": "2026-03-13",
        "speed_10yd": 1.78,
        "speed_40yd": 4.95,
        "vertical_jump": 24,
        "broad_jump": 92,
        "agility_shuttle": 4.75,
        "reaction_time": 0.32,
        "pullups": 8,
        "pushups": 25,
        "endurance_300yd": 68,
    }


def test_core_authenticated_athlete_baseline_and_development_flow(client, auth_headers):
    headers = auth_headers()

    athlete_response = client.post("/athletes/create", json=build_athlete_payload(), headers=headers)
    assert athlete_response.status_code == 201, athlete_response.text
    athlete = athlete_response.json()
    athlete_id = athlete["athlete_id"]

    baseline_response = client.post("/baseline/create", json=build_baseline_payload(athlete_id), headers=headers)
    assert baseline_response.status_code == 201, baseline_response.text
    baseline = baseline_response.json()

    assert baseline["athlete_id"] == athlete_id
    assert baseline["standing_height"] == 68
    assert baseline["body_weight"] == 145
    assert baseline["baseline_score"] > 0

    development_response = client.get(f"/athletes/{athlete_id}/development", headers=headers)
    assert development_response.status_code == 200, development_response.text
    development = development_response.json()

    assert development["athlete"]["athlete_id"] == athlete_id
    assert development["baseline_score"] == baseline["baseline_score"]
    assert development["pathway"]["pathway_name"]
    assert development["active_training_plan"]["weekly_sessions_target"] >= 1
    assert development["training_template"]["sessions"]
    assert development["insights"]["next_best_action"]
    assert development["athlete_build"]["overall_rating"] > 0


def test_baseline_can_only_be_recorded_once(client, auth_headers):
    headers = auth_headers()
    athlete_response = client.post("/athletes/create", json=build_athlete_payload(), headers=headers)
    athlete_id = athlete_response.json()["athlete_id"]

    first_response = client.post("/baseline/create", json=build_baseline_payload(athlete_id), headers=headers)
    second_response = client.post("/baseline/create", json=build_baseline_payload(athlete_id), headers=headers)

    assert first_response.status_code == 201, first_response.text
    assert second_response.status_code == 409, second_response.text
    assert second_response.json()["detail"] == "Baseline already exists and cannot be overwritten"

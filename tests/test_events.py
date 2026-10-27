def test_get_event_returns_existing_event(client):
    response = client.get("events/2")
    assert response.status_code == 200
    assert response.json()["event"]["id"] == 2

def test_get_event_not_found_returns_404(client):
    response = client.get("events/909090")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"

def test_get_event_with_invalid_id_type_returns_400(client):
    response = client.get("events/True")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_TYPE"


def test_get_events_returns_all_events_as_dict_value_of_list_of_dicts(client):
    response = client.get("events")
    assert response.status_code == 200
    assert len(response.json()["events"]) == 5

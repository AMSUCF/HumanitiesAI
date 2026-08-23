import responses
from canvas_client import CanvasClient

BASE = "https://webcourses.ucf.edu/api/v1/courses/123"

def client():
    return CanvasClient("https://webcourses.ucf.edu", "tok", "123")

@responses.activate
def test_upsert_module_finds_existing():
    responses.get(f"{BASE}/modules", json=[{"id": 7, "name": "Week One"}])
    responses.put(f"{BASE}/modules/7", json={"id": 7})
    assert client().upsert_module("Week One") == 7

@responses.activate
def test_upsert_module_creates_when_missing():
    responses.get(f"{BASE}/modules", json=[])
    responses.post(f"{BASE}/modules", json={"id": 9, "name": "Week Two"})
    assert client().upsert_module("Week Two") == 9

@responses.activate
def test_upsert_discussion_updates_known_id():
    responses.put(f"{BASE}/discussion_topics/42", json={"id": 42})
    got = client().upsert_discussion("T", "<p>m</p>", 6,
                                     "2026-08-31T03:59:00Z", 5, known_id=42)
    assert got == 42

@responses.activate
def test_upsert_discussion_creates_graded():
    responses.get(f"{BASE}/discussion_topics", json=[])
    rsp = responses.post(f"{BASE}/discussion_topics", json={"id": 43})
    assert client().upsert_discussion("T", "<p>m</p>", 6,
                                      "2026-08-31T03:59:00Z", 5) == 43
    import json as j
    sent = j.loads(rsp.calls[0].request.body)
    assert sent["assignment"]["points_possible"] == 6
    assert sent["assignment"]["assignment_group_id"] == 5
    assert sent["published"] is False

@responses.activate
def test_upsert_assignment_updates_known_id():
    responses.put(f"{BASE}/assignments/42", json={"id": 42})
    got = client().upsert_assignment("Activity Verification", 6,
                                     "2026-08-31T03:59:00Z", 5,
                                     ["online_url", "online_text_entry"],
                                     known_id=42)
    assert got == 42

@responses.activate
def test_upsert_assignment_creates_when_missing():
    responses.get(f"{BASE}/assignments", json=[])
    rsp = responses.post(f"{BASE}/assignments", json={"id": 44})
    assert client().upsert_assignment("Activity Verification", 6,
                                      "2026-08-31T03:59:00Z", 5,
                                      ["online_url", "online_text_entry"]) == 44
    import json as j
    sent = j.loads(rsp.calls[0].request.body)
    assert sent["assignment"]["name"] == "Activity Verification"
    assert sent["assignment"]["points_possible"] == 6
    assert sent["assignment"]["assignment_group_id"] == 5
    assert sent["assignment"]["submission_types"] == ["online_url", "online_text_entry"]
    assert sent["assignment"]["published"] is False


@responses.activate
def test_upsert_module_updates_existing_with_unlock():
    responses.get(f"{BASE}/modules", json=[{"id": 7, "name": "Week One"}])
    rsp = responses.put(f"{BASE}/modules/7", json={"id": 7})
    assert client().upsert_module("Week One", unlock_at="2026-08-24T04:00:00Z") == 7
    import json as j
    sent = j.loads(rsp.calls[0].request.body)
    assert sent["module"]["unlock_at"] == "2026-08-24T04:00:00Z"


@responses.activate
def test_upsert_page_known_url_updates_in_place():
    rsp = responses.put(f"{BASE}/pages/week-one-video-lecture",
                        json={"url": "week-one-video-lecture"})
    got = client().upsert_page("Week One Readings + Lecture", "<p>b</p>",
                               True, known_url="week-one-video-lecture")
    assert got == "week-one-video-lecture"
    import json as j
    sent = j.loads(rsp.calls[0].request.body)
    assert sent["wiki_page"]["title"] == "Week One Readings + Lecture"


@responses.activate
def test_get_page_body_returns_none_on_404():
    responses.get(f"{BASE}/pages/nope", json={"errors": []}, status=404)
    assert client().get_page_body("nope") is None


@responses.activate
def test_add_to_module_repositions_existing_item():
    responses.get(f"{BASE}/modules/7/items",
                  json=[{"id": 1, "type": "Page", "page_url": "lec", "position": 2},
                        {"id": 2, "type": "Page", "page_url": "pg", "position": 1}])
    rsp = responses.put(f"{BASE}/modules/7/items/1", json={"id": 1})
    client().add_to_module(7, "Page", "lec", position=1)
    import json as j
    sent = j.loads(rsp.calls[0].request.body)
    assert sent["module_item"]["position"] == 1


@responses.activate
def test_add_to_module_skips_put_when_position_matches():
    responses.get(f"{BASE}/modules/7/items",
                  json=[{"id": 1, "type": "Page", "page_url": "lec", "position": 1}])
    client().add_to_module(7, "Page", "lec", position=1)
    assert len(responses.calls) == 1  # only the GET


@responses.activate
def test_add_to_module_creates_with_position():
    responses.get(f"{BASE}/modules/7/items", json=[])
    rsp = responses.post(f"{BASE}/modules/7/items", json={"id": 3})
    client().add_to_module(7, "Page", "lec", position=1)
    import json as j
    sent = j.loads(rsp.calls[0].request.body)
    assert sent["module_item"] == {"type": "Page", "page_url": "lec", "position": 1}


@responses.activate
def test_upsert_discussion_sends_availability_window():
    responses.put(f"{BASE}/discussion_topics/42", json={"id": 42})
    client().upsert_discussion("T", "<p>m</p>", 6, "2026-08-31T03:59:00Z", 5,
                               known_id=42, unlock_at="2026-08-24T04:00:00Z",
                               lock_at="2026-09-07T03:59:00Z")
    import json as j
    sent = j.loads(responses.calls[0].request.body)
    assert sent["assignment"]["unlock_at"] == "2026-08-24T04:00:00Z"
    assert sent["assignment"]["lock_at"] == "2026-09-07T03:59:00Z"

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



API = "https://canvas.test"
COURSE = f"{API}/api/v1/courses/42"


def c42():
    return CanvasClient(API, "tok", "42")


@responses.activate
def test_upload_file_three_step(tmp_path):
    f = tmp_path / "moduleone.pptx"; f.write_bytes(b"PK..")
    responses.post(f"{COURSE}/files", json={"upload_url": "https://up.test/x",
                                            "upload_params": {"key": "k"}})
    responses.post("https://up.test/x", status=302,
                   headers={"Location": f"{API}/api/v1/files/7/create_success"})
    responses.get(f"{API}/api/v1/files/7/create_success", json={"id": 7, "updated_at": "T1"})
    out = c42().upload_file(f, "Lecture Slides", "application/x")
    assert out["id"] == 7
    pre = responses.calls[0].request
    assert b'"on_duplicate": "overwrite"' in pre.body and b'"parent_folder_path": "Lecture Slides"' in pre.body
    assert "Authorization" not in responses.calls[1].request.headers   # never send the token to the upload host


@responses.activate
def test_find_or_create_page_never_overwrites():
    responses.get(f"{COURSE}/pages", json=[{"title": "Syllabus", "url": "syllabus"}])
    assert c42().find_or_create_page("Syllabus") == "syllabus"
    assert all(c.request.method == "GET" for c in responses.calls)


@responses.activate
def test_updated_at_none_on_404():
    responses.get(f"{COURSE}/pages/gone", status=404)
    assert c42().updated_at("pages", "gone") is None


TOPIC = {"id": 5, "title": "Exercise Discussion: M1", "message": "<p>hi</p>",
         "assignment": {"due_at": "2027-01-25T04:59:00Z", "points_possible": 10,
                        "lock_at": "2027-01-26T04:59:00Z", "unlock_at": "2027-01-11T05:00:00Z"}}


@responses.activate
def test_updated_at_discussion_falls_back_to_content_hash():
    import hashlib, json
    responses.get(f"{COURSE}/discussion_topics/5", json=TOPIC)
    a = TOPIC["assignment"]
    want = json.dumps({"title": TOPIC["title"], "message": TOPIC["message"],
                       "due_at": a["due_at"], "points_possible": 10,
                       "lock_at": a["lock_at"], "unlock_at": a["unlock_at"]}, sort_keys=True)
    assert c42().updated_at("discussion_topics", 5) == \
        "sha:" + hashlib.sha256(want.encode("utf-8")).hexdigest()


@responses.activate
def test_updated_at_discussion_marker_sees_due_date_and_title_changes():
    moved = {**TOPIC, "assignment": {**TOPIC["assignment"], "due_at": "2027-01-27T04:59:00Z"}}
    renamed = {**TOPIC, "title": "Renamed"}
    for body in (TOPIC, moved, renamed, TOPIC):
        responses.get(f"{COURSE}/discussion_topics/5", json=body)
    markers = [c42().updated_at("discussion_topics", 5) for _ in range(4)]
    assert markers[0] == markers[3]                     # stable for the same topic
    assert len(set(markers[:3])) == 3                   # due date or title change shows


@responses.activate
def test_updated_at_discussion_prefers_updated_at():
    responses.get(f"{COURSE}/discussion_topics/5",
                  json={"id": 5, "message": "m", "updated_at": "T9"})
    assert c42().updated_at("discussion_topics", 5) == "T9"


@responses.activate
def test_updated_at_file_uses_course_independent_url():
    responses.get(f"{API}/api/v1/files/7", json={"id": 7, "updated_at": "T3"})
    assert c42().updated_at("files", 7) == "T3"


@responses.activate
def test_course_info():
    responses.get(COURSE, json={"name": "N", "course_code": "C"})
    assert c42().course_info()["course_code"] == "C"


# --- publish-only updates, guard support (final fix wave) ------------------

import json as _json


@responses.activate
def test_publish_page_sends_only_published():
    rsp = responses.put(f"{COURSE}/pages/syllabus", json={"url": "syllabus"})
    c42().publish_page("syllabus")
    assert _json.loads(rsp.calls[0].request.body) == {"wiki_page": {"published": True}}


@responses.activate
def test_publish_discussion_sends_only_published():
    rsp = responses.put(f"{COURSE}/discussion_topics/21", json={"id": 21})
    c42().publish_discussion(21)
    assert _json.loads(rsp.calls[0].request.body) == {"published": True}


@responses.activate
def test_publish_assignment_and_module_send_only_published():
    a = responses.put(f"{COURSE}/assignments/8", json={"id": 8})
    m = responses.put(f"{COURSE}/modules/11", json={"id": 11})
    c42().publish_assignment(8)
    c42().publish_module(11)
    assert _json.loads(a.calls[0].request.body) == {"assignment": {"published": True}}
    assert _json.loads(m.calls[0].request.body) == {"module": {"published": True}}


@responses.activate
def test_updated_at_assignment():
    responses.get(f"{COURSE}/assignments/8", json={"id": 8, "updated_at": "A1"})
    assert c42().updated_at("assignments", 8) == "A1"


@responses.activate
def test_add_to_module_without_reposition_leaves_existing_item():
    responses.get(f"{COURSE}/modules/7/items",
                  json=[{"id": 1, "type": "Page", "page_url": "lec", "position": 3}])
    assert c42().add_to_module(7, "Page", "lec", position=1, reposition=False) is True
    assert len(responses.calls) == 1                    # only the GET, no move


@responses.activate
def test_add_to_module_without_add_missing_does_not_add():
    responses.get(f"{COURSE}/modules/7/items", json=[])
    assert c42().add_to_module(7, "File", 5, position=2, add_missing=False) is False
    assert len(responses.calls) == 1                    # no POST


@responses.activate
def test_add_to_module_reports_added_item():
    responses.get(f"{COURSE}/modules/7/items", json=[])
    responses.post(f"{COURSE}/modules/7/items", json={"id": 3})
    assert c42().add_to_module(7, "File", 5, position=2) is True


@responses.activate
def test_find_page_and_module_names():
    responses.get(f"{COURSE}/pages", json=[{"title": "Syllabus", "url": "syllabus"}])
    responses.get(f"{COURSE}/modules", json=[{"id": 1, "name": "Module One: X"}])
    assert c42().find_page("Syllabus") == "syllabus"
    assert c42().find_page("Nope") is None
    assert c42().module_names() == ["Module One: X"]
    assert all(c.request.method == "GET" for c in responses.calls)

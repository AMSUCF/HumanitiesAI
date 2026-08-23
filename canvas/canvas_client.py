from __future__ import annotations

import requests


class CanvasClient:
    def __init__(self, base_url: str, token: str, course_id: str, session=None):
        self.course = f"{base_url.rstrip('/')}/api/v1/courses/{course_id}"
        self.s = session or requests.Session()
        self.s.headers["Authorization"] = f"Bearer {token}"

    def _get_all(self, url: str, **params) -> list:
        out, params = [], {"per_page": 100, **params}
        while url:
            r = self.s.get(url, params=params)
            r.raise_for_status()
            out.extend(r.json())
            url = r.links.get("next", {}).get("url")
            params = {}
        return out

    def _post(self, url: str, payload: dict) -> dict:
        r = self.s.post(url, json=payload)
        r.raise_for_status()
        return r.json()

    def _put(self, url: str, payload: dict) -> dict:
        r = self.s.put(url, json=payload)
        r.raise_for_status()
        return r.json()

    def upsert_module(self, name: str, unlock_at: str | None = None,
                      published: bool | None = None) -> int:
        payload = {"module": {"name": name}}
        if unlock_at is not None:
            payload["module"]["unlock_at"] = unlock_at
        if published is not None:
            payload["module"]["published"] = published
        for m in self._get_all(f"{self.course}/modules"):
            if m["name"] == name:
                return self._put(f"{self.course}/modules/{m['id']}", payload)["id"]
        return self._post(f"{self.course}/modules", payload)["id"]

    def upsert_page(self, title: str, body: str, published: bool = False,
                    known_url: str | None = None) -> str:
        payload = {"wiki_page": {"title": title, "body": body, "published": published}}
        if known_url is not None:
            return self._put(f"{self.course}/pages/{known_url}", payload)["url"]
        for p in self._get_all(f"{self.course}/pages", search_term=title):
            if p["title"] == title:
                return self._put(f"{self.course}/pages/{p['url']}", payload)["url"]
        return self._post(f"{self.course}/pages", payload)["url"]

    def get_page_body(self, url: str) -> str | None:
        r = self.s.get(f"{self.course}/pages/{url}")
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json().get("body") or ""

    def upsert_assignment_group(self, name: str) -> int:
        for g in self._get_all(f"{self.course}/assignment_groups"):
            if g["name"] == name:
                return g["id"]
        return self._post(f"{self.course}/assignment_groups", {"name": name})["id"]

    def upsert_discussion(self, title: str, message: str, points: int,
                          due_at: str | None, assignment_group_id: int,
                          published: bool = False,
                          known_id: int | None = None,
                          unlock_at: str | None = None,
                          lock_at: str | None = None) -> int:
        assignment = {"points_possible": points, "due_at": due_at,
                      "assignment_group_id": assignment_group_id}
        if unlock_at is not None:
            assignment["unlock_at"] = unlock_at
        if lock_at is not None:
            assignment["lock_at"] = lock_at
        payload = {
            "title": title, "message": message, "published": published,
            "assignment": assignment,
        }
        if known_id is None:
            for d in self._get_all(f"{self.course}/discussion_topics"):
                if d["title"] == title:
                    known_id = d["id"]
                    break
        if known_id is not None:
            return self._put(f"{self.course}/discussion_topics/{known_id}", payload)["id"]
        return self._post(f"{self.course}/discussion_topics", payload)["id"]

    def upsert_assignment(self, name: str, points: int, due_at: str | None,
                          assignment_group_id: int,
                          submission_types: list[str],
                          published: bool = False,
                          known_id: int | None = None,
                          unlock_at: str | None = None,
                          lock_at: str | None = None) -> int:
        payload = {
            "assignment": {
                "name": name, "points_possible": points, "due_at": due_at,
                "assignment_group_id": assignment_group_id,
                "submission_types": submission_types, "published": published,
            }
        }
        if unlock_at is not None:
            payload["assignment"]["unlock_at"] = unlock_at
        if lock_at is not None:
            payload["assignment"]["lock_at"] = lock_at
        if known_id is None:
            for a in self._get_all(f"{self.course}/assignments"):
                if a["name"] == name:
                    known_id = a["id"]
                    break
        if known_id is not None:
            return self._put(f"{self.course}/assignments/{known_id}", payload)["id"]
        return self._post(f"{self.course}/assignments", payload)["id"]

    def add_to_module(self, module_id: int, item_type: str, ref,
                      position: int | None = None) -> None:
        items = self._get_all(f"{self.course}/modules/{module_id}/items")
        if item_type == "Page":
            found = next((i for i in items if i.get("page_url") == ref), None)
            item = {"type": "Page", "page_url": ref}
        else:
            found = next((i for i in items
                          if i.get("content_id") == ref and i["type"] == item_type), None)
            item = {"type": item_type, "content_id": ref}
        if found is not None:
            if position is not None and found.get("position") != position:
                self._put(f"{self.course}/modules/{module_id}/items/{found['id']}",
                          {"module_item": {"position": position}})
            return
        if position is not None:
            item["position"] = position
        self._post(f"{self.course}/modules/{module_id}/items", {"module_item": item})

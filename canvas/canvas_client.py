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

    def upsert_module(self, name: str) -> int:
        for m in self._get_all(f"{self.course}/modules"):
            if m["name"] == name:
                return m["id"]
        return self._post(f"{self.course}/modules", {"module": {"name": name}})["id"]

    def upsert_page(self, title: str, body: str, published: bool = False) -> str:
        payload = {"wiki_page": {"title": title, "body": body, "published": published}}
        for p in self._get_all(f"{self.course}/pages", search_term=title):
            if p["title"] == title:
                return self._put(f"{self.course}/pages/{p['url']}", payload)["url"]
        return self._post(f"{self.course}/pages", payload)["url"]

    def upsert_assignment_group(self, name: str) -> int:
        for g in self._get_all(f"{self.course}/assignment_groups"):
            if g["name"] == name:
                return g["id"]
        return self._post(f"{self.course}/assignment_groups", {"name": name})["id"]

    def upsert_discussion(self, title: str, message: str, points: int,
                          due_at: str | None, assignment_group_id: int,
                          published: bool = False,
                          known_id: int | None = None) -> int:
        payload = {
            "title": title, "message": message, "published": published,
            "assignment": {"points_possible": points, "due_at": due_at,
                           "assignment_group_id": assignment_group_id},
        }
        if known_id is None:
            for d in self._get_all(f"{self.course}/discussion_topics"):
                if d["title"] == title:
                    known_id = d["id"]
                    break
        if known_id is not None:
            return self._put(f"{self.course}/discussion_topics/{known_id}", payload)["id"]
        return self._post(f"{self.course}/discussion_topics", payload)["id"]

    def add_to_module(self, module_id: int, item_type: str, ref) -> None:
        items = self._get_all(f"{self.course}/modules/{module_id}/items")
        if item_type == "Page":
            if any(i.get("page_url") == ref for i in items):
                return
            item = {"type": "Page", "page_url": ref}
        else:
            if any(i.get("content_id") == ref and i["type"] == item_type for i in items):
                return
            item = {"type": item_type, "content_id": ref}
        self._post(f"{self.course}/modules/{module_id}/items", {"module_item": item})

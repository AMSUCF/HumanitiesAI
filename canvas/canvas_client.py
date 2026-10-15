from __future__ import annotations

import hashlib
import json

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
                      published: bool | None = None,
                      known_id: int | None = None) -> int:
        payload = {"module": {"name": name}}
        if unlock_at is not None:
            payload["module"]["unlock_at"] = unlock_at
        if published is not None:
            payload["module"]["published"] = published
        if known_id is not None:
            return self._put(f"{self.course}/modules/{known_id}", payload)["id"]
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
                      position: int | None = None, reposition: bool = True,
                      add_missing: bool = True) -> bool:
        """Put an item in a module; True if it is in the module afterwards.

        reposition=False leaves an item already there where it is (only a
        new item gets `position`); add_missing=False never adds one.
        """
        items = self._get_all(f"{self.course}/modules/{module_id}/items")
        if item_type == "Page":
            found = next((i for i in items if i.get("page_url") == ref), None)
            item = {"type": "Page", "page_url": ref}
        else:
            found = next((i for i in items
                          if i.get("content_id") == ref and i["type"] == item_type), None)
            item = {"type": item_type, "content_id": ref}
        if found is not None:
            if (reposition and position is not None
                    and found.get("position") != position):
                self._put(f"{self.course}/modules/{module_id}/items/{found['id']}",
                          {"module_item": {"position": position}})
            return True
        if not add_missing:
            return False
        if position is not None:
            item["position"] = position
        self._post(f"{self.course}/modules/{module_id}/items", {"module_item": item})
        return True

    def module_names(self) -> list[str]:
        return [m["name"] for m in self._get_all(f"{self.course}/modules")]

    # publish-only updates: they leave every other field, including any
    # edit made in Canvas, as it is
    def publish_page(self, url: str) -> None:
        self._put(f"{self.course}/pages/{url}", {"wiki_page": {"published": True}})

    def publish_discussion(self, topic_id) -> None:
        self._put(f"{self.course}/discussion_topics/{topic_id}", {"published": True})

    def publish_assignment(self, assignment_id) -> None:
        self._put(f"{self.course}/assignments/{assignment_id}",
                  {"assignment": {"published": True}})

    def publish_module(self, module_id) -> None:
        self._put(f"{self.course}/modules/{module_id}", {"module": {"published": True}})

    def course_info(self) -> dict:
        r = self.s.get(self.course)
        r.raise_for_status()
        return r.json()

    def upload_file(self, path, folder: str, content_type: str) -> dict:
        """Canvas three-step upload; replaces a same-named file in `folder`."""
        data = path.read_bytes()
        pre = self._post(f"{self.course}/files", {
            "name": path.name, "size": len(data), "content_type": content_type,
            "parent_folder_path": folder, "on_duplicate": "overwrite"})
        # step 2 goes to the storage host, which must not get our token
        r = requests.post(pre["upload_url"], data=pre["upload_params"],
                          files={"file": (path.name, data, content_type)},
                          allow_redirects=False)
        if r.is_redirect:
            r = self.s.get(r.headers["Location"])
        r.raise_for_status()
        out = r.json()
        if "id" not in out and out.get("location"):
            out = self.s.get(out["location"]).json()
        return out

    def find_page(self, title: str) -> str | None:
        """The url slug of the page titled exactly `title`, else None."""
        for p in self._get_all(f"{self.course}/pages", search_term=title):
            if p["title"] == title:
                return p["url"]
        return None

    def find_or_create_page(self, title: str) -> str:
        """Return the page url slug; an existing page is never modified."""
        url = self.find_page(title)
        if url is not None:
            return url
        return self._post(f"{self.course}/pages",
                          {"wiki_page": {"title": title, "body": "<p></p>",
                                         "published": False}})["url"]

    def updated_at(self, kind: str, ref) -> str | None:
        """Change marker for a page, discussion topic, assignment or file
        (kind "pages", "discussion_topics", "assignments", "files"); None
        on 404.

        Pages and assignments return `updated_at` as written. A file returns
        "<id>@<modified_at>#<size>" of what Canvas serves for `ref`: Canvas
        bumps a file's updated_at by itself (preview conversion), and a
        Replace gives the file a new id that the old id redirects to.
        Discussion topics may
        not expose `updated_at`, so fall back to "sha:" + sha256 of a stable
        JSON of the title, message and the assignment's due_at,
        points_possible, lock_at and unlock_at: an edit to any of them in
        Canvas changes the marker.
        """
        root = self.course.split("/courses/")[0]
        url = (f"{root}/files/{ref}" if kind == "files"
               else f"{self.course}/{kind}/{ref}")
        r = self.s.get(url)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        body = r.json()
        if kind == "files":
            return f"{body.get('id')}@{body.get('modified_at')}#{body.get('size')}"
        if kind == "discussion_topics" and not body.get("updated_at"):
            a = body.get("assignment") or {}
            content = {"title": body.get("title"), "message": body.get("message") or "",
                       **{k: a.get(k) for k in
                          ("due_at", "points_possible", "lock_at", "unlock_at")}}
            return "sha:" + hashlib.sha256(
                json.dumps(content, sort_keys=True).encode("utf-8")).hexdigest()
        return body.get("updated_at")

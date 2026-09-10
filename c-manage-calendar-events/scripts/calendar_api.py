#!/usr/bin/env python3
"""Direct Google Calendar API helper for true all-day events."""

from __future__ import annotations

import argparse
import base64
import hashlib
import http.server
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import date, datetime, time as datetime_time, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


PRIVATE_DIR = Path(
    os.environ.get(
        "CODEX_GOOGLE_CALENDAR_PRIVATE_DIR",
        str(Path.home() / ".codex" / "private" / "google-calendar"),
    )
)
CLIENT_FILE = PRIVATE_DIR / "client.json"
TOKEN_FILE = PRIVATE_DIR / "token.json"
API_ROOT = "https://www.googleapis.com/calendar/v3"
CALENDAR_SCOPE = "https://www.googleapis.com/auth/calendar.events"

CREATE_FIELDS = {
    "calendar_id",
    "title",
    "start_date",
    "end_date",
    "description",
    "location",
    "timezone",
    "recurrence",
    "reminders",
    "visibility",
    "transparency",
    "color_id",
    "duplicate_check",
}
UPDATE_FIELDS = CREATE_FIELDS | {"event_id"}


class CalendarError(RuntimeError):
    pass


def json_request(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    form: dict[str, Any] | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if form is not None and payload is not None:
        raise ValueError("Use either form or payload, not both.")
    request_headers = dict(headers or {})
    data = None
    if form is not None:
        data = urllib.parse.urlencode(form).encode()
        request_headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif payload is not None:
        data = json.dumps(payload).encode()
        request_headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        url, method=method, headers=request_headers, data=data
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise CalendarError(f"Google Calendar API error {exc.code}: {detail}") from exc


def load_client() -> dict[str, Any]:
    if not CLIENT_FILE.exists():
        raise CalendarError(f"Missing OAuth client configuration: {CLIENT_FILE}")
    raw = json.loads(CLIENT_FILE.read_text())
    client = raw.get("installed") or raw.get("web")
    required = {"client_id", "client_secret", "token_uri"}
    if not isinstance(client, dict) or not required.issubset(client):
        raise CalendarError("OAuth client configuration is incomplete.")
    return client


def load_token() -> dict[str, Any]:
    if not TOKEN_FILE.exists():
        raise CalendarError(
            f"Missing OAuth token: {TOKEN_FILE}. Complete authorization first."
        )
    token = json.loads(TOKEN_FILE.read_text())
    if not token.get("refresh_token"):
        raise CalendarError("OAuth token has no refresh token.")
    return token


def save_token(token: dict[str, Any]) -> None:
    PRIVATE_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(PRIVATE_DIR, 0o700)
    TOKEN_FILE.write_text(json.dumps(token, indent=2))
    os.chmod(TOKEN_FILE, 0o600)


def valid_access_token() -> str:
    client = load_client()
    token = load_token()
    expires_at = int(token.get("expires_at", 0))
    if not token.get("access_token") or expires_at <= int(time.time()) + 30:
        refreshed = json_request(
            client["token_uri"],
            method="POST",
            form={
                "client_id": client["client_id"],
                "client_secret": client["client_secret"],
                "refresh_token": token["refresh_token"],
                "grant_type": "refresh_token",
            },
        )
        token.update(refreshed)
        token["expires_at"] = (
            int(time.time()) + int(refreshed.get("expires_in", 3600)) - 60
        )
        save_token(token)
    return str(token["access_token"])


def authorize() -> dict[str, Any]:
    client = load_client()
    verifier = (
        base64.urlsafe_b64encode(secrets.token_bytes(64))
        .rstrip(b"=")
        .decode()
    )
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .rstrip(b"=")
        .decode()
    )
    state = secrets.token_urlsafe(24)
    result: dict[str, str] = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            result.update({key: values[0] for key, values in query.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                b"<h2>Google Calendar connected.</h2>"
                b"<p>You may close this tab and return to Codex.</p>"
            )

        def log_message(self, *_: Any) -> None:
            return

    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    server.timeout = 300
    redirect_uri = f"http://127.0.0.1:{server.server_port}/"
    params = {
        "client_id": client["client_id"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": CALENDAR_SCOPE,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    auth_uri = client.get("auth_uri", "https://accounts.google.com/o/oauth2/auth")
    auth_url = auth_uri + "?" + urllib.parse.urlencode(params)
    if not webbrowser.open(auth_url):
        server.server_close()
        raise CalendarError("Could not open the Google authorization page.")
    server.handle_request()
    server.server_close()
    if result.get("state") != state or "code" not in result:
        detail = result.get("error", "authorization was not completed")
        raise CalendarError(f"Google authorization failed: {detail}.")
    token = json_request(
        client["token_uri"],
        method="POST",
        form={
            "client_id": client["client_id"],
            "client_secret": client["client_secret"],
            "code": result["code"],
            "code_verifier": verifier,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
    )
    token["expires_at"] = int(time.time()) + int(token.get("expires_in", 3600)) - 60
    save_token(token)
    return {
        "status": "authorized",
        "scope": token.get("scope", CALENDAR_SCOPE),
        "refresh_token_present": bool(token.get("refresh_token")),
    }


def api(
    path: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return json_request(
        API_ROOT + path,
        method=method,
        headers={"Authorization": f"Bearer {valid_access_token()}"},
        payload=payload,
    )


def read_input(path: str) -> dict[str, Any]:
    raw = sys.stdin.read() if path == "-" else Path(path).read_text()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CalendarError(f"Input is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise CalendarError("Input must be a JSON object.")
    return value


def iso_date(value: Any, field: str) -> date:
    if not isinstance(value, str):
        raise CalendarError(f"{field} must be an ISO date in YYYY-MM-DD format.")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise CalendarError(
            f"{field} must be an ISO date in YYYY-MM-DD format."
        ) from exc


def reject_unknown(data: dict[str, Any], allowed: set[str]) -> None:
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise CalendarError(f"Unsupported input fields: {', '.join(unknown)}")
    forbidden = {"start_time", "end_time", "dateTime"} & set(data)
    if forbidden:
        raise CalendarError(
            "Timed duration fields are forbidden. Use start_date/end_date and put "
            "the actual time in description."
        )


def normalize_event(
    data: dict[str, Any], *, partial: bool = False
) -> tuple[str, str, dict[str, Any], dict[str, Any]]:
    reject_unknown(data, UPDATE_FIELDS if partial else CREATE_FIELDS)
    calendar_id = str(data.get("calendar_id", "primary"))
    timezone = str(data.get("timezone", "Asia/Shanghai"))
    metadata = {
        "timezone": timezone,
        "duplicate_check": bool(data.get("duplicate_check", True)),
    }
    event: dict[str, Any] = {}

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            raise CalendarError("title must be a non-empty string.")
        event["summary"] = data["title"].strip()
    elif not partial:
        raise CalendarError("title is required.")

    if "start_date" in data:
        start = iso_date(data["start_date"], "start_date")
        end = (
            iso_date(data["end_date"], "end_date")
            if data.get("end_date")
            else start + timedelta(days=1)
        )
        if end <= start:
            raise CalendarError("end_date must be later than start_date.")
        event["start"] = {"date": start.isoformat()}
        event["end"] = {"date": end.isoformat()}
    elif "end_date" in data:
        raise CalendarError("end_date cannot be supplied without start_date.")
    elif not partial:
        raise CalendarError("start_date is required.")

    mappings = {
        "description": "description",
        "location": "location",
        "recurrence": "recurrence",
        "reminders": "reminders",
        "visibility": "visibility",
        "transparency": "transparency",
        "color_id": "colorId",
    }
    for source, destination in mappings.items():
        if source in data and data[source] is not None:
            event[destination] = data[source]

    return calendar_id, timezone, event, metadata


def rfc3339_boundary(day: str, timezone: str) -> str:
    parsed = iso_date(day, "date boundary")
    zone = ZoneInfo(timezone)
    return datetime.combine(parsed, datetime_time.min, tzinfo=zone).isoformat()


def encoded_calendar(calendar_id: str) -> str:
    return urllib.parse.quote(calendar_id, safe="")


def find_duplicate(
    calendar_id: str,
    event: dict[str, Any],
    timezone: str,
) -> dict[str, Any] | None:
    start_date = event["start"]["date"]
    end_date = event["end"]["date"]
    params = urllib.parse.urlencode(
        {
            "timeMin": rfc3339_boundary(start_date, timezone),
            "timeMax": rfc3339_boundary(end_date, timezone),
            "singleEvents": "true",
            "maxResults": "50",
            "q": event["summary"],
        }
    )
    result = api(
        f"/calendars/{encoded_calendar(calendar_id)}/events?{params}"
    )
    for item in result.get("items", []):
        if (
            item.get("summary") == event["summary"]
            and item.get("start", {}).get("date") == start_date
            and item.get("end", {}).get("date") == end_date
        ):
            return item
    return None


def create(data: dict[str, Any], dry_run: bool) -> dict[str, Any]:
    calendar_id, timezone, event, metadata = normalize_event(data)
    if dry_run:
        return {
            "status": "validated",
            "calendar_id": calendar_id,
            "event": event,
        }
    if metadata["duplicate_check"]:
        duplicate = find_duplicate(calendar_id, event, timezone)
        if duplicate:
            return {
                "status": "duplicate",
                "event_id": duplicate.get("id"),
                "title": duplicate.get("summary"),
                "start": duplicate.get("start"),
                "end": duplicate.get("end"),
                "html_link": duplicate.get("htmlLink"),
            }
    params = urllib.parse.urlencode({"sendUpdates": "none"})
    result = api(
        f"/calendars/{encoded_calendar(calendar_id)}/events?{params}",
        method="POST",
        payload=event,
    )
    return {
        "status": "created",
        "event_id": result.get("id"),
        "title": result.get("summary"),
        "start": result.get("start"),
        "end": result.get("end"),
        "html_link": result.get("htmlLink"),
    }


def normalize_window(value: Any, field: str, timezone: str) -> str:
    if not isinstance(value, str):
        raise CalendarError(f"{field} is required.")
    if len(value) == 10:
        return rfc3339_boundary(value, timezone)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CalendarError(f"{field} must be an ISO date or datetime.") from exc
    if parsed.tzinfo is None:
        raise CalendarError(f"{field} datetime must include a timezone.")
    return parsed.isoformat()


def search(data: dict[str, Any]) -> dict[str, Any]:
    allowed = {"calendar_id", "time_min", "time_max", "query", "timezone", "max_results"}
    reject_unknown(data, allowed)
    calendar_id = str(data.get("calendar_id", "primary"))
    timezone = str(data.get("timezone", "Asia/Shanghai"))
    params = {
        "timeMin": normalize_window(data.get("time_min"), "time_min", timezone),
        "timeMax": normalize_window(data.get("time_max"), "time_max", timezone),
        "singleEvents": "true",
        "orderBy": "startTime",
        "maxResults": str(int(data.get("max_results", 50))),
    }
    if data.get("query"):
        params["q"] = str(data["query"])
    result = api(
        f"/calendars/{encoded_calendar(calendar_id)}/events?"
        + urllib.parse.urlencode(params)
    )
    items = []
    for item in result.get("items", []):
        items.append(
            {
                "id": item.get("id"),
                "title": item.get("summary"),
                "start": item.get("start"),
                "end": item.get("end"),
                "location": item.get("location"),
                "description": item.get("description"),
                "html_link": item.get("htmlLink"),
                "status": item.get("status"),
            }
        )
    return {"status": "ok", "events": items}


def get_event(data: dict[str, Any]) -> dict[str, Any]:
    allowed = {"calendar_id", "event_id"}
    reject_unknown(data, allowed)
    calendar_id = str(data.get("calendar_id", "primary"))
    event_id = data.get("event_id")
    if not isinstance(event_id, str) or not event_id:
        raise CalendarError("event_id is required.")
    event = api(
        f"/calendars/{encoded_calendar(calendar_id)}/events/"
        f"{urllib.parse.quote(event_id, safe='')}"
    )
    return {"status": "ok", "event": event}


def update(data: dict[str, Any], dry_run: bool) -> dict[str, Any]:
    event_id = data.get("event_id")
    if not isinstance(event_id, str) or not event_id:
        raise CalendarError("event_id is required.")
    calendar_id, _, patch, _ = normalize_event(data, partial=True)
    if not patch:
        raise CalendarError("At least one event field must be supplied.")
    if dry_run:
        return {
            "status": "validated",
            "calendar_id": calendar_id,
            "event_id": event_id,
            "patch": patch,
        }
    params = urllib.parse.urlencode({"sendUpdates": "none"})
    result = api(
        f"/calendars/{encoded_calendar(calendar_id)}/events/"
        f"{urllib.parse.quote(event_id, safe='')}?{params}",
        method="PATCH",
        payload=patch,
    )
    return {
        "status": "updated",
        "event_id": result.get("id"),
        "title": result.get("summary"),
        "start": result.get("start"),
        "end": result.get("end"),
        "html_link": result.get("htmlLink"),
    }


def delete(data: dict[str, Any], confirmed: bool) -> dict[str, Any]:
    allowed = {"calendar_id", "event_id"}
    reject_unknown(data, allowed)
    if not confirmed:
        raise CalendarError("Deletion requires --confirm-delete.")
    calendar_id = str(data.get("calendar_id", "primary"))
    event_id = data.get("event_id")
    if not isinstance(event_id, str) or not event_id:
        raise CalendarError("event_id is required.")
    params = urllib.parse.urlencode({"sendUpdates": "none"})
    api(
        f"/calendars/{encoded_calendar(calendar_id)}/events/"
        f"{urllib.parse.quote(event_id, safe='')}?{params}",
        method="DELETE",
    )
    return {"status": "deleted", "event_id": event_id}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Use the direct Google Calendar API with private OAuth credentials."
    )
    parser.add_argument(
        "action",
        choices={"authorize", "create", "search", "get", "update", "delete"},
    )
    parser.add_argument("--input", default="-", help="JSON file path, or - for stdin")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate create/update payloads without using credentials or the API",
    )
    parser.add_argument(
        "--confirm-delete",
        action="store_true",
        help="Required acknowledgement for a delete request",
    )
    args = parser.parse_args()
    try:
        if args.action == "authorize":
            if args.dry_run or args.confirm_delete:
                raise CalendarError(
                    "authorize does not accept --dry-run or --confirm-delete."
                )
            print(json.dumps(authorize(), indent=2, ensure_ascii=False))
            return 0
        data = read_input(args.input)
        if args.action == "create":
            result = create(data, args.dry_run)
        elif args.action == "search":
            if args.dry_run:
                raise CalendarError("--dry-run is only supported for create and update.")
            result = search(data)
        elif args.action == "get":
            if args.dry_run:
                raise CalendarError("--dry-run is only supported for create and update.")
            result = get_event(data)
        elif args.action == "update":
            result = update(data, args.dry_run)
        else:
            if args.dry_run:
                raise CalendarError("--dry-run is not supported for delete.")
            result = delete(data, args.confirm_delete)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (CalendarError, OSError, ValueError, ZoneInfoNotFoundError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

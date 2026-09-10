#!/usr/bin/env python3
"""Audit a generated long-horizon recursive setup folder.

This is a deterministic structural and cross-file audit, not a semantic proof.
The five canonical documents stay at the operating-folder root. Node paths and
parent relationships are read from TASK_ARCHITECTURE.md, so the audit does not
assume fixed stage/subtask folder names or a fixed recursion depth.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


ROOT_DOCS = [
    "OPERATING_INDEX.md",
    "PROJECT_BRIEF.md",
    "TASK_MODEL.md",
    "TASK_ARCHITECTURE.md",
    "MASTER_PROGRESS.md",
]

FORBIDDEN_ROOT_DOCS = [
    "IMPLEMENTATION_BLUEPRINT.md",
    "APPROVAL_LOG.md",
    "SETUP_PROGRESS.md",
]

WORK_STATES = {
    "planned",
    "ready",
    "active",
    "blocked",
    "done",
    "deferred",
    "waived",
}
TERMINAL_WORK_STATES = {"done", "deferred", "waived"}
GATE_STATES = {"pending", "approved", "rejected", "waived"}
ALLOWED_NODE_TYPES = {"stage", "subtask", "dynamic discovery"}

REQUIRED_HEADINGS = {
    "OPERATING_INDEX.md": [
        ("read routes", ("start here", "read order", "cold start")),
        ("document map", ("document map",)),
        ("update routing", ("update routing", "update protocol")),
        (
            "final prompt location",
            ("final goal prompt location", "final codex goal prompt location"),
        ),
    ],
    "PROJECT_BRIEF.md": [
        ("original request or intent", ("original request", "intent")),
        ("goal", ("goal",)),
        ("source inputs", ("source inputs", "inputs")),
        ("scope and boundaries", ("scope and boundaries", "scope")),
        ("decision authority", ("decision authority", "roles", "ownership")),
        ("success standard", ("final success standard", "success standard", "success")),
        ("final goal prompt", ("final codex goal prompt", "final goal prompt")),
    ],
    "TASK_MODEL.md": [
        ("approved two-step definition", ("approved two-step definition",)),
        ("goal", ("goal",)),
        ("outcomes", ("outcomes",)),
        ("deliverables", ("deliverables", "expected outputs")),
        ("work model", ("work model", "execution plan")),
        (
            "approvals and consequential actions",
            (
                "approvals and human checkpoints",
                "approvals and consequential actions",
                "approvals and risky actions",
            ),
        ),
        (
            "details later runs must not lose",
            ("details later runs must not lose",),
        ),
        ("decisions and unknowns", ("decisions and unknowns",)),
        ("constraints", ("constraints",)),
        ("coverage risks", ("coverage risks",)),
        ("unresolved items", ("unresolved items",)),
    ],
    "TASK_ARCHITECTURE.md": [
        (
            "stage/subtask-to-node map",
            ("stage and subtask to node", "stage subtask to node", "task-to-node", "model-to-node"),
        ),
        ("node registry", ("node registry", "node map")),
        (
            "architecture-relevant constraints and blockers",
            ("architecture relevant constraints and blockers", "constraints and blockers"),
        ),
        (
            "runtime human checkpoints",
            ("runtime human checkpoints", "human checkpoints"),
        ),
        (
            "deferred or rejected nodes",
            ("deferred or rejected nodes", "deferred or rejected"),
        ),
        ("structural check", ("structural check", "orphan")),
    ],
    "MASTER_PROGRESS.md": [
        ("active work", ("parallel execution", "current cursor", "active node", "active lanes")),
        ("node state", ("node state", "status table", "node statuses")),
        ("gate decisions", ("gate decisions", "approval gates")),
        ("blockers", ("blockers",)),
        ("runtime queue", ("runtime queue", "next node queue", "queue")),
        ("completion rule", ("completion rule",)),
    ],
}

NODE_REQUIRED_HEADINGS = [
    ("objective and success", ("objective and success",)),
    ("scope", ("scope",)),
    ("relevant context", ("relevant parent context", "relevant context", "parent context")),
    ("decision latitude", ("decision latitude",)),
    ("working approach", ("working approach", "execution")),
    ("tracking", ("tracking",)),
    ("result and completion", ("result and completion", "completion and handoff")),
]

COLUMN_ALIASES = {
    "node_id": ("node id", "id"),
    "node_file": ("node file", "node path", "file", "path"),
    "node_type": ("type", "node type"),
    "parent_id": ("parent id", "parent node", "parent"),
    "relationship": (
        "related node ids relationship",
        "related nodes relationship",
        "relationship",
        "relationships",
    ),
    "purpose": ("purpose", "why this node exists"),
    "outcome": (
        "outcome deliverable owned",
        "outcome",
        "deliverable owned",
        "owned outcome",
    ),
    "quality": ("quality needs", "quality", "verification needs"),
    "merge_handoff": (
        "merge handoff condition",
        "merge condition",
        "join reconciliation handoff condition",
        "join reconciliation handoff",
        "handoff condition",
        "join reconciliation condition",
        "join condition",
        "handoff",
    ),
    "assignment": ("assignment", "assignment name", "assignment id"),
    "assigned_work": ("assigned work", "work", "scope", "items"),
    "worker": ("worker", "worker reference", "owner", "agent"),
    "assignment_result": ("result evidence", "result link", "evidence link", "result", "evidence"),
    "constraint": ("constraint or blocker", "constraint", "blocker"),
    "affected_node": (
        "affected stage subtask or node file",
        "affected stage or node",
        "affected node",
    ),
    "constraint_effect": (
        "what it constrains or blocks",
        "constraint effect",
        "effect",
        "impact",
    ),
    "resolution": (
        "planning response or resolution condition",
        "resolution condition",
        "planning response",
        "response",
    ),
    "stage": ("stage",),
    "subtask": ("subtask",),
    "state": (
        "work state",
        "local state",
        "item state",
        "item status",
        "status",
        "state",
    ),
    "result_link": ("result link", "evidence link", "result", "evidence"),
    "blocker_ref": ("blocker / gate ref", "blocker gate ref", "gate ref", "blocker"),
    "active_node_id": ("active node id", "node id", "active node"),
    "active_node_file": ("active node file", "node file", "active file"),
    "next_action": ("next action", "next", "next action blocker"),
    "gate_id": ("gate", "gate name", "gate id", "edge / gate id", "edge gate id", "edge id"),
    "gate_state": ("gate state", "state", "decision"),
    "blocker_id": ("blocker", "blocker name", "blocker id", "id"),
    "updated": ("updated", "date", "last updated"),
}

PLACEHOLDER_WORDS = (
    "project name",
    "node name",
    "n-###",
    "root or n-###",
    "approved stage",
    "approved subtask",
    "stage / workstream",
    "node idea",
    "observable result",
    "observable outcome",
    "specific action",
    "required qualities",
    "path or url",
    "absolute/path",
    "describe ",
    "state the ",
    "state or ",
    "who or what",
    "what must be true",
    "source set",
    "source ref",
    "meaningful item",
    "material uncertainty",
    "useful condition",
    "completion / review ref",
    "date and result",
    "constraint ids",
    "field",
)

GENERIC_PHRASES = [
    "do the task",
    "complete the task",
    "finish the work",
    "handle this stage",
    "work on this",
]


class AuditReport:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def normalize_label(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def canonical_node_type(value: str) -> str:
    normalized = normalize_label(value)
    if normalized == "dynamic discovery node":
        return "dynamic discovery"
    return normalized if normalized in ALLOWED_NODE_TYPES else ""


def clean_cell(value: str) -> str:
    value = value.strip().strip(chr(96)).strip()
    link = re.fullmatch(r"\[[^\]]*\]\(([^)]+)\)", value)
    if link:
        value = link.group(1).strip()
    return value.strip(chr(96)).strip()


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", text))


def heading_matches(text: str) -> list[re.Match[str]]:
    return list(re.finditer(r"^(#{1,6})[ \t]+(.+?)\s*$", text, re.MULTILINE))


def find_heading(text: str, aliases: tuple[str, ...]) -> re.Match[str] | None:
    wanted = [normalize_label(alias) for alias in aliases]
    for match in heading_matches(text):
        title = normalize_label(match.group(2))
        if any(title == alias or title.startswith(alias + " ") for alias in wanted):
            return match
    return None


def section_body(text: str, aliases: tuple[str, ...]) -> str:
    match = find_heading(text, aliases)
    if match is None:
        return ""
    level = len(match.group(1))
    end = len(text)
    for following in heading_matches(text[match.end() :]):
        if len(following.group(1)) <= level:
            end = match.end() + following.start()
            break
    return text[match.end() : end].strip()


def has_placeholder(text: str) -> bool:
    for content in re.findall(r"\[([^\]]+)\]", text):
        lowered = content.casefold().strip()
        if any(word in lowered for word in PLACEHOLDER_WORDS):
            return True
    return bool(
        re.search(r"\b(?:TBD|TODO)\b", text, re.IGNORECASE)
        or re.search(r"(?im)^\s*todo\s*:", text)
    )


def parse_prompt(text: str) -> str:
    body = section_body(text, ("final codex goal prompt", "final goal prompt"))
    match = re.search(
        r"(?:\x60{3}|~{3})(?:text)?\s*\n([\s\S]*?)\n(?:\x60{3}|~{3})",
        body,
    )
    return match.group(1).strip() if match else ""


def split_table_line(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [clean_cell(cell) for cell in line.split("|")]


def is_table_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|")


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def parse_markdown_table(body: str) -> tuple[list[str], list[dict[str, str]]]:
    lines = body.splitlines()
    for index in range(len(lines) - 1):
        if not is_table_line(lines[index]) or not is_table_line(lines[index + 1]):
            continue
        headers = split_table_line(lines[index])
        if not is_separator_row(split_table_line(lines[index + 1])):
            continue
        rows: list[dict[str, str]] = []
        for line in lines[index + 2 :]:
            if not is_table_line(line):
                break
            cells = split_table_line(line)
            if is_separator_row(cells):
                continue
            if len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))
        return headers, rows
    return [], []


def row_value(row: dict[str, str], column: str) -> str:
    aliases = {normalize_label(alias) for alias in COLUMN_ALIASES[column]}
    for header, value in row.items():
        if normalize_label(header) in aliases:
            return clean_cell(value)
    return ""


def check_table_columns(
    report: AuditReport,
    label: str,
    headers: list[str],
    required: tuple[str, ...],
) -> None:
    normalized = {normalize_label(header) for header in headers}
    for column in required:
        aliases = {normalize_label(alias) for alias in COLUMN_ALIASES[column]}
        if not normalized.intersection(aliases):
            report.error(f"{label} table is missing column: {column}")


def metadata_value(text: str, labels: tuple[str, ...]) -> str:
    for label in labels:
        match = re.search(
            rf"^\s*{re.escape(label)}\s*:\s*(.*?)\s*$",
            text,
            re.MULTILINE | re.IGNORECASE,
        )
        if match:
            return clean_cell(match.group(1))
    return ""


def relative_path(root: Path, raw_value: str) -> str | None:
    value = clean_cell(raw_value)
    if not value:
        return ""
    value = value.split("#", 1)[0].strip()
    if not value or value.casefold() in {"none", "n/a", "-", "—"}:
        return ""
    candidate = Path(value)
    if candidate.is_absolute() or "://" in value or ".." in candidate.parts:
        return None
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate.as_posix().lstrip("./")


def check_heading_groups(
    report: AuditReport,
    filename: str,
    text: str,
    groups: list[tuple[str, tuple[str, ...]]],
) -> None:
    for label, aliases in groups:
        match = find_heading(text, aliases)
        if match is None:
            report.error(f"{filename} missing required section: {label}")
            continue
        if word_count(section_body(text, aliases)) < 4:
            report.warning(f"{filename} section may be too shallow: {label}")


def check_parent_cycles(report: AuditReport, parents: dict[str, str]) -> None:
    for start in parents:
        seen: set[str] = set()
        current = start
        while current in parents and parents[current].upper() != "ROOT":
            if current in seen:
                report.error(f"Parent cycle detected involving node {current}")
                break
            seen.add(current)
            current = parents[current]


def duplicate_values(rows: list[dict[str, str]], column: str) -> set[str]:
    values = [row_value(row, column) for row in rows]
    counts = Counter(value for value in values if value)
    return {value for value, count in counts.items() if count > 1}


def looks_like_node(text: str) -> bool:
    has_id = bool(re.search(r"(?im)^\s*Node ID\s*:", text))
    has_parent = bool(re.search(r"(?im)^\s*Parent file\s*:", text))
    has_tracking = find_heading(
        text, ("tracking",)
    ) is not None
    return has_id or (has_parent and has_tracking)


def markdown_candidates(root: Path) -> set[str]:
    candidates: set[str] = set()
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if len(relative.parts) == 1 and relative.name in ROOT_DOCS:
            continue
        if any(part.startswith(".") for part in relative.parts):
            continue
        if looks_like_node(read(path)):
            candidates.add(relative.as_posix())
    return candidates


def path_is_mentioned(index_text: str, node_path: str) -> bool:
    if node_path in index_text:
        return True
    parts = Path(node_path).parts
    for length in range(1, len(parts)):
        prefix = Path(*parts[:length]).as_posix()
        if f"{prefix}/**" in index_text or f"{prefix}/..." in index_text:
            return True
    return False


def audit(root: Path) -> AuditReport:
    report = AuditReport()
    root = root.resolve()
    if not root.exists() or not root.is_dir():
        report.error(f"Setup folder does not exist or is not a directory: {root}")
        return report

    texts: dict[str, str] = {}
    for filename in ROOT_DOCS:
        path = root / filename
        if not path.is_file():
            report.error(f"Missing required root document: {filename}")
            continue
        text = read(path)
        texts[filename] = text
        if not text.strip():
            report.error(f"{filename} is empty")
            continue
        if has_placeholder(text):
            report.error(f"{filename} contains an unresolved placeholder or TODO")
        check_heading_groups(report, filename, text, REQUIRED_HEADINGS[filename])

    for filename in FORBIDDEN_ROOT_DOCS:
        if (root / filename).exists():
            report.error(f"Obsolete root document should not be generated: {filename}")

    index_text = texts.get("OPERATING_INDEX.md", "")
    master_text = texts.get("MASTER_PROGRESS.md", "")
    parallelism_active = find_heading(
        master_text, ("parallel execution", "parallelism")
    ) is not None
    for filename in ROOT_DOCS[1:]:
        if index_text and filename not in index_text:
            report.error(f"OPERATING_INDEX.md does not reference {filename}")

    project_brief_text = texts.get("PROJECT_BRIEF.md", "")
    if project_brief_text:
        prompt = parse_prompt(project_brief_text)
        if not prompt:
            report.error("PROJECT_BRIEF.md is missing a fenced final Codex goal prompt")
        else:
            if len(prompt) >= 4000:
                report.error(f"Final Codex goal prompt is too long: {len(prompt)} chars")
            for filename in ROOT_DOCS:
                if filename not in prompt:
                    report.error(
                        f"Final Codex goal prompt does not reference {filename}"
                    )
            if "c-long-horizon-start-to-end-setup" in prompt:
                report.error("Final Codex goal prompt invokes the setup skill")

    task_model_text = texts.get("TASK_MODEL.md", "")
    if task_model_text:
        two_step = section_body(task_model_text, ("approved two-step definition",))
        if not two_step:
            report.error("TASK_MODEL.md is missing the approved two-step definition")
        else:
            step_one = section_body(two_step, ("step 1 - structure approval",))
            step_two = section_body(two_step, ("step 2 - detail approval",))
            if not step_one:
                report.error("TASK_MODEL.md is missing Step 1 structure approval")
            else:
                for label, aliases in [
                    ("Step 1 stages", ("stages",)),
                    ("Step 1 subtasks", ("subtasks",)),
                ]:
                    if find_heading(step_one, aliases) is None:
                        report.error(f"TASK_MODEL.md is missing {label}")
            if not step_two:
                report.error("TASK_MODEL.md is missing Step 2 detail approval")
            else:
                if find_heading(
                    step_two,
                    ("stages with subtasks and rich details", "detailed stages"),
                ) is None:
                    report.error("TASK_MODEL.md is missing Step 2 detailed stages")
                if find_heading(step_two, ("lazy points",)) is None:
                    report.error("TASK_MODEL.md is missing Step 2 Lazy Points")

    architecture_text = texts.get("TASK_ARCHITECTURE.md", "")
    registry: list[dict[str, str]] = []
    registry_by_id: dict[str, dict[str, str]] = {}
    registry_by_path: dict[str, dict[str, str]] = {}
    if architecture_text:
        map_body = section_body(
            architecture_text,
            ("stage and subtask to node", "stage subtask to node"),
        )
        map_headers, _ = parse_markdown_table(map_body)
        if not map_headers:
            report.error(
                "TASK_ARCHITECTURE.md stage/subtask-to-node map is missing a Markdown table"
            )
        else:
            check_table_columns(
                report,
                "TASK_ARCHITECTURE.md stage/subtask-to-node map",
                map_headers,
                ("stage", "subtask", "node_file"),
            )

        registry_body = section_body(architecture_text, ("node registry", "node map"))
        headers, rows = parse_markdown_table(registry_body)
        if not headers:
            report.error("TASK_ARCHITECTURE.md node registry is missing a Markdown table")
        else:
            check_table_columns(
                report,
                "TASK_ARCHITECTURE.md node registry",
                headers,
                (
                    "node_id",
                    "node_file",
                    "node_type",
                    "parent_id",
                    "relationship",
                    "purpose",
                    "outcome",
                    "quality",
                    "merge_handoff",
                ),
            )

        for row in rows:
            node_id = row_value(row, "node_id")
            node_file = row_value(row, "node_file")
            node_type = row_value(row, "node_type")
            parent_id = row_value(row, "parent_id")
            if not node_id and not node_file:
                continue
            record = {
                "id": node_id,
                "path": relative_path(root, node_file) or "",
                "raw_path": node_file,
                "node_type": node_type,
                "parent": parent_id,
            }
            registry.append(record)
            if not node_id:
                report.error("TASK_ARCHITECTURE.md node registry row is missing node ID")
            elif node_id in registry_by_id:
                report.error(f"Duplicate node ID in architecture registry: {node_id}")
            else:
                registry_by_id[node_id] = record
            if not node_file:
                report.error(
                    f"Architecture node {node_id or '<unknown>'} is missing a node file"
                )
            elif record["path"] == "":
                report.error(
                    f"Architecture node {node_id or '<unknown>'} has an invalid node path"
                )
            elif record["path"] in registry_by_path:
                report.error(
                    f"Duplicate node path in architecture registry: {record['path']}"
                )
            else:
                registry_by_path[record["path"]] = record
            canonical_type = canonical_node_type(node_type)
            if not node_type:
                report.error(
                    f"Architecture node {node_id or '<unknown>'} is missing a node type"
                )
            elif not canonical_type:
                report.error(
                    f"Architecture node {node_id or '<unknown>'} has unsupported node type: {node_type}"
                )

        if not registry:
            report.error("TASK_ARCHITECTURE.md node registry contains no nodes")

        constraints_body = section_body(
            architecture_text,
            (
                "architecture relevant constraints and blockers",
                "constraints and blockers",
            ),
        )
        constraint_headers, _ = parse_markdown_table(constraints_body)
        if constraint_headers:
            check_table_columns(
                report,
                "TASK_ARCHITECTURE.md constraints and blockers",
                constraint_headers,
                ("constraint", "affected_node", "constraint_effect", "resolution"),
            )
    parent_map = {
        record["id"]: record["parent"]
        for record in registry
        if record["id"]
    }
    for node_id, parent_id in parent_map.items():
        if not parent_id:
            report.error(f"Architecture node {node_id} is missing a parent ID")
        elif parent_id.upper() != "ROOT" and parent_id not in registry_by_id:
            report.error(f"Architecture node {node_id} has missing parent ID: {parent_id}")
    check_parent_cycles(report, parent_map)

    registered_paths = set(registry_by_path)
    candidate_paths = markdown_candidates(root)
    for orphan in sorted(candidate_paths - registered_paths):
        report.error(f"Node-like Markdown file is absent from TASK_ARCHITECTURE.md: {orphan}")

    node_texts: dict[str, str] = {}
    for node_path in sorted(registered_paths):
        path = root / node_path
        if not path.is_file():
            report.error(f"Architecture registry path does not exist: {node_path}")
            continue
        if path.suffix.casefold() != ".md":
            report.error(f"Registered node is not a Markdown file: {node_path}")
        node_texts[node_path] = read(path)
        if not path_is_mentioned(index_text, node_path):
            report.error(
                f"Registered node is not reachable from OPERATING_INDEX.md: {node_path}"
            )

    children_by_parent: dict[str, list[str]] = {}
    for record in registry:
        if record["id"] and record["parent"].upper() != "ROOT":
            children_by_parent.setdefault(record["parent"], []).append(record["id"])

    for node_path, text in node_texts.items():
        record = registry_by_path[node_path]
        if has_placeholder(text):
            report.error(f"{node_path} contains an unresolved placeholder or TODO")
        if any(phrase in text.casefold() for phrase in GENERIC_PHRASES):
            report.warning(f"{node_path} contains generic task language")
        check_heading_groups(report, node_path, text, NODE_REQUIRED_HEADINGS)

        node_id = metadata_value(text, ("Node ID",))
        if not node_id:
            report.error(f"{node_path} is missing Node ID metadata")
        elif node_id != record["id"]:
            report.error(f"{node_path} Node ID does not match TASK_ARCHITECTURE.md")

        declared_type = metadata_value(text, ("Node type", "Type"))
        declared_canonical_type = canonical_node_type(declared_type)
        registry_canonical_type = canonical_node_type(record["node_type"])
        if not declared_type:
            report.error(f"{node_path} is missing node-type metadata")
        elif not declared_canonical_type:
            report.error(f"{node_path} has unsupported node type: {declared_type}")
        elif declared_canonical_type != registry_canonical_type:
            report.error(
                f"{node_path} node type does not match TASK_ARCHITECTURE.md"
            )

        parent_file = metadata_value(text, ("Parent file", "Parent"))
        if not parent_file:
            report.error(f"{node_path} is missing parent-file metadata")
        else:
            actual_parent = relative_path(root, parent_file)
            expected_parent = (
                "TASK_ARCHITECTURE.md"
                if record["parent"].upper() == "ROOT"
                else registry_by_id.get(record["parent"], {}).get("path", "")
            )
            if actual_parent != expected_parent:
                report.error(
                    f"{node_path} parent file does not match its architecture parent"
                )

        declared_parent_id = metadata_value(text, ("Parent ID", "Parent node"))
        if declared_parent_id and declared_parent_id != record["parent"]:
            report.error(f"{node_path} Parent ID does not match TASK_ARCHITECTURE.md")

        lowered = text.casefold()
        if declared_canonical_type == "dynamic discovery":
            dynamic_section = section_body(text, ("dynamic discovery",))
            if not dynamic_section:
                report.error(f"{node_path} is missing its Dynamic Discovery section")
            for label, markers in [
                (
                    "discovery sources",
                    ("discovery sources", "inclusion and exclusion", "deduplication"),
                ),
                (
                    "stopping rule and denominator",
                    ("stopping rule", "denominator"),
                ),
                (
                    "approved structural scope",
                    ("approved structural scope", "owning stage subtree"),
                ),
                (
                    "structural modification authority",
                    ("structural modification authority", "may create", "may update"),
                ),
                (
                    "discovery handoff",
                    ("discovery handoff", "production receives"),
                ),
            ]:
                if not any(marker in dynamic_section.casefold() for marker in markers):
                    report.error(f"{node_path} Dynamic Discovery section is missing {label}")

        node_parallel_heading = find_heading(text, ("parallelism",))
        if not parallelism_active and node_parallel_heading is not None:
            report.error(
                f"{node_path} contains a parallelism section without active parallelism"
            )
        if "guardrail" not in lowered:
            report.error(f"{node_path} is missing guardrails")
        if not any(
            marker in lowered
            for marker in ("done checks", "done signals", "local done", "completion checks")
        ):
            report.error(f"{node_path} is missing local done checks")
        if "completion rule" not in lowered:
            report.error(f"{node_path} is missing a completion rule")
        if "handoff" not in lowered:
            report.error(f"{node_path} is missing a handoff rule")
        if "result" not in lowered or "evidence" not in lowered:
            report.error(f"{node_path} is missing a result/evidence note")

        tracking = section_body(
            text, ("tracking",)
        )
        tracking_headers, tracking_rows = parse_markdown_table(tracking)
        if not tracking_headers:
            report.error(f"{node_path} tracking section is missing a Markdown table")
        else:
            check_table_columns(
                report,
                f"{node_path} tracking",
                tracking_headers,
                ("state", "next_action"),
            )
            output_headers = {
                normalize_label(header) for header in tracking_headers
            }
            if not output_headers.intersection(
                {
                    normalize_label(alias)
                    for alias in (
                        "output / reason",
                        "output path or reason",
                        "output",
                        "reason",
                    )
                }
            ):
                report.error(f"{node_path} tracking is missing output/reason column")
            if not output_headers.intersection(
                {
                    normalize_label(alias)
                    for alias in ("evidence", "count", "evidence / count")
                }
            ):
                report.warning(f"{node_path} tracking has no evidence/count column")

            active_rows = [
                row
                for row in tracking_rows
                if row_value(row, "state").casefold() in {"active", "modified"}
            ]
            if not parallelism_active and len(active_rows) > 1:
                report.error(
                    f"{node_path} has more than one active or modified tracking row"
                )

        for child_id in children_by_parent.get(record["id"], []):
            child_path = registry_by_id[child_id]["path"]
            if child_path not in text and child_id not in text:
                report.error(
                    f"{node_path} does not list child {child_id} or {child_path}"
                )

    master_text = texts.get("MASTER_PROGRESS.md", "")
    state_by_id: dict[str, dict[str, str]] = {}
    if master_text:
        state_body = section_body(
            master_text, ("node state", "status table", "node statuses")
        )
        state_headers, state_rows = parse_markdown_table(state_body)
        if not state_headers:
            report.error(
                "MASTER_PROGRESS.md node-state section is missing a Markdown table"
            )
        else:
            check_table_columns(
                report,
                "MASTER_PROGRESS.md node state",
                state_headers,
                ("node_id", "state"),
            )
            for value in sorted(duplicate_values(state_rows, "node_id")):
                report.error(f"Duplicate canonical node-state row: {value}")
            for row in state_rows:
                node_id = row_value(row, "node_id")
                if not node_id:
                    continue
                state_by_id[node_id] = row
                state = row_value(row, "state").casefold()
                if state not in WORK_STATES:
                    report.error(f"Node {node_id} has invalid work state: {state}")
                result_link = row_value(row, "result_link")
                result_path = relative_path(root, result_link)
                if result_path is None:
                    report.error(f"Node {node_id} has an invalid result link")
                elif result_path and not (root / result_path).is_file():
                    report.error(
                        f"Node {node_id} result link path does not exist: {result_path}"
                    )

        registry_ids = set(registry_by_id)
        state_ids = set(state_by_id)
        for node_id in sorted(registry_ids - state_ids):
            report.error(f"Architecture node has no canonical state row: {node_id}")
        for node_id in sorted(state_ids - registry_ids):
            report.error(f"Node-state row references unknown node: {node_id}")

        active_ids = {
            node_id for node_id, row in state_by_id.items()
            if row_value(row, "state").casefold() == "active"
        }
        if parallelism_active:
            runtime_body = section_body(master_text, ("parallel execution", "parallelism"))
            assignment_body = section_body(runtime_body, ("assignment record", "assignments"))
            headers, assignments = parse_markdown_table(assignment_body or runtime_body)
            if not headers:
                report.error("MASTER_PROGRESS.md is missing its assignment table")
            else:
                check_table_columns(
                    report, "MASTER_PROGRESS.md assignments", headers,
                    ("assignment", "node_file", "assigned_work", "worker", "state",
                     "assignment_result", "next_action"),
                )
            for name in sorted(duplicate_values(assignments, "assignment")):
                report.error(f"Duplicate assignment: {name}")

            stage_path = relative_path(root, metadata_value(runtime_body, ("Active stage",)))
            stage_record = registry_by_path.get(stage_path or "", {})
            if stage_path and canonical_node_type(stage_record.get("node_type", "")) != "stage":
                report.error("MASTER_PROGRESS.md active stage is not a registered Stage node")
            assigned_active_ids: set[str] = set()
            active_scopes: set[tuple[str, str]] = set()
            for row in assignments:
                name = row_value(row, "assignment")
                node_path = relative_path(root, row_value(row, "node_file"))
                record = registry_by_path.get(node_path or "")
                if not name or not row_value(row, "assigned_work"):
                    report.error("Assignment is missing its name or assigned work")
                if record is None:
                    report.error(f"Assignment {name} references an unknown node file")
                    continue
                state = row_value(row, "state").casefold()
                if state not in WORK_STATES:
                    report.error(f"Assignment {name} has invalid work state: {state}")
                result = row_value(row, "assignment_result")
                if result:
                    result_path = relative_path(root, result)
                    if result_path is None or (result_path and not (root / result_path).is_file()):
                        report.error(f"Assignment {name} has an invalid result/evidence link")
                if state != "active":
                    continue
                node_id = record["id"]
                assigned_active_ids.add(node_id)
                if node_id not in active_ids:
                    report.error(f"Active assignment {name} belongs to a node that is not active")
                if not row_value(row, "worker"):
                    report.error(f"Active assignment {name} is missing its worker")
                scope = (node_id, normalize_label(row_value(row, "assigned_work")))
                if scope in active_scopes:
                    report.error(f"Duplicate active assignment scope for node {node_id}")
                active_scopes.add(scope)

                # Use the registered hierarchy, not folder names or hierarchy depth.
                ancestor = record
                seen: set[str] = set()
                while canonical_node_type(ancestor.get("node_type", "")) != "stage":
                    if ancestor.get("id", "") in seen:
                        break
                    seen.add(ancestor.get("id", ""))
                    ancestor = registry_by_id.get(ancestor.get("parent", ""), {})
                    if not ancestor:
                        break
                if not stage_record or ancestor.get("id") != stage_record.get("id"):
                    report.error(f"Active assignment {name} is outside the recorded active stage")
            for node_id in sorted(active_ids - assigned_active_ids):
                report.error(f"Active node {node_id} is missing from assignments")
            if active_ids and not stage_path:
                report.error("MASTER_PROGRESS.md is missing its active stage")

            for label, aliases in [
                ("runtime protocol", ("runtime protocol", "execution protocol")),
                ("pause and resume", ("pause and resume", "resume")),
            ]:
                if not section_body(runtime_body, aliases):
                    report.error(f"MASTER_PROGRESS.md parallel execution is missing {label}")
            if not find_heading(
                index_text,
                ("parallel execution route", "parallel runtime route", "parallel execution", "parallelism"),
            ):
                report.error("OPERATING_INDEX.md is missing a parallel-execution navigation route")
        else:
            cursor_body = section_body(master_text, ("current cursor", "active node", "active lanes"))
            headers, cursor_rows = parse_markdown_table(cursor_body)
            if not headers:
                report.error("MASTER_PROGRESS.md active cursor is missing a Markdown table")
            else:
                check_table_columns(
                    report, "MASTER_PROGRESS.md active cursor", headers,
                    ("active_node_id", "active_node_file", "next_action"),
                )
            cursor_ids: set[str] = set()
            for row in cursor_rows:
                node_id = row_value(row, "active_node_id")
                if not node_id or node_id.casefold() in {"none", "n/a", "-", "—"}:
                    continue
                if node_id in cursor_ids:
                    report.error(f"Duplicate active cursor node: {node_id}")
                cursor_ids.add(node_id)
                if node_id not in registry_by_id:
                    report.error(f"Active cursor references unknown node: {node_id}")
                    continue
                cursor_state = row_value(state_by_id.get(node_id, {}), "state").casefold()
                if cursor_state not in {"planned", "ready", "active", "blocked"}:
                    report.error(f"Execution cursor points to node {node_id} whose state is not resumable")
                if relative_path(root, row_value(row, "active_node_file")) != registry_by_id[node_id]["path"]:
                    report.error(f"Active cursor file does not match node {node_id}")
            if len(cursor_ids) > 1:
                report.error("Linear execution has more than one cursor node")
            if len(active_ids) > 1:
                report.error("Linear execution has more than one active node")
            for node_id in sorted(active_ids - cursor_ids):
                report.error(f"Active node {node_id} is missing from the active cursor")
            if find_heading(
                index_text,
                ("parallel execution route", "parallel runtime route", "parallel execution", "parallelism"),
            ):
                report.error("OPERATING_INDEX.md contains a parallelism route without active parallelism")

        gate_body = section_body(master_text, ("gate decisions", "approval gates"))
        gate_headers, gate_rows = parse_markdown_table(gate_body)
        gate_by_id: dict[str, dict[str, str]] = {}
        if gate_headers:
            check_table_columns(
                report,
                "MASTER_PROGRESS.md gate decisions",
                gate_headers,
                ("gate_id", "gate_state"),
            )
            for value in sorted(duplicate_values(gate_rows, "gate_id")):
                report.error(f"Duplicate gate-decision row: {value}")
            for row in gate_rows:
                gate_id = row_value(row, "gate_id")
                if not gate_id:
                    continue
                gate_by_id[gate_id] = row
                gate_state = row_value(row, "gate_state").casefold()
                if gate_state not in GATE_STATES:
                    report.error(f"Gate {gate_id} has invalid gate state: {gate_state}")

        blocker_body = section_body(master_text, ("blockers",))
        _, blocker_rows = parse_markdown_table(blocker_body)
        blocker_ids = {
            row_value(row, "blocker_id")
            for row in blocker_rows
            if row_value(row, "blocker_id")
        }
        for value in sorted(duplicate_values(blocker_rows, "blocker_id")):
            report.error(f"Duplicate blocker row: {value}")
        for value in sorted(blocker_ids & set(gate_by_id)):
            report.error(f"Gate and blocker share an ambiguous name: {value}")
        for node_id, row in state_by_id.items():
            references = row_value(row, "blocker_ref").split(";")
            for value in references:
                reference = clean_cell(value)
                if reference.casefold() in {"", "none", "none currently", "n/a", "-", "—"}:
                    continue
                if reference in gate_by_id or reference in blocker_ids:
                    continue
                if re.fullmatch(r"G-\d+", reference):
                    report.error(f"Node {node_id} references unknown gate: {reference}")
                elif re.fullmatch(r"B-\d+", reference):
                    report.error(
                        f"Node {node_id} references unknown blocker: {reference}"
                    )
                else:
                    report.error(f"Node {node_id} references unknown blocker or gate: {reference}")

        edge_body = section_body(
            architecture_text, ("dependency and gate edges", "dependencies and gates")
        )
        _, edge_rows = parse_markdown_table(edge_body)
        approval_gate_ids = {
            row_value(row, "gate_id")
            for row in edge_rows
            if "approval" in normalize_label(
                row.get("Type", row.get("type", ""))
            )
        }
        approval_gate_ids.update(re.findall(r"\bG-\d+\b", edge_body))
        for gate_id in sorted(approval_gate_ids - set(gate_by_id)):
            report.error(f"Approval gate has no live decision row: {gate_id}")

    for parent_id, child_ids in children_by_parent.items():
        parent_state = row_value(state_by_id.get(parent_id, {}), "state").casefold()
        if parent_state != "done":
            continue
        nonterminal = [
            child_id
            for child_id in child_ids
            if row_value(state_by_id.get(child_id, {}), "state").casefold()
            not in TERMINAL_WORK_STATES
        ]
        if nonterminal:
            report.error(
                f"Complete parent {parent_id} has nonterminal children: {', '.join(nonterminal)}"
            )

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("setup_folder", help="Generated recursive setup folder to audit")
    args = parser.parse_args()

    root = Path(args.setup_folder).expanduser().resolve()
    report = audit(root)
    for warning in report.warnings:
        print(f"WARNING: {warning}")
    if report.errors:
        print(f"Audit failed for {root}")
        for error in report.errors:
            print(f"ERROR: {error}")
        return 1

    suffix = f" with {len(report.warnings)} warning(s)" if report.warnings else ""
    print(f"Audit passed for {root}{suffix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

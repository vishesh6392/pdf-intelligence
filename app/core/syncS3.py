import os
import json
import time
import threading
from app.storage.s3 import download_file

REGISTRY_PATH = "data/registry/documents.json"
TMP_REGISTRY_PATH = "data/registry/_remote.json"

# ✅ All lowercase, canonical states
STATE_PRIORITY = {
    "processing": 1,
    "ready": 2,
    "failed": 2,
}

# -------------------------------------------------------
# 🔵 Normalize status (CRITICAL)
# -------------------------------------------------------
def normalize_status(status: str) -> str:
    if not status:
        return "processing"
    return status.strip().lower()

# -------------------------------------------------------
# 🔵 Merge registry (NO rollback, NO KeyError)
# -------------------------------------------------------
def merge_registry(local: dict, remote: dict) -> dict:
    merged = local.copy()

    for doc_id, remote_doc in remote.items():
        local_doc = local.get(doc_id)

        # New document → accept
        if not local_doc:
            merged[doc_id] = remote_doc
            continue

        remote_status = normalize_status(remote_doc.get("status"))
        local_status = normalize_status(local_doc.get("status"))

        # Compare safely
        if STATE_PRIORITY.get(remote_status, 0) >= STATE_PRIORITY.get(local_status, 0):
            merged[doc_id] = remote_doc
        else:
            merged[doc_id] = local_doc  # prevent Ready → processing

    return merged

# -------------------------------------------------------
# 🔵 Initial sync (runs once at API startup)
# -------------------------------------------------------
def initial_sync():
    os.makedirs("data/registry", exist_ok=True)
    os.makedirs("data/index", exist_ok=True)

    try:
        download_file("registry/documents.json", TMP_REGISTRY_PATH)
        print("[SYNC] Registry downloaded (initial)")
    except Exception as e:
        print("[SYNC][WARN] No registry found yet:", e)
        return

    with open(TMP_REGISTRY_PATH, "r", encoding="utf-8") as f:
        remote = json.load(f)

    local = {}
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            local = json.load(f)

    merged = merge_registry(local, remote)

    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)

    # Download indexes for READY documents
    for doc_id, doc in merged.items():
        if normalize_status(doc.get("status")) == "ready":
            _download_index_safe(doc_id)

# -------------------------------------------------------
# 🔵 Safe index downloader (NEVER raises)
# -------------------------------------------------------
def _download_index_safe(doc_id: str):
    index_dir = f"data/index/{doc_id}"
    os.makedirs(index_dir, exist_ok=True)

    try:
        download_file(
            f"index/{doc_id}/faiss.index",
            f"{index_dir}/faiss.index"
        )
        download_file(
            f"index/{doc_id}/meta.json",
            f"{index_dir}/meta.json"
        )
        print(f"[SYNC] Index loaded for document {doc_id}")

    except Exception as e:
        print(f"[SYNC][WARN] Index not available yet for {doc_id}: {e}")

# -------------------------------------------------------
# 🔵 Periodic background sync (SAFE MERGE)
# -------------------------------------------------------
def periodic_sync(interval: int = 60):
    while True:
        try:
            download_file("registry/documents.json", TMP_REGISTRY_PATH)

            with open(TMP_REGISTRY_PATH, "r", encoding="utf-8") as f:
                remote = json.load(f)

            local = {}
            if os.path.exists(REGISTRY_PATH):
                with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                    local = json.load(f)

            merged = merge_registry(local, remote)

            with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
                json.dump(merged, f, indent=2)

            for doc_id, doc in merged.items():
                if normalize_status(doc.get("status")) != "ready":
                    continue

                local_index = f"data/index/{doc_id}/faiss.index"
                if os.path.exists(local_index):
                    continue

                print(f"[SYNC] New READY document detected: {doc_id}")
                _download_index_safe(doc_id)

        except Exception as e:
            print("[SYNC][WARN] Periodic sync error:", e)

        time.sleep(interval)

# -------------------------------------------------------
# 🟢 Public entry point
# -------------------------------------------------------
def start_background_sync():
    print("[SYNC] Starting background sync service")
    initial_sync()

    threading.Thread(
        target=periodic_sync,
        daemon=True
    ).start()

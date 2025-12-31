import os
import json
import time
import threading
from app.storage.s3 import download_file


# -------------------------------------------------------
# 🔵 Initial sync (runs once at API startup)
# -------------------------------------------------------
def initial_sync():
    os.makedirs("data/registry", exist_ok=True)
    os.makedirs("data/index", exist_ok=True)

    # 1️⃣ Download registry (best effort)
    try:
        download_file(
            "registry/documents.json",
            "data/registry/documents.json"
        )
        print("[SYNC] Registry downloaded")
    except Exception as e:
        print("[SYNC][WARN] No registry found yet:", e)
        return

    # 2️⃣ Load registry
    try:
        with open("data/registry/documents.json", "r", encoding="utf-8") as f:
            registry = json.load(f)
    except Exception as e:
        print("[SYNC][WARN] Failed to read registry:", e)
        return

    # 3️⃣ Download indexes for READY documents
    for doc_id, doc in registry.items():
        if doc.get("status") != "Ready":
            continue

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
        # VERY IMPORTANT:
        # Missing index must NEVER crash API
        print(f"[SYNC][WARN] Index not available yet for {doc_id}: {e}")


# -------------------------------------------------------
# 🔵 Periodic background sync (runs forever)
# -------------------------------------------------------
def periodic_sync(interval: int = 60):
    while True:
        try:
            # Refresh registry
            download_file(
                "registry/documents.json",
                "data/registry/documents.json"
            )

            with open("data/registry/documents.json", "r", encoding="utf-8") as f:
                registry = json.load(f)

            for doc_id, doc in registry.items():
                if doc.get("status") != "Ready":
                    continue

                local_index = f"data/index/{doc_id}/faiss.index"
                if os.path.exists(local_index):
                    continue  # already synced

                print(f"[SYNC] New READY document detected: {doc_id}")
                _download_index_safe(doc_id)

        except Exception as e:
            print("[SYNC][WARN] Periodic sync error:", e)

        time.sleep(interval)


# -------------------------------------------------------
# 🟢 Public entry point (called from FastAPI startup)
# -------------------------------------------------------
def start_background_sync():
    print("[SYNC] Starting background sync service")

    # Initial load (non-fatal)
    initial_sync()

    # Background polling thread
    threading.Thread(
        target=periodic_sync,
        daemon=True
    ).start()

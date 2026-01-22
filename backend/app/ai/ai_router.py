from app.services.transcript_store import get_room_logs


def merge_transcripts(room_name: str) -> str:
    users = get_room_logs(room_name)

    all_entries = []
    for speaker, logs in users.items():
        for log in logs:
            all_entries.append({
                "speaker": speaker,
                "text": log["text"],
                "timestamp": log["timestamp"]
            })

    # sort by time
    all_entries.sort(key=lambda x: x["timestamp"])

    merged = ""
    for e in all_entries:
        merged += f"[{e['timestamp']}] {e['speaker']}: {e['text']}\n"

    return merged

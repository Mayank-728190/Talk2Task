from typing import Dict, List

# TRANSCRIPTS[room_name][speaker_id] = [logs...]
TRANSCRIPTS: Dict[str, Dict[str, List[dict]]] = {}


def add_log(room_name: str, speaker_id: str, log: dict):
    if room_name not in TRANSCRIPTS:
        TRANSCRIPTS[room_name] = {}

    if speaker_id not in TRANSCRIPTS[room_name]:
        TRANSCRIPTS[room_name][speaker_id] = []

    TRANSCRIPTS[room_name][speaker_id].append(log)


def get_room_logs(room_name: str):
    return TRANSCRIPTS.get(room_name, {})


def get_user_logs(room_name: str, speaker_id: str):
    return TRANSCRIPTS.get(room_name, {}).get(speaker_id, [])

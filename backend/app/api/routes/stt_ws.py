import asyncio
import json
from datetime import datetime

import websockets
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.config import settings
from app.services.transcript_store import add_log

router = APIRouter()


def build_deepgram_url(lang: str):
    """
    Supported language modes:
    - en  => English
    - hi  => Hindi
    - hinglish => treated as Hindi (works best for mixed Hindi-English)
    """
    if lang == "hinglish":
        lang = "hi"

    return (
        "wss://api.deepgram.com/v1/listen"
        "?model=nova-2"
        f"&language={lang}"
        "&smart_format=true"
        "&punctuate=true"
        "&interim_results=true"
        "&encoding=opus"
        "&container=webm"
    )


@router.websocket("/ws/stt/{room_name}/{speaker_id}")
async def stt_websocket(websocket: WebSocket, room_name: str, speaker_id: str):
    await websocket.accept()

    if not settings.DEEPGRAM_API_KEY:
        await websocket.send_json({"error": "DEEPGRAM_API_KEY missing in backend .env"})
        await websocket.close()
        return

    # read language from query param
    lang = websocket.query_params.get("lang", "en")  # default English
    deepgram_url = build_deepgram_url(lang)

    dg_ws = None

    try:
        dg_ws = await websockets.connect(
            deepgram_url,
            additional_headers=[
                ("Authorization", f"Token {settings.DEEPGRAM_API_KEY}")
            ],
            ping_interval=20,
            ping_timeout=20,
        )

        async def deepgram_receiver():
            while True:
                msg = await dg_ws.recv()
                data = json.loads(msg)

                channel = data.get("channel")
                if not channel:
                    continue

                alt = channel.get("alternatives", [{}])[0]
                transcript = (alt.get("transcript") or "").strip()
                if transcript == "":
                    continue

                payload = {
                    "room": room_name,
                    "speaker_id": speaker_id,
                    "language_mode": lang,
                    "text": transcript,
                    "confidence": alt.get("confidence", 0),
                    "is_final": data.get("is_final", False),
                    "timestamp": datetime.utcnow().isoformat(),
                }

                # Store final logs only
                if payload["is_final"]:
                    add_log(room_name, speaker_id, payload)

                await websocket.send_text(json.dumps(payload))

        async def frontend_receiver():
            while True:
                audio_chunk = await websocket.receive_bytes()
                await dg_ws.send(audio_chunk)

        await asyncio.gather(deepgram_receiver(), frontend_receiver())

    except WebSocketDisconnect:
        print("Frontend disconnected STT websocket")

    except Exception as e:
        try:
            await websocket.send_json({"error": str(e)})
        except:
            pass

    finally:
        try:
            if dg_ws:
                await dg_ws.close()
        except:
            pass

        try:
            await websocket.close()
        except:
            pass

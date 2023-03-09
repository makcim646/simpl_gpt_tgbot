from fastapi import FastAPI
from stt import STT
import uvicorn

stt = STT()
app = FastAPI()


@app.get("/stt/{file}")
async def start(file):
    """Convers audio msg to txt and return txt"""
    file_path = f'voice\\{file}.oga'
    text = stt.audio_to_text(file_path)
    return {'text': text}


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)

    
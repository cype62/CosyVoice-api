import os
import sys
import argparse
import logging
import wave
from io import BytesIO
logging.getLogger('matplotlib').setLevel(logging.WARNING)
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('{}/../../..'.format(ROOT_DIR))
sys.path.append('{}/../../../third_party/Matcha-TTS'.format(ROOT_DIR))
from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav

app = FastAPI()

# Set cross-region allowance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Function to generate a WAV file from the model output
def generate_wav_data(model_output):
    wav_io = BytesIO()  # create an in-memory bytes buffer to store the wav file

    # Set parameters for WAV file
    with wave.open(wav_io, 'wb') as wav_file:
        n_channels = 1
        sampwidth = 2  # 16-bit audio, so 2 bytes per sample
        framerate = 22050  # Assuming 16kHz sample rate, modify if necessary
        wav_file.setnchannels(n_channels)
        wav_file.setsampwidth(sampwidth)
        wav_file.setframerate(framerate)

        # Write model output as WAV format
        for i in model_output:
            tts_audio = (i['tts_speech'].numpy() * (2 ** 15)).astype(np.int16).tobytes()
            wav_file.writeframes(tts_audio)  # Append audio frames to WAV

    wav_io.seek(0)  # Reset the buffer position to the beginning
    return wav_io


@app.get("/inference_sft")
async def inference_sft(tts_text: str = Form(), spk_id: str = Form()):
    model_output = cosyvoice.inference_sft(tts_text, spk_id)
    wav_data = generate_wav_data(model_output)
    return StreamingResponse(wav_data, media_type="audio/wav")


@app.get("/inference_zero_shot")
async def inference_zero_shot(tts_text: str = Form(), prompt_text: str = Form(), prompt_wav: UploadFile = File()):
    prompt_speech_16k = load_wav(prompt_wav.file, 16000)
    model_output = cosyvoice.inference_zero_shot(tts_text, prompt_text, prompt_speech_16k)
    wav_data = generate_wav_data(model_output)
    return StreamingResponse(wav_data, media_type="audio/wav")


@app.get("/inference_cross_lingual")
async def inference_cross_lingual(tts_text: str = Form(), prompt_wav: UploadFile = File()):
    prompt_speech_16k = load_wav(prompt_wav.file, 16000)
    model_output = cosyvoice.inference_cross_lingual(tts_text, prompt_speech_16k)
    wav_data = generate_wav_data(model_output)
    return StreamingResponse(wav_data, media_type="audio/wav")


@app.get("/inference_instruct")
async def inference_instruct(tts_text: str = Form(), spk_id: str = Form(), instruct_text: str = Form()):
    model_output = cosyvoice.inference_instruct(tts_text, spk_id, instruct_text)
    wav_data = generate_wav_data(model_output)
    return StreamingResponse(wav_data, media_type="audio/wav")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',
                        type=int,
                        default=50000)
    parser.add_argument('--model_dir',
                        type=str,
                        default='../../../pretrained_models/CosyVoice-300M',
                        help='local path or modelscope repo id')
    args = parser.parse_args()
    cosyvoice = CosyVoice(args.model_dir)
    uvicorn.run(app, host="0.0.0.0", port=args.port)

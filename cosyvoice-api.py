import io, os, sys
import argparse
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('{}/third_party/Matcha-TTS'.format(ROOT_DIR))
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

from flask import Flask, request, Response,send_from_directory
import torch

from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav
import torchaudio
import ffmpeg

from flask_cors import CORS
from flask import make_response

import json

app = Flask(__name__)

CORS(app, cors_allowed_origins="*")

CORS(app, supports_credentials=True)


@app.route("/", methods=['POST'])
def sft_post():
    question_data = request.get_json()

    text = question_data.get('text')
    speaker = question_data.get('speaker')
    streaming = question_data.get('streaming',0)

    speed = request.args.get('speed',1.0)
    speed = float(speed)
    

    if not text:
        return {"error": "文本不能为空"}, 400

    if not speaker:
        return {"error": "角色名不能为空"}, 400

    # 非流式
    if streaming == 0:

        buffer = io.BytesIO()

        tts_speeches = []

        for i, j in enumerate(cosyvoice.inference_sft(text,speaker,stream=False,speed=speed)):
            # torchaudio.save('sft_{}.wav'.format(i), j['tts_speech'], 22050)
            tts_speeches.append(j['tts_speech'])
        
        audio_data = torch.concat(tts_speeches, dim=1)
        torchaudio.save(buffer,audio_data, 22050, format="wav")
        buffer.seek(0)
        return Response(buffer.read(), mimetype="audio/wav")

    # 流式模式
    else:

        def generate():

            for i, j in enumerate(cosyvoice.inference_sft(text,speaker,stream=True,speed=speed)):

                tts_speeches = []
                buffer = io.BytesIO()
                tts_speeches.append(j['tts_speech'])
                audio_data = torch.concat(tts_speeches, dim=1)
                torchaudio.save(buffer,audio_data, 22050, format="ogg")
                buffer.seek(0)

                yield buffer.read()

        response = make_response(generate())
        response.headers['Content-Type'] = 'audio/ogg'
        response.headers['Content-Disposition'] = 'attachment; filename=sound.ogg'
        return response


@app.route("/", methods=['GET'])
def sft_get():

    text = request.args.get('text')
    speaker = request.args.get('speaker')
    new = request.args.get('new',0)
    streaming = request.args.get('streaming',0)
    speed = request.args.get('speed',1.0)
    speed = float(speed)

    if not text:
        return {"error": "文本不能为空"}, 400

    if not speaker:
        return {"error": "角色名不能为空"}, 400

    # 非流式
    if streaming == 0:

        buffer = io.BytesIO()

        tts_speeches = []

        for i, j in enumerate(cosyvoice.inference_sft(text,speaker,stream=False,speed=speed)):
            # torchaudio.save('sft_{}.wav'.format(i), j['tts_speech'], 22050)
            tts_speeches.append(j['tts_speech'])
        
        audio_data = torch.concat(tts_speeches, dim=1)
        torchaudio.save(buffer,audio_data, 22050, format="wav")
        buffer.seek(0)
        return Response(buffer.read(), mimetype="audio/wav")

    # 流式模式
    else:

        
        def generate():

            for i, j in enumerate(cosyvoice.inference_sft(text,speaker,stream=True,speed=speed)):

                tts_speeches = []
                buffer = io.BytesIO()
                tts_speeches.append(j['tts_speech'])
                audio_data = torch.concat(tts_speeches, dim=1)
                torchaudio.save(buffer,audio_data, 22050, format="ogg")
                buffer.seek(0)

                yield buffer.read()

        response = make_response(generate())
        response.headers['Content-Type'] = 'audio/ogg'
        response.headers['Content-Disposition'] = 'attachment; filename=sound.ogg'
        return response
        
        # return Response(generate(), mimetype='audio/x-wav')

                


@app.route("/inference_sft/", methods=['POST'])
def tts_to_audio():

    
    question_data = request.get_json()

    text = question_data.get('text')
    speaker = question_data.get('speaker')

    speed = question_data.get('speed')
    

    if not text:
        return {"error": "文本不能为空"}, 400

    if not speaker:
        return {"error": "角色名不能为空"}, 400

    buffer = io.BytesIO()

    tts_speeches = []

    for i, j in enumerate(cosyvoice.inference_sft(text,speaker,stream=False,speed=speed)):
        # torchaudio.save('sft_{}.wav'.format(i), j['tts_speech'], 22050)
        tts_speeches.append(j['tts_speech'])
    
    audio_data = torch.concat(tts_speeches, dim=1)
    torchaudio.save(buffer,audio_data, 22050, format="wav")
    buffer.seek(0)
    return Response(buffer.read(), mimetype="audio/wav")


@app.route("/speakers", methods=['GET'])
def speakers():

    return cosyvoice.list_avaliable_spks()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',
                        type=int,
                        default=50000)
    parser.add_argument('--model_dir',
                        type=str,
                        default='pretrained_models/CosyVoice-300M',
                        help='local path or modelscope repo id')
    args = parser.parse_args()

    cosyvoice = CosyVoice(args.model_dir)
    print("默认音色",cosyvoice.list_avaliable_spks())
    app.run(host='0.0.0.0', port=args.port)

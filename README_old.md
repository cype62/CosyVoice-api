## 安装依赖

确保安装了所有必需的 Python 包：

```pip install fastapi uvicorn numpy```
## 启动 FastAPI 服务器

在终端运行以下命令启动服务器：

```python server.py --port <端口号> --model_dir <模型目录路径>```
将 <端口号> 替换为你希望服务器监听的端口号。
将 <模型目录路径> 替换为你预训练的 CosyVoice 模型的路径。
### 示例：

```python server.py --port 50000 --model_dir ../../../pretrained_models/CosyVoice-300M```
访问API

服务器启动后，API 可通过 http://localhost:<端口号> 进行访问。

## API接口
### 1. /inference_sft
请求方法: GET
描述: 使用 Speaker Fine-Tuning（SFT）方法进行语音合成。
请求参数:

tts_text (表单数据, 必填): 要合成的文本。
spk_id (表单数据, 必填): 说话人的 ID。
响应: 返回一个 WAV 音频流（采样率为 22050 Hz）。

请求示例:

```curl -X GET "http://localhost:<端口号>/inference_sft" -F "tts_text=你好，世界" -F "spk_id=spk_001"```
### 2. /inference_zero_shot
请求方法: GET
描述: 进行零样本语音合成。
请求参数:

tts_text (表单数据, 必填): 要合成的文本。
prompt_text (表单数据, 必填): 提供的提示文本。
prompt_wav (表单数据, 必填): 提供的 WAV 音频文件（UploadFile 格式上传）。
响应: 返回一个 WAV 音频流（采样率为 22050 Hz）。

请求示例:

```
curl -X GET "http://localhost:<端口号>/inference_zero_shot" \
-F "tts_text=你好" \
-F "prompt_text=这是一个提示文本" \
-F "prompt_wav=@文件路径.wav"
```
### 3. /inference_cross_lingual
请求方法: GET
描述: 使用提示音频文件进行跨语言语音合成。
请求参数:

tts_text (表单数据, 必填): 要合成的文本。
prompt_wav (表单数据, 必填): 提供的 WAV 音频文件（UploadFile 格式上传）。
响应: 返回一个 WAV 音频流（采样率为 22050 Hz）。

请求示例:

```
curl -X GET "http://localhost:<端口号>/inference_cross_lingual" \
-F "tts_text=你好" \
-F "prompt_wav=@文件路径.wav"
```
### 4. /inference_instruct
请求方法: GET
描述: 提供指令文本进行语音合成。
请求参数:

tts_text (表单数据, 必填): 要合成的文本。
spk_id (表单数据, 必填): 说话人的 ID。
instruct_text (表单数据, 必填): 模型需要遵循的指令文本。
响应: 返回一个 WAV 音频流（采样率为 22050 Hz）。

请求示例:

```
curl -X GET "http://localhost:<端口号>/inference_instruct" \
-F "tts_text=请按照指令说话" \
-F "spk_id=spk_002" \
-F "instruct_text=用平静的语调说"
```
示例用法
/inference_sft 的 cURL 示例：

```
curl -X GET "http://localhost:50000/inference_sft" \
-F "tts_text=你好，世界" \
-F "spk_id=spk_001"
```
此请求将发送文本 "你好，世界" 并使用说话人 ID spk_001 进行合成，返回一个 WAV 文件。

/inference_zero_shot 的 Python 示例：
```
import requests

url = "http://localhost:50000/inference_zero_shot"
files = {'prompt_wav': open('path_to_wav_file.wav', 'rb')}
data = {
    'tts_text': '你好',
    'prompt_text': '示例提示'
}

response = requests.get(url, data=data, files=files)
with open('output.wav', 'wb') as f:
    f.write(response.content)
```
注意事项
音频输出: 输出音频为 WAV 格式，采样率为 22050 Hz。
错误处理: 请确保输入的 WAV 文件格式正确，并且采样率为 22050 Hz。
自定义模型目录: 启动服务器时，可以通过 --model_dir 参数指定模型目录。
该服务器使用 FastAPI 的 StreamingResponse 返回 WAV 音频数据，确保生成的语音文件能够被高效地返回和播放。

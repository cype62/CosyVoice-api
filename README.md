# 使用文档：cosyvoice-api.py
## 1. 简介
server_wav.py 是一个使用 Flask 构建的文本到语音（TTS）服务。该服务支持通过文本生成音频文件，并可以选择流式或非流式输出模式。该服务还允许用户根据不同的角色和语速生成语音。

注意：只提供了预训练的音色接口，支持参数：文案、角色、速度

## 2. 环境要求
Python 3.6 及以上
已安装以下 Python 库：
```
Flask
torch
torchaudio
ffmpeg-python
flask_cors
cosyvoice
```
您可以通过以下命令安装所需依赖项（假设您已经安装了 pip）：
```
pip install flask torch torchaudio ffmpeg-python flask-cors cosyvoice
```
## 3. 配置
在运行服务器之前，请确保您已经下载了所需的 TTS 模型，并指定模型路径。您可以通过命令行参数设置模型的路径。

## 4. 运行服务
要启动 Flask 服务器，请在终端中运行以下命令：
```
python server_wav.py --port 50000 --model_dir <YOUR_MODEL_PATH>
```
其中 --port 参数用于设置端口号，--model_dir 是您模型文件的路径。

## 5. 接口说明
### 5.1 / - POST 方法
该接口接收 JSON 数据并返回生成的音频。

请求示例：
```
{
    "text": "你好，这是一个测试语音。",
    "speaker": "speaker_name",
    "streaming": 0
}
```
响应：

如果成功，返回音频文件，内容类型为 audio/wav 或 audio/ogg（根据 streaming 参数）。
错误请求将返回相应的错误消息。
### 5.2 /tts_to_audio/ - POST 方法
此接口用于将文本、角色和速度转换为音频文件。
请求示例：
```
POST /tts_to_audio/
```

参数：
```
{
    "text": "欢迎使用语音合成服务。",
    "speaker": "speaker_name",
    "speed": 1.0
}
```
响应：

返回生成的音频文件，内容类型为 audio/wav。
错误请求将返回相应的错误消息。
### 5.3 /speakers - GET 方法
此接口返回可用的角色列表。

请求示例：

```
GET /speakers
```
响应：
```
{
    "available_speakers": ["speaker1", "speaker2", "..."]
}
```
### 5.4 / - GET 方法
此接口与 POST 方法类似，但接受 query parameters 作为输入。

请求示例：

```
GET /?text=你好&speaker=speaker_name&streaming=0
```
响应：
返回生成的音频文件，内容类型基于 streaming 参数。
错误请求将返回相应的错误消息。
## 6. 注意事项
确保输入文本和角色不为空。
音频生成可能会消耗一定的时间，尤其是在处理长文本时。
服务器默认绑定到 0.0.0.0，这意味着它将在所有可用IP上监听请求。
## 7. 示例请求
使用 curl 可模拟 POST 请求：

```
curl -X POST http://localhost:50000/ -H "Content-Type: application/json" -d '{"text":"你好","speaker":"speaker_name","streaming":0}'
```
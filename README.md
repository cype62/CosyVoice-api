CosyVoice API 接口使用文档
概述
CosyVoice API 提供了多种语音合成功能，包括基于输入文本的多发音人 TTS、跨语言语音合成、零样本语音合成等功能。该 API 通过 FastAPI 框架构建，使用了 CosyVoice 模型，并提供跨域请求支持。

本 API 服务的默认端口为 50000，如需修改，请在启动服务时指定 --port 参数。

基本设置
API根路径： /

返回格式： 所有语音合成接口均返回 audio/wav 格式的语音文件流。

接口说明
1. 语音合成（单发音人）- inference_sft
描述：
使用 CosyVoice 进行单发音人语音合成。传入文本和发音人 ID，生成对应语音。

请求方式：
GET /inference_sft

请求参数：
| 参数名 | 类型 | 说明 | | -------- | ------ | ------------------------- | | tts_text | Form | 合成语音的文本内容 | | spk_id | Form | 发音人 ID |

响应：
返回生成的 audio/wav 文件。

示例请求：
curl -X GET "http://localhost:50000/inference_sft" \
-F "tts_text=你好，世界" \
-F "spk_id=001"
2. 零样本语音合成 - inference_zero_shot
描述：
基于文本、提示语音文件（prompt_wav）以及提示文本，进行零样本语音合成。

请求方式：
GET /inference_zero_shot

请求参数：
| 参数名 | 类型 | 说明 | | ----------- | ---------- | ----------------------------- | | tts_text | Form | 合成语音的文本内容 | | prompt_text | Form | 提示文本（用于指导语音风格） | | prompt_wav | File | 提示语音文件，用于模仿该语音的发音风格 |

响应：
返回生成的 audio/wav 文件。

示例请求：
curl -X GET "http://localhost:50000/inference_zero_shot" \
-F "tts_text=你好，世界" \
-F "prompt_text=你好" \
-F "prompt_wav=@path_to_prompt_wav.wav"
3. 跨语言语音合成 - inference_cross_lingual
描述：
基于输入文本与提示语音文件，生成跨语言的合成语音。

请求方式：
GET /inference_cross_lingual

请求参数：
| 参数名 | 类型 | 说明 | | --------- | -------- | ------------------------- | | tts_text | Form | 合成语音的文本内容 | | prompt_wav | File | 提示语音文件（语音样本） |

响应：
返回生成的 audio/wav 文件。

示例请求：
curl -X GET "http://localhost:50000/inference_cross_lingual" \
-F "tts_text=你好，世界" \
-F "prompt_wav=@path_to_prompt_wav.wav"
4. 指令引导语音合成 - inference_instruct
描述：
基于输入的文本、发音人 ID 及指令文本生成合成语音，指令文本用于引导语音风格。

请求方式：
GET /inference_instruct

请求参数：
| 参数名 | 类型 | 说明 | | ------------ | ------- | ----------------------------- | | tts_text | Form | 合成语音的文本内容 | | spk_id | Form | 发音人 ID | | instruct_text | Form | 指令文本（用于指导语音风格） |

响应：
返回生成的 audio/wav 文件。

示例请求：
curl -X GET "http://localhost:50000/inference_instruct" \
-F "tts_text=你好，世界" \
-F "spk_id=001" \
-F "instruct_text=以温柔的语气说出"
启动服务
可以通过命令行运行以下命令来启动服务：

python server.py --port 50000 --model_dir ../../../pretrained_models/CosyVoice-300M
--port：设置服务器端口号，默认为 50000。
--model_dir：设置模型文件路径，默认路径为 ../../../pretrained_models/CosyVoice-300M。
注意事项
所有语音合成接口都返回 audio/wav 文件流。
请确保上传的音频文件为 .wav 格式，采样率为 16kHz，以确保模型处理的正确性。
CORS 跨域请求已允许。
如有问题，请参考 CosyVoice 项目的文档或联系开发团队。
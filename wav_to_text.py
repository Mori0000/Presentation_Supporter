import os
import io
from pydub import AudioSegment
from google.cloud import speech

# 環境変数にサービスアカウントのキーを設定
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './client.json'

# ステレオ音声をモノラルに変換
stereo_audio = AudioSegment.from_file("./test.wav")
mono_audio = stereo_audio.set_channels(1)
mono_audio.export("./test_mono.wav", format="wav")

# Google Cloud Speech-to-Text APIクライアントの作成
client = speech.SpeechClient()

# モノラル音声ファイルを読み込む
with io.open('./test_mono.wav', 'rb') as f:
    content = f.read()

# 音声データの設定
audio = speech.RecognitionAudio(content=content)

# 認識の設定
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    enable_automatic_punctuation=True,
    language_code='ja-JP'
)

# 音声を認識
response = client.recognize(config=config, audio=audio)

# 認識結果を表示
for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))

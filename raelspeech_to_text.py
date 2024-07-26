import os
import pyaudio
from google.cloud import speech
import queue
import threading

# 環境変数にサービスアカウントのキーを設定
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './client.json'

# 音声データを取得するための設定
RATE = 16000
CHUNK = int(RATE / 10)  # 100msごとのチャンクサイズ

# PyAudioのストリーム設定
pyaudio_instance = pyaudio.PyAudio()
stream = pyaudio_instance.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
    stream_callback=None
)

# 音声データを保持するキュー
audio_queue = queue.Queue()

# Google Cloud Speech-to-Text APIクライアントの作成
client = speech.SpeechClient()

# 音声認識の設定
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=RATE,
    language_code='ja-JP',
    enable_automatic_punctuation=True
)

streaming_config = speech.StreamingRecognitionConfig(
    config=config,
    interim_results=True
)

# 音声データをストリームで送信するジェネレーター
stop_flag = threading.Event()

def generate_audio_stream():
    while not stop_flag.is_set():
        data = audio_queue.get()
        if data is None:
            break
        yield speech.StreamingRecognizeRequest(audio_content=data)

# 音声ストリームからデータを取得してキューに入れるコールバック関数
def fill_audio_queue():
    while not stop_flag.is_set():
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_queue.put(data)

# 音声データを非同期で読み取るスレッドを開始
audio_thread = threading.Thread(target=fill_audio_queue)
audio_thread.start()

# キーワードリスト
stop_keywords = ["ストップ", "止まれ", "終わり"]

# 音声認識のストリームを開始
requests = generate_audio_stream()
responses = client.streaming_recognize(config=streaming_config, requests=requests)

# 認識結果をリアルタイムで表示し、キーワード検出をチェック
try:
    for response in responses:
        for result in response.results:
            transcript = result.alternatives[0].transcript
            print('Transcript: {}'.format(transcript))
            if any(keyword in transcript for keyword in stop_keywords):
                print("Stopping recognition as stop keyword was detected.")
                stop_flag.set()  # ストップフラグを設定
                audio_queue.put(None)  # ジェネレーターを停止
                break
except Exception as e:
    print(e)
finally:
    # スレッドが停止するのを待つ
    audio_thread.join()
    # ストリームを閉じる
    stream.stop_stream()
    stream.close()
    pyaudio_instance.terminate()

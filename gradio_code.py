import gradio as gr

def read_txt(file):
    # ファイルの内容を読み込む
    with open(file.name, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

# Gradioインターフェースの設定
interface = gr.Interface(
    fn=read_txt,  # テキストファイルの内容を表示する関数
    inputs=gr.File(file_types=['.txt']),  # 入力ウィジェット（TXTファイルのみ）
    outputs=gr.Textbox(lines=20, label="File Content")  # 出力ウィジェット（テキストボックス）
)

# インターフェースの実行
if __name__ == "__main__":
    interface.launch()

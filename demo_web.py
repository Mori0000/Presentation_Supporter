# import gradio as gr

# def read_file(file):
#     with open(file.name, "r", encoding="utf-8") as f:
#         content = f.read()
#     return content

# iface = gr.Interface(
#     fn=read_file, 
#     inputs=gr.inputs.File(type="file", label="Upload a text file"), 
#     outputs=gr.outputs.Textbox(label="File content")
# )

# iface.launch()

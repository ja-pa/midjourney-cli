import gradio as gr
import pandas as pd
import json
from midjourneycli import Midjourney


def load_config(config_file="config.json"):
    print("Loading config from " + config_file)
    with open(config_file, 'r') as f:
        config = json.load(f)
        return config["CHANNEL_ID"], config["SERVER_ID"], config["SALAI_TOKEN"], config["MIDJOURNEY_SESSION_TOKEN"], config["MIDJOURNEY_USER_ID"]


def load_html_article(file_path="article.html"):
    with open(file_path, 'r') as f:
        html = f.read()
        return html
    
# Function to display the custom table
def display_table(prompt="", single_line=False, prompt_start="", prompt_end="",prompt_variant="", midjourney_version=""):
    prompt_all=[]
    if prompt_variant == "":
        prompt_variant = "\n"
    
    for variant in prompt_variant.splitlines():
        prompt_all.append( "%s %s %s %s" % (prompt, prompt_start, variant, midjourney_version))
        print(prompt_all)
        #prompt_all = "%s %s %s %s" % (prompt, prompt_start, prompt_end, midjourney_version)
        
    CHANNEL_ID, SERVER_ID, SALAI_TOKEN, MIDJOURNEY_SESSION_TOKEN, MIDJOURNEY_USER_ID = load_config("config.json")
    mj_obj=Midjourney(CHANNEL_ID, SERVER_ID, SALAI_TOKEN, MIDJOURNEY_SESSION_TOKEN, MIDJOURNEY_USER_ID)
    #mj_obj.set_prompt(prompt_all)
    mj_obj.send_prompt_list(prompt_all,False,"","")
    
    return prompt_all




# Define the Gradio interface
iface = gr.Interface(
    fn=display_table,
    inputs=[
        gr.inputs.Textbox(lines=3, label="Prompt:"),
        gr.Checkbox(label="Prompts on single line", info="Every prompt is on a single line."),
        gr.inputs.Textbox(lines=1, label="Prompt start"),
        gr.inputs.Textbox(lines=1, label="Prompt end"),
        gr.inputs.Textbox(lines=3, label="Prompt Variant"),
        gr.Dropdown(
            ["--v 5", "--v 4", "--v 3"], value="--v 5", multiselect=False, label="Midjourney version", info="Version of midjourney engine."
        ),
    ],
    outputs="text",
    title="Midjourney Prompt Generator",
    description="Midjourney Prompt Generator",
    article=load_html_article("article.html"),
    examples=[
        [None, None, None, None, "by Arthur Adams"],
        [None, None, None, None, "by Neal Adams"],
        [None, None, None, None, "by Charles Addams"],
        [None, None, None, None, "by Benchmark"],
        [None, None, None, None, "by Mattias Adolfsson"],
        [None, None, None, None, "by Alena Aenami"],
    ],
)

# Launch the Gradio app
iface.launch()

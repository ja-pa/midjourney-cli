import time
import requests
import argparse
import json


CHANNEL_ID=""
SERVER_ID=""
SALAI_TOKEN=""


def load_config(config_file="config.json"):
    with open(config_file, 'r') as f:
        config = json.load(f)
        return config["CHANNEL_ID"], config["SERVER_ID"], config["SALAI_TOKEN"]


def check_blacklist(text : str):
	pass


def PassPromptToSelfBot(prompt : str):
    payload ={"type":2,
    "application_id":"936929561302675456",
    "guild_id":SERVER_ID,
    "channel_id":CHANNEL_ID,
    "session_id":"0a010c9eaf31b12c8b2345c0d38bbb7c",
    "data":{"version":"994261739745050686",
            "id":"938956540159881230",
            "name":"imagine",
            "type":1,
            "options":[{"type":3,"name":"prompt","value":prompt}],
            "application_command":{"id":"938956540159881230",
                                "application_id":"936929561302675456",
                                "version":"994261739745050686",
                                "default_permission":True,
                                "default_member_permissions":None,
                                "type":1,
                                "name":"imagine",
                                "description":"There are endless possibilities...",
                                "dm_permission":True,
                                "options":[{"type":3,"name":"prompt","description":"The prompt to imagine","required":True}]},
                                "attachments":[]}}
    header = {
        'authorization' : SALAI_TOKEN
    }
    response = requests.post("https://discord.com/api/v9/interactions",
    json = payload, headers = header)
    return response


def send_prompt_to_midjourney(prompt_list: list,test: bool,prompt_start: str,prompt_end: str):
	for i in prompt_list:
		prompt_text=prompt_start+i+prompt_end
		print("Prompt: ",prompt_text)
		if test == False:
			response = PassPromptToSelfBot(prompt_text)
			if response.status_code >= 400:
				print("Request has failed; please try later")
			else:
				print("Your prompt image is being prepared, please wait a moment...")
		time.sleep(3)



parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Path to input file with prompts")
parser.add_argument("-t", "--text-prompt", help="Input with prompts.")
parser.add_argument("-c", "--config", help="Load config file.")
parser.add_argument("-s", "--prompt-start",default="", help="Start all prompts with this text.")
parser.add_argument("-e", "--prompt-end",default="", help="End all prompts with this text.")
parser.add_argument("--test-mode",action='store_true',default=False, help="enable test mode")



args = parser.parse_args()

if args.config:
    CHANNEL_ID, SERVER_ID, SALAI_TOKEN = load_config(args.config)
else:
    CHANNEL_ID, SERVER_ID, SALAI_TOKEN = load_config("config.json")

if args.file:
    with open(args.file, 'r') as f:
        send_prompt_to_midjourney(f.readlines())
elif args.text_prompt:
    input_text = args.text_prompt
    send_prompt_to_midjourney([input_text],args.test_mode,args.prompt_start,args.prompt_end)
else:
    parser.error("Please provide either a file or text input")

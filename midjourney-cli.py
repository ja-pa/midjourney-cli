import time
import requests
import argparse
import json
import os


CHANNEL_ID = ""
SERVER_ID = ""
SALAI_TOKEN = ""
MIDJOURNEY_SESSION_TOKEN = ""
MIDJOURNEY_USER_ID = ""


def load_config(config_file="config.json"):
    with open(config_file, 'r') as f:
        config = json.load(f)
        return config["CHANNEL_ID"], config["SERVER_ID"], config["SALAI_TOKEN"], config["MIDJOURNEY_SESSION_TOKEN"], config["MIDJOURNEY_USER_ID"]


def check_blacklist(text: str):
    pass


def download_image(url, save_as=None):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_as, 'wb') if save_as else None as f:
            f.write(response.content)
    else:
        print(f"Failed to download image from URL: {url}")


class Midjourney:
    def __init__(self, CHANNEL_ID, SERVER_ID, SALAI_TOKEN, MIDJOURNEY_SESSION_TOKEN, USER_ID):
        self.__CHANNEL_ID = CHANNEL_ID
        self.__SERVER_ID = SERVER_ID
        self.__SALAI_TOKEN = SALAI_TOKEN
        self.__MIDJOURNEY_SESSION_TOKEN = MIDJOURNEY_SESSION_TOKEN
        self.__USER_ID = USER_ID
        print("AAAAAAAAAAAAAAAAAAAAAAA", self.__USER_ID)

    def get_generated_images_json(self, list_upscales: bool):
        headers = {
            "User-Agent": 'Midjourney-history-sync/1.0',
            "Cookie": "__Secure-next-auth.session-token=" + self.__MIDJOURNEY_SESSION_TOKEN,
            "Content-Type": "application/json"
        }
        url = ""
        if list_upscales:
            url = "https://www.midjourney.com/api/app/recent-jobs/?orderBy=new&jobType=upscale&jobStatus=completed&userId=" + \
                self.__USER_ID + "&dedupe=true&refreshApi=0"
        else:
            url = "https://www.midjourney.com/api/app/recent-jobs/?orderBy=new&jobStatus=completed&userId=" + \
                self.__USER_ID + "&dedupe=true&refreshApi=0"

        response = requests.get(url, headers=headers, verify=True)
        # print(response.content)
        return json.loads(response.content)

    def __generate_prompt(self, prompt: str):
        payload = {"type": 2,
                   "application_id": "936929561302675456",
                   "guild_id": self.__SERVER_ID,
                   "channel_id": self.__CHANNEL_ID,
                   "session_id": "0a010c9eaf31b12c8b2345c0d38bbb7c",
                   "data": {"version": "994261739745050686",
                            "id": "938956540159881230",
                            "name": "imagine",
                            "type": 1,
                            "options": [{"type": 3, "name": "prompt", "value": prompt}],
                            "application_command": {"id": "938956540159881230",
                                                    "application_id": "936929561302675456",
                                                    "version": "994261739745050686",
                                                    "default_permission": True,
                                                    "default_member_permissions": None,
                                                    "type": 1,
                                                    "name": "imagine",
                                                    "description": "There are endless possibilities...",
                                                    "dm_permission": True,
                                                    "options": [{"type": 3, "name": "prompt", "description": "The prompt to imagine", "required": True}]},
                            "attachments": []}}
        header = {
            'authorization': self.__SALAI_TOKEN
        }
        response = requests.post("https://discord.com/api/v9/interactions",
                                 json=payload, headers=header)
        return response

    def get_upscale(self, index: int, messageId: str, messageHash: str):
        payload = {"type": 3,
                   "guild_id": self.__SERVER_ID,
                   "channel_id": self.__CHANNEL_ID,
                   "message_flags": 0,
                   "message_id": messageId,
                   "application_id": "936929561302675456",
                   "session_id": "45bc04dd4da37141a5f73dfbfaf5bdcf",
                   "data": {"component_type": 2,
                            "custom_id": "MJ::JOB::upsample::{}::{}".format(index, messageHash)}
                   }
        header = {
            'authorization': self.__SALAI_TOKEN
        }
        response = requests.post("https://discord.com/api/v9/interactions",
                                 json=payload, headers=header)
        return response

    def send_prompt_list(self, prompt_list: list, test: bool, prompt_start: str, prompt_end: str):
        for i in prompt_list:
            prompt_text = prompt_start+i+prompt_end
            print("Prompt: ", prompt_text)
            if test == False:
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                response = self.__generate_prompt(prompt_text)
                if response.status_code >= 400:
                    print("Request has failed; please try later")
                else:
                    print(
                        "Your prompt image is being prepared, please wait a moment...")
            time.sleep(3)


def print_images(mj_json, max_prompts=10, download=False, download_path=""):
    y = 0
    for i in mj_json:
        y = y+1
        # print(i,"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print("")
        print("Prompt:\n%s" % i["full_command"])
        timestamp = i["enqueue_time"].split()[0].replace("-", "_")
        target_hash = i["id"]
        target_id = i["platform_message_id"]
        index_i = 0
        for image_url in i["image_paths"]:
            image_name = os.path.basename(image_url)
            save_name = i["prompt"].replace(
                "  ", " ").replace(" ", "_").lower()
            full_name = "%s_%s_%s" % (timestamp, save_name, image_name)
            if download:
                download_image(image_url, download_path+full_name)
            print(index_i, full_name)
            print(" ", image_url)
            index_i = index_i + 1
        print("")
        print("target_hash", target_hash)
        print("target_id", target_id)

        if y >= max_prompts:
            break


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-f", "--file", help="Path to input file with prompts")
group.add_argument("-j", "--json-file",
                   help="Path to input json file with prompts")
group.add_argument("-t", "--text-prompt", help="Input with prompts.")
parser.add_argument("-c", "--config", help="Load config file.")
parser.add_argument("-s", "--prompt-start", default="",
                    help="Start all prompts with this text.")
parser.add_argument("-e", "--prompt-end", default="",
                    help="End all prompts with this text.")
parser.add_argument("-d", "--download-images", nargs='?', type=str,
                    const="NO_PATH_GIVEN", help="Download images to selected directory.")
group.add_argument("-l", "--list-images", type=int, const=10,
                   nargs='?', help="List images from midjourney page.")
parser.add_argument("--list-upscales", action='store_true',
                    default=False, help="List only upscales.")


parser.add_argument("-u", "--upscale",  action='store', nargs=3,
                    help="Upscales image. Takes <index> <target_hash> <target_id>")


parser.add_argument("--test-mode", action='store_true',
                    default=False, help="enable test mode")


args = parser.parse_args()

if args.config:
    CHANNEL_ID, SERVER_ID, SALAI_TOKEN, MIDJOURNEY_SESSION_TOKEN, MIDJOURNEY_USER_ID = load_config(
        args.config)
else:
    CHANNEL_ID, SERVER_ID, SALAI_TOKEN, MIDJOURNEY_SESSION_TOKEN, MIDJOURNEY_USER_ID = load_config(
        "config.json")

mj_obj = Midjourney(CHANNEL_ID, SERVER_ID, SALAI_TOKEN,
                    MIDJOURNEY_SESSION_TOKEN, MIDJOURNEY_USER_ID)

if args.list_images:
    midjourney_json = mj_obj.get_generated_images_json(
        list_upscales=args.list_upscales)
    download_path = ""
    download_bool = False
    if args.download_images:
        if 'NO_PATH_GIVEN' in args.download_images:
            download_path = ""
            download_bool = True
        elif os.path.isdir(args.download_images):
            download_path = args.download_images
            download_bool = True
        else:
            download_path = ""
            download_bool = False
            print("Error! Wrong path. Images can't be downloaded. ")
    print_images(midjourney_json, args.list_images,
                 download_bool, download_path)

if args.upscale:
    print("upsacale aaaaaaaaaaaaa")
    up_index, up_target_id, up_target_hash = args.upscale
    print(up_index, up_target_id, up_target_hash)
    ret = mj_obj.get_upscale(up_index, up_target_id, up_target_hash)
    print(ret)

if args.file:
    with open(args.file, 'r') as f:
        mj_obj.send_prompt_to_midjourney(
            f.readlines(), args.test_mode, args.prompt_start, args.prompt_end)
        # send_prompt_to_midjourney(
        #    f.readlines(), args.test_mode, args.prompt_start, args.prompt_end)

if args.text_prompt:
    input_text = args.text_prompt
    mj_obj.send_prompt_list(
        [input_text], args.test_mode, args.prompt_start, args.prompt_end)
    # send_prompt_to_midjourney(
    #    [input_text], args.test_mode, args.prompt_start, args.prompt_end)

if args.json_file:
    prompt_list = []
    with open(args.json_file) as fp:
        json_obj = json.load(fp)
        for item in json_obj:
            print(item)
            prompt_list.append(item["prompt"])
    # print(prompt_list)
    mj_obj.send_prompt_to_midjourney(
        prompt_list, args.test_mode, args.prompt_start, args.prompt_end)

# else:
#    parser.error("Please provide either a file or text input")

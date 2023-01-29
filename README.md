# midjourney-cli

This script allows users to send prompt to midjourney from cli interface.

## Config

The following variables must be set in a **config.json** file or passed as an argument to the script:
* CHANNEL_ID: ID of the Discord channel where the bot will send the prompt
* SERVER_ID: ID of the Discord server where the bot will send the prompt
* SALAI_TOKEN: Token of user which paid for midjourney subscription

## Usage

The script can be run with the following arguments:
* -f or --file: Path to a file containing prompts, one per line
* -t or --text-prompt: A single prompt passed as a string
* -c or --config: Path to a config file If no config file is provided, the script will look for a file called config.json in the same directory.

*  -h, --help            show this help message and exit
*  -f FILE, --file FILE  Path to input file with prompts
*  -t TEXT_PROMPT, --text-prompt TEXT_PROMPT Input with prompts.
*  -c CONFIG, --config CONFIG Load config file.
*  -s PROMPT_START, --prompt-start PROMPT_START Start all prompts with this text.
*  -e PROMPT_END, --prompt-end PROMPT_END End all prompts with this text.
*  --test-mode           enable test mode

### Command examples:

Text input:

``$ python midjourney-cli.py -t "big rabbit smoking cigar --v 4"``

Test mode on (Doesn't send anything to discord)

``$ python midjourney-cli.py -t "big rabbit smoking cigar --v 4" --test-mode`` 

## Note

This script is using a selfbot which is a violation of discord API use case policy, it is not recommended to use selfbot in your application.

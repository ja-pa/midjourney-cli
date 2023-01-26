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


Command usage:

``$ python midjourney-cli.py -t "big rabbit smoking cigar --v 4"``


## Note

This script is using a selfbot which is a violation of discord API use case policy, it is not recommended to use selfbot in your application.

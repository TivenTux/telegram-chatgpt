## Telegram ChatGPT Bot
Simple telegram bot that uses chatGPT or hosted LLM.

Get chatGPT api key here: https://platform.openai.com/account/api-keys

If you use chatgpt, you do not need to edit anything on locally hosted LLM settings.

Set ENV variables:  

**aiselection** - set 1 for openAI or 2 for custom api <br>
**openaikey** - your openAI api key here <br> 
**aihost** - set host for self hosted LLM 'ip:port'. Ignore if you're using chatgpt. <br>
**TELEGRAM_BOT_TOKEN** - Telegram bot token <br> 
**bot_nickname** - Bot's name <br> 
**bot_keyword** - Keyword which the bot will respond to. Usually same with its name. <br> 
**pass_author** - Option to give the user's first name to the bot. Enable with 1, disable with 0. <br> 


### pip install

```
telebotapi, openai

```

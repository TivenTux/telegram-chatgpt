## Telegram ChatGPT Bot
Simple telegram bot that uses chatGPT or hosted LLM.

Get chatGPT api key here: https://platform.openai.com/account/api-keys

### Environment Variables  

| Environment Variable             | Description                                                                         |
|----------------------------------|-------------------------------------------------------------------------------------|
| `openaikey`                      | Your openAI api key (https://platform.openai.com/account/api-keys)                  |
| `telegram_bot_token`             | The api token of your telegram bot.  (https://core.telegram.org/bots)               |
| `bot_nickname`                   | Set the bot's name.                                                                 |
| `bot_keyword`                    | Keyword which the bot will respond to. Usually same with its name.                  |
| `pass_author`                    | Option to give the user's first name to the bot. Enable with 1, disable with 0. Default enabled.   

You can specify these environment variables when starting the container using the `-e` command-line option as documented
[here](https://docs.docker.com/engine/reference/run/#env-environment-variables):
```bash
docker run -e "openaikey=yy"
```

### Building the container

After having cloned this repository, you can run
```bash
docker build -t telegram-chatgpt .
```

### Running the container

```bash
docker run -d -e "openaikey=yyy" -e "telegram_bot_token=yyy" -e "bot_nickname=yyy" -e "bot_keyword=yyy" telegram-chatgpt

```

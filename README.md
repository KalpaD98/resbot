# Restaurant Bot

## Instructions

*Make sure you have set up the Rasa on your system or server.*

### Integration

- Step 1: Since this Chat UI communicates with the Rasa server using `rest` channel, make sure you have added `rest`
  channel in the `credentials.yml` file
- Once you have developed your bot and you are ready to integrate the bot with the UI, you can start the Rasa server
  using the below command

Rasa run

```
rasa run -m models --enable-api --cors "*" --debug
```

Run action server

```
rasa run actions --cors "*" --debug
```
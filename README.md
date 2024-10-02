<h1 align="center">
    Test Checker Bot
</h1>
An aiogram bot to organize public tests and get top scorers using an easily understandble and scalable template.

## About
Makes use of different handlers, filters, states, keyboards and more. Database is done with sqlite3 standard library. Always require admin and user to confirm their action to prevent accidental sending of answers. Keeps the track of past sent answers, so if user tries to resend their answer second time, it will not allow it. You can create, delete a test and see the answers of the bot as well as see the top scorers.

## How to setup your own bot:
To create your own, you need, first, to create a bot at BotFather. After creating it, you will need to put its `TOKEN` to `config.py` file on `data` folder. Replace `API_TOKEN` with your bot's `TOKEN` given by BotFather, `ADMIN_ID` with your user id.

## Working example:
A working bot of mine - [Not here yet](https://nothere)
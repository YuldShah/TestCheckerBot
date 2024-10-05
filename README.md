<h1 align="center">
    Test Checker Bot
</h1>
An aiogram bot to organize public tests and get top scorers using an easily understandble and scalable template.

## About
Makes use of different handlers, filters, states, keyboards and more. Database is done with sqlite3 standard library. Always require admin and user to confirm their action to prevent accidental sending of answers. Keeps the track of past sent answers, so if user tries to resend their answer second time, it will not allow it. You can create, end and archive a test and see the answers of the test as well as see the top scorers.

##Help
Commands available and their functions:
	/check - Check your answers for a test
	/results - Check your results over the tests

###The format to follow while sending answers at once:
<code>
first answer
second answer
third answer
...</code>

## How to setup your own bot:
To create your own, you need, first, to create a bot at BotFather. After creating it, you will need to put its `TOKEN` to `config.py` file on `data` folder. Replace `API_TOKEN` with your bot's `TOKEN` given by BotFather, update the list `ADMINS`, inserting your own user id.

## Working example:
A working bot of mine - [iTestCheck Bot](https://itestcheck_bot)
﻿<h1 align="center">
    Test Checker Bot
</h1>
An aiogram bot to organize public tests and get top scorers using an easily understandble and scalable template.

## About

Makes use of different handlers, filters, states, keyboards and more. Database is done with sqlite3 standard library. Always require admin and user to confirm their action to prevent accidental sending of answers. Keeps the track of past sent answers, so if user tries to resend their answer second time, it will not allow it. You can create, end and archive a test and see the answers of the test as well as see the top scorers.

## Help

Commands available and their functions:
	`/check` - Check your answers for a test
	`/results` - Check your results over the tests

## How to setup your own bot:

To create your own, you need, first, to create a bot at BotFather. After creating it, you will need to put its `TOKEN` to `config.py` file on `data` folder. Replace `API_TOKEN` with your bot's `TOKEN` given by BotFather, update the list `ADMINS`, inserting your own user id.

## User experience & brief look at the bot

You can use the bot as an admin and a user

### Admin mode

When `config.py` has your telegram id in `ADMINS` list, you will be able to use the bot in Admin mode. When you press `/start`, this will be the response by the bot:
![image](https://github.com/user-attachments/assets/ec2378d7-2234-40c5-a4a9-5f59653fcc60)

### Creating a test

First you will need to choose a title for your test
![image](https://github.com/user-attachments/assets/40667a7c-7c6a-4523-99e9-8f9d4eba636d)

I made it you can skip the description because it is not that necessary
![image](https://github.com/user-attachments/assets/777eb79f-397e-427a-93ff-211ead6a533f)

But you can't skip without giving the number of questions, logical
![image](https://github.com/user-attachments/assets/0e742f38-c0c8-48a2-bfdd-831bc0901f7a)

Now you can choose either way to enter the correct solutions:
![image](https://github.com/user-attachments/assets/3740b4d1-deee-4a74-8502-2113664bd1ce)

### The format to follow while sending answers at once:

<code>first answer
second answer
third answer
...</code>

With one-by-one method of entering, you can safely store the answers
![image](https://github.com/user-attachments/assets/14b4bbe0-c322-437a-8106-c1485e9f0f28)

I made sure user will always have the choice to go back to last step if anything goes wrong, providing ease to user

After everything, bot needs to make sure to have confirmation from user
![image](https://github.com/user-attachments/assets/8a7fd265-bd0b-427e-b4e2-35a298b606e6)

After confirmation, you will be brought to main menu

### Running tests

You can check the running tests
![image](https://github.com/user-attachments/assets/f87baf35-b343-4047-b6cc-a07192b98634)

As you can see, user will have the options
- To see the results
- To see the answers
- Edit the title and description
- Share the test (I will cover more about that later)
- End the test and archive it

I decided to stop for sharing the test because it was a good idea, even if it is simple
![image](https://github.com/user-attachments/assets/a5eaa043-cfd4-4917-9819-5aa90119be1c)

It generates 6-character code, so that no unauthorized users will be able to answer for tests, creating further privacy

The way archive works is simple, providing all the tests that have been archived
![image](https://github.com/user-attachments/assets/152edb0a-2af0-43ef-9f7c-789a54f846ac)

Pressing help will provide this message
![image](https://github.com/user-attachments/assets/8bb934d9-caaa-41c5-a85a-490065aba5fa)

You can also see the stats of the bot
![image](https://github.com/user-attachments/assets/be7ce6f9-5ade-494e-b7cb-247acf7e6158)

### User mode
When you start the bot, you will find this
![image](https://github.com/user-attachments/assets/11498367-d294-414b-a3d4-7416350105b8)

You can participate in a test, providing the bot with the special code 
![image](https://github.com/user-attachments/assets/43755c52-d4ca-430d-9794-af708ba2cc12)

After you enter the answers, you will get the results
![image](https://github.com/user-attachments/assets/5d61d693-fb57-402d-82e4-68e233dca2ac)

If you were to enter the code of a test you have already participated, bot will not let you
![image](https://github.com/user-attachments/assets/60dc45e8-ec31-4821-9c3b-339a31c41108)

With the results section, you can look at the results of your tests
![image](https://github.com/user-attachments/assets/3fb135c0-11f3-4799-b4a3-343638d16310)

You can also enter the code of the test you want to know the results of

This is what you get as a user when you press help
![image](https://github.com/user-attachments/assets/4ad2f37e-4213-4c5d-a9d1-4c20f9a89d62)

## Working example:

A working bot of mine - [iTestCheck Bot](https://itestcheck_bot)

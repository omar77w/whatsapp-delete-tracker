### Tired of people deleting their WhatsApp messages? Want to know what they wrote?

This Python program detects message deletions in your WhatsApp conversations and provides you with a copy of the deleted message(s).
This is done by continously tracking (using the Selenium library) and storing your recent WhatsApp messages—all locally. The program works on WhatsApp's web client (https://web.whatsapp.com) using Mozilla Firefox or Google Chrome.

There are two files:
- **Single_convo.py**:  tracks and detects deletions in one conversation of your choosing. The program will prompt you to choose the conversation.
- **Multiple_convos.py**:  automatically tracks and detects deletions in your most recent 19 conversations.



Known limitations:
- Multiple_convos.py currently does not support conversation names with apostrophes in them. It is advised to rename or archive said conversations while running it.
- The program currently only works on text messages and is unable to detect photo deletions.
- Using the program results in sending "Read receipts" (two blue checkmarks). This is not an issue for those with "Read receipts" disabled in WhatsApp settings.

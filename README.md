Tired of people deleting their WhatsApp messages?

This Python program uses the Selenium library to detect message deletions in your WhatsApp and provide you with a copy of the deleted message.
This is done by continously tracking and storing your recent WhatsApp messages, all locally. The program works on WhatsApp's web client (https://web.whatsapp.com) using Firefox. Chrome can be used instead with a switch of one line in the code.

Known limitations:
- The program currently does not support conversation names with apostrophes in them. It is advised to archive or rename such conversations while running it.
- The program currently only works on text messages and is unable to detect photo deletions.

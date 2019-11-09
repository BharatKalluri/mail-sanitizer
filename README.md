# Mail sanitizer

## The idea
If you signup to a lot of websites to get a peek into the product or get on a trail. Then your mail box probably has several thousands of emails.
The idea of this tool is to analyze emails, find and unsubscribe link and open it. Also show you who has polluted your email the most etc..

### This is still very much WIP, hopefully it will be complete soon

### How to use

> mail-sanatizer create-dump

will create A mail dump file in your home directory called .mail_dump

> mail-sanatizer sanatize

starts a series of questions, the questions will be in the form of 

```bash
 You have recieved 300 emails from xxx@xxx.com, do you want to delete all these emails?
 y
 We also found an unsubscribe link, do you want to unsubscribe?
 y
 Please click https://<irriatating_website>.com/unsub/random_string
 You have recieved 234 emails from yyy@yyy.com, do you want to delete all these emails?
 ....
```

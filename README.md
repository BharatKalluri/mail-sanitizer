# Mail sanitizer

## The idea

If you signup to a lot of websites to get a peek into the product or get on a trial. Then your mail box probably has several thousands of emails.
The idea of this tool is to analyze emails, find and unsubscribe link and open it. Also show you who has polluted your email the most etc..

### One time setup

- Go [here](https://developers.google.com/gmail/api/quickstart/python) and click on Enable Gmail API

- Click on Download client configuration and copy the file over to ~/.config/mail-sanitizer/credentials.json

- Create a file called config.yaml in the same directory with the following contents

```yaml
email: <your email here>
```

### Usage

`mail-sanatizer collect`: Will create a mail dump for the sanitizer to operate on

`mail-sanatizer sanitize`: starts a series of questions, the questions will be in the form of

```bash
 You have recieved 300 emails from xxx@xxx.com, do you want to delete all these emails?
 y
 You have recieved 234 emails from yyy@yyy.com, do you want to delete all these emails?
 ....
```

Feel free to file issues if you face any problems or add suggestions in the github issues.
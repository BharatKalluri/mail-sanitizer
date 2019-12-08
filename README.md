<h1 align="center">Mail sanitizer</h1>

<a href="https://asciinema.org/a/282456" target="_blank"><img src="https://asciinema.org/a/282456.svg" /></a>


## Tell me what it does!

If you signup to a lot of websites to get a peek into the product or get on a trial. Then your mail box probably has several thousands of emails.
This tool will get all your emails, store it locally and let's you delete emails in bulk by sender and provide un-subscribe links if it finds any.

## Install

```bash
pip3 install --user mail-sanitizer
```

## One time setup

- Go [here](https://developers.google.com/gmail/api/quickstart/python) and click on Enable Gmail API

- Click on Download client configuration

- Create the configuration directory and copy the config.json to this directory

```shell script
mkdir -p ~/.config/mail-sanitizer
cp ~/Downloads/config.json ~/.config/mail-sanitizer
```


## Usage

- Run `mail-sanitizer sanitize`

> Note: During authorization, you will get a screen saying `This app isn't verified`, click `Advanced` here and click on `Go to Quickstart (unsafe)`

Feel free to file issues if you face any problems or add suggestions in the github issues.
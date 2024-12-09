# AI Newsletter Generator: DS 3850 Quarterly Assessment 4

For the final project in DS 3850, we were tasked with writing a Python app that collects news from an API, passes it into OpenAI's API to summarize each article, and email the summaries as a newsletter to a given email.

## Running the Project on your Machine

First, clone the github repository. Then run the following commands:

```bash
cd /path/to/proj/directory/
python3 -m venv .venv
```

```bash
pip install python-dotenv openai newsapi-python
```

This will create a virtual environment to run the program in, and install any necessary packages for the `app.py` file. 

Additionally, you can create the logging files (the shell script should create them anyways):

```bash
touch newsletter.log && touch job_logging.log
```

Now, navigate to `newsletter.sh` and change the pathnames to match your project structure, then run

```bash
chmod +x newsletter.sh
```

I chose chmod +x and not u+x to ensure this would run with cron, you can additionally run

```bash
chmod 777 newsletter.sh
chmod 777 app.py
```

to ensure that everything is enabled to run. **Only do this if nothing is running, this is considered an unsafe practice.**

Now you should be able to execute the shell script by running `./newsletter.sh`.

## Scheduling the Job with cron

To schedule a job, open crontab with `crontab -e`.

You can add the following command to have the project run at 7AM daily:

```vi
0 7 * * * /path/to/shell/script.sh >> /path/to/job_logging.log 2>&1
```

To change the Hour or Minute, modify the 2nd digit or the 1st digit, respectively. Remember that cron takes in 24-hour time, so something like 2pm would need to be entered as 14.

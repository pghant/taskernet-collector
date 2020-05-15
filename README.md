# Taskernet Collector

Collects public reddit posts and comments from the /r/tasker and /r/taskernet subreddits that have links to https://taskernet.com. Reddit bot that will respond to searches for Taskernet shares.

## Background

This project is in support of the users of the [Tasker application](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm) for Android and the community at https://reddit.com/r/tasker. Users of Tasker are able to share programs they've built through the app through the first party Taskernet system. Using this project, users can more easily search Taskernet shares that were publicly posted on Reddit. See the [announcement post](https://www.reddit.com/r/tasker/comments/gic906/introducing_utaskernetcollector_a_bot_that_will/) for more information.

## How to use

You can call /u/taskernet-collector in a Reddit comment to search for Taskernet shares as follows:

```
/u/taskernet-collector search "query"
```

The bot will respond to the comment with the results that match the query if any. The command must be formatted in precisely this way with the query enclosed in double quotes.

Alternatively, you can also private message the bot and it will reply to the PM. Here you would just omit the mention and just include the following in the message:

```
search "query"
```

The subject of the PM does not matter.

**The bot does not respond to Reddit chat messages**

## Privacy and Security

Taskernet collector only collects publicly posted Taskernet shares on the /r/tasker and /r/taskernet communities. It does not have access to Taskernet shares that were created and not shared on Reddit.

Tasker is a powerful application with a lot of access to private data on your phone. It is important that users of Taskernet Collector **always** check the description of a share before importing, and do not enable anything without understanding what it does. Taskernet collector does not do any verification of shares it collects, and users are responsible for making sure anything they find through this project is safe to use.

## Environment setup

The bot uses a search database on [Algolia](https://www.algolia.com). An Algolia account needs to be created before it can be run. The Python scripts rely on environment variables to be set for the Algolia API.

Reddit API methods are through the [PRAW](https://github.com/praw-dev/praw) library. The scripts depend on a [praw.ini](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html) file in order to initialize PRAW.

## Running the bot

The bot has three Python scripts that are always running:

* `posts_bot.py`
* `comments_bot.py`
* `searcher_bot.py`

The first two are responsible for getting every new post and comment on the monitored subreddits and uploading any Taskernet shares to the database. The third gets new messages that the bot recieves through user mentions and private messages and responds to search requests.
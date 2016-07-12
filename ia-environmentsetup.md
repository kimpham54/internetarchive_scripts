Setting up your environment to use the internetarchive python library. It's best to have your own environment workspace so you don't screw up dependencies and avoid version conflicts between different packages

Install or update your virtualenv

```$ pip install virtualenv
$ pip install --upgrade virtualenv```

I didn't have python 3 installed so I had to get it

```$ brew search python
$ brew install python3
$ python3 --version```

Setup a new environment, this one is named iapy3 and is using python3

```$ virtualenv -p python3 iapy3```

Start the environment

```$ source iapy3/bin/activate```

In your environment install internetarchive

```$ pip install internetarchive```

To quit your environment

```$ deactivate```


# Redmine integration

To setup the redmine python package

```$ pip install python-redmine```




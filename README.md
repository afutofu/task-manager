# Task Manager

My personal tool to manage activities and deadlines

I made this program with the purpose of both creating a handy tool and to make myself more comfortable with python (and programming in general)
This was created around 5 months ago and since then (September 2019 at time of writing) I have learned more programming techniques.

The goal for this git repository is for me to implement these techniques on this old project and hopefully discover any chance of improvement whilst learning to get used to working with git.

Will be updated with better implementation of programming principles, better design, and decrease/eliminate impractical features

To install and run on local environment through bash:

1. On the root project directory, create a virtual environment named "env" by running the following command

```
virtualenv venv
```

If virtualenv is not installed, then install it using pip by the running the command

```
pip install virtualenv
```

2. Activate the virtual environment by running the command

```
source venv/Scripts/activate
```

3. Once activated, install the dependenices from requirements.txt by running the command

```
pip install -r requirements.txt
```

4. After installing dependencies and still on the root project directory, run the following command to run the app

```
python taskmanager.pyw
```

To deactivate the virtual environment, on the root project directory, simply run the command

```
deactivate
```

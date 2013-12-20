checkio-task-tester
===================

Requirements:
-------------

Twisted >= 11.0.0

Using:
------

For using it you need to set some settings in additional file **src/settings_local.py**.
 
    TESTER_KEY -- Your individual tester's key. You can see it on Edit page after adding a task.
    CENTER_FOLDER -- Name for your task on the remote server. You can see it on Edit page after adding a task.
    REPO_FOLDER -- Local path to task's folder.
    CENTER_UCH_PORT -- Local port for transport data (Default: 2323)
    PYTHON_3 -- Local path for python 3 interpreter

Also you can set this parameters with command line

    usage: runner.py [-h] [--center CENTER] [--key KEY] [--folder FOLDER]
                     [--port PORT] [--python3 PYTHON3]

    Checkio Task Tester

    optional arguments:
      -h, --help         show this help message and exit
      --center CENTER    Center folder name for the task (CENTER_FOLDER)
      --key KEY          Your tester key (TESTER_KEY)
      --folder FOLDER    Local path for task folder (REPO_FOLDER)
      --port PORT        Local port for tester (CENTER_UCH_PORT)
      --python3 PYTHON3  Local path for python3 interpreter (PYTHON_3)

Run:
----

    cd checkio-task-tester/src
    python runner.py
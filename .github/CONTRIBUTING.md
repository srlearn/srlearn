# boostsrl-python-package Contributing Guidelines

Our goal is to make BoostSRL more accessible to the Python community by creating general-purpose wrappers for the existing software.

### Submitting Issues (bugs and new features):

* How to file a bug report?

  Start the issue with:

  * boostsrl_java version (`pip freeze | grep "boostsrl_java"`)
  * Development environment details (`python --version`, `java -version`, operating system)

  Briefly explain what led to the bug, and (if relevant) include:

  * Any stack tracebacks that were returned by Python.
  * The background knowledge and some examples from the data.
  * If Java crashed, the tracebacks are logged. Check content of:
    * ~/.boostsrl_data/train_output.txt
    * ~/.boostsrl_data/test_output.txt

  Examples:

  * [java command not found... but only with Python 3?](https://github.com/batflyer/boostsrl-python-package/issues/3)

* How to suggest a new feature?

  If the feature is already part of BoostSRL:

  * Include the command.
  * (e.g. `java -jar bsrl.jar -train train/ -softm -alpha 0.5 -beta -2 -trees 10`)

  Otherwise:

  * Describe the feature in the title (e.g. "Set multiple targets for learning/inference")
  * Include a short paragraph expanding on the title and why the feature would be useful.
  * Include rough code or pseudocode based on how it might work.
  * Include possible inputs and outputs.
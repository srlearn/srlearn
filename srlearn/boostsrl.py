# Copyright 2017, 2018, 2019 Alexander L. Hayes

"""
(Deprecated) boostsrl class for training and testing.

.. warning:: This module is deprecated, pending removal in 0.6.0.
    See :class:`srlearn.rdn` instead.
"""

import os
import re
import subprocess

print(
    "Deprecation Warning: "
    "'srlearn.boostsrl' is deprecated and will be removed in 0.6.0. "
    "'srlearn.rdn' will replace this functionality."
)

# Mode definitions and examples can be verified with regular expressions.
mode_re = re.compile(
    r"[a-zA-Z0-9]*\(((\+|\-|\#)[a-zA-Z0-9]*,( )*)*(\+|\-|\#)[a-zA-Z0-9]*\)\."
)
exam_re = re.compile(r"[a-zA-Z0-9]*\(([a-zA-Z0-9]*,( )*)*[a-zA-Z0-9]*\)\.")


def example_data(example):
    """
    .. deprecated:: 0.5.0
       Use :class:`srlearn.example_data` instead.

    For demo purposes, include some sample data.

    .. code-block:: python

        from srlearn.boostsrl import example_data
        train_pos = example_data('train_pos')
        train_neg = example_data('train_neg')
        train_facts = example_data('train_facts')

    """

    print(
        "Deprecation Warning: "
        "'srlearn.boostsrl.example_data' will be removed in 0.6.0. "
        "'srlearn.example_data' will replace this functionality."
    )

    from . import example_data as ex_data

    if example == "train_pos":
        return ex_data.train.pos
    elif example == "train_neg":
        return ex_data.train.neg
    elif example == "train_facts":
        return ex_data.train.facts
    elif example == "test_pos":
        return ex_data.test.pos
    elif example == "test_neg":
        return ex_data.test.neg
    elif example == "test_facts":
        return ex_data.test.facts
    elif example == "background":
        return ex_data.test.background
    else:
        raise (Exception("Attempted to use sample data that does not exist."))


def call_process(call):
    """
    .. deprecated:: 0.5.0
       Not intended as a public method.

    Create a subprocess and wait for it to finish.
    Raise an Exception if errors occur.
    """
    try:
        p = subprocess.Popen(call, shell=True)
        os.waitpid(p.pid, 0)
    except:
        raise Exception("Encountered problems while running process: ", call)


def inspect_mode_syntax(example):
    """
    .. deprecated:: 0.5.0
       Not intended as a public method.

    Uses a regular expression to check whether all of the examples in a list
    are in the correct form.
    """
    if not mode_re.search(example):
        raise (
            Exception(
                "Error when checking background knowledge; incorrect syntax: "
                + example
                + "\nBackground knowledge should only contain letters and numbers, "
                + "of the form: predicate(+var1, -var2)."
            )
        )


def inspect_example_syntax(example):
    """
    .. deprecated:: 0.5.0
       Not intended as a public method.

    Uses a regular expression to check whether all of the examples in a list are
    in the correct form.
    """
    if not exam_re.search(example):
        raise (Exception("Error when checking example; incorrect syntax: " + example))


def write_to_file(content, path):
    """
    .. deprecated:: 0.5.0
       Not intended as a public method.

    Takes a list (content) and a path/file (path) and
    writes each line of the list to the file location.
    """
    with open(path, "w") as f:
        for line in content:
            f.write(line + "\n")
    f.close()


class modes(object):
    def __init__(
        self,
        background,
        target,
        bridgers=None,
        precomputes=None,
        loadAllLibraries=False,
        useStdLogicVariables=False,
        usePrologVariables=False,
        recursion=False,
        lineSearch=False,
        resampleNegs=False,
        treeDepth=None,
        maxTreeDepth=None,
        nodeSize=None,
        numOfClauses=None,
        numOfCycles=None,
        minLCTrees=None,
        incrLCTrees=None,
    ):
        """
        target: a list of predicate heads that learning/inference will be performed on.
        """
        print(
            "Deprecation Warning: "
            "'srlearn.boostsrl' is deprecated and will be removed in 0.6.0. "
            "'srlearn.rdn' will replace this functionality."
        )

        self.target = target

        self.bridgers = bridgers
        self.precomputes = precomputes

        self.loadAllLibraries = loadAllLibraries
        self.useStdLogicVariables = useStdLogicVariables
        self.usePrologVariables = usePrologVariables
        self.treeDepth = treeDepth
        self.maxTreeDepth = maxTreeDepth
        self.nodeSize = nodeSize
        self.numOfClauses = numOfClauses
        self.numOfCycles = numOfCycles
        self.minLCTrees = minLCTrees
        self.incrLCTrees = incrLCTrees
        self.recursion = recursion
        self.lineSearch = lineSearch
        self.resampleNegs = resampleNegs
        # self.queryPred = 'advisedby/2'

        # Many of the arguments in the modes object are optional this shows
        # us the values of the ones that are neither false nor none.

        types = {
            "background should be a list.": isinstance(background, list),
            "target should be a list.": isinstance(target, list),
            "bridgers should be a list.": isinstance(bridgers, list)
            or bridgers is None,
            "precomputes should be a dictionary.": isinstance(precomputes, dict)
            or precomputes is None,
            "loadAllLibraries should be boolean.": isinstance(loadAllLibraries, bool),
            "useStdLogicVariables should be boolean.": isinstance(
                useStdLogicVariables, bool
            ),
            "usePrologVariables should be boolean.": isinstance(
                usePrologVariables, bool
            ),
            "recursion should be boolean.": isinstance(recursion, bool),
            "lineSearch should be boolean.": isinstance(lineSearch, bool),
            "resampleNegs should be boolean.": isinstance(resampleNegs, bool),
            "treeDepth should be an int.": isinstance(treeDepth, int)
            or treeDepth is None,
            "maxTreeDepth should be an int.": isinstance(maxTreeDepth, int)
            or maxTreeDepth is None,
            "nodeSize should be an int.": isinstance(nodeSize, int) or nodeSize is None,
            "numOfClause should be an int.": isinstance(numOfClauses, int)
            or numOfClauses is None,
            "numOfCycles should be an int.": isinstance(numOfCycles, int)
            or numOfCycles is None,
            "minLCTrees should be an int.": isinstance(minLCTrees, int)
            or minLCTrees is None,
            "incrLCTrees should be an int.": isinstance(incrLCTrees, int)
            or incrLCTrees is None,
        }

        # Force type checking for input validation Issue #5
        for type_check in types:
            if not types[type_check]:
                raise (TypeError("Error when checking type: " + type_check))

        relevant = [
            [attr, value]
            for attr, value in self.__dict__.items()
            if (value is not False) and (value is not None)
        ]
        self.relevant = relevant

        background_knowledge = []
        for a, v in relevant:
            if a in ["useStdLogicVariables", "usePrologVariables"] and v:
                s = a + ": " + str(v).lower() + "."
                background_knowledge.append(s)
            elif a in ["target", "bridgers", "precomputes"]:
                pass
            elif v:
                s = "setParam: " + a + "=" + str(v).lower() + "."
                background_knowledge.append(s)
            else:
                s = "setParam: " + a + "=" + str(v) + "."
                background_knowledge.append(s)

        for pred in background:
            inspect_mode_syntax(pred)
            background_knowledge.append("mode: " + pred)

        if self.bridgers is not None:
            for bridger in self.bridgers:
                background_knowledge.append("bridger: " + bridger)

        if self.precomputes is not None:
            for precompute in self.precomputes:
                background_knowledge.append(self.precomputes[precompute])
                background_knowledge.append("mode: " + precompute)

        # Write the newly created background_knowledge to a file: background.txt
        self.background_knowledge = background_knowledge
        write_to_file(background_knowledge, "background.txt")


class train(object):
    """
    .. deprecated:: 0.5.0
       Use :class:`srlearn.rdn` instead.
    """

    def __init__(
        self,
        background,
        train_pos,
        train_neg,
        train_facts,
        save=False,
        advice=False,
        softm=False,
        alpha=0.5,
        beta=-2,
        trees=10,
    ):
        print(
            "Deprecation Warning: "
            "'srlearn.boostsrl' is deprecated and will be removed in 0.6.0. "
            "'srlearn.rdn' will replace this functionality."
        )

        self.target = background.target
        self.train_pos = train_pos
        self.train_neg = train_neg
        self.train_facts = train_facts
        self.advice = advice
        self.softm = softm
        self.alpha = alpha
        self.beta = beta
        self.trees = trees

        # Syntax checking for examples in each set.
        for example in self.train_pos:
            inspect_example_syntax(example)
        for example in self.train_neg:
            inspect_example_syntax(example)
        for example in self.train_facts:
            inspect_example_syntax(example)

        write_to_file(self.train_pos, "srlearn/train/train_pos.txt")
        write_to_file(self.train_neg, "srlearn/train/train_neg.txt")
        write_to_file(self.train_facts, "srlearn/train/train_facts.txt")

        CALL = (
            "(cd srlearn; java -jar v1-0.jar -l -train train/ -target "
            + ",".join(self.target)
            + " -trees "
            + str(self.trees)
            + " > train_output.txt 2>&1)"
        )
        call_process(CALL)

    def tree(self, treenumber, target, image=False):
        """
        """
        # Tree number is between 0 and the self.trees.
        if treenumber > (self.trees - 1):
            raise Exception("Tried to find a tree that does not exist.")
        elif image:
            """
            Writing this with Jupyter notebooks in mind.
            """
            from graphviz import Source

            tree_file = (
                "srlearn/train/models/bRDNs/dotFiles/WILLTreeFor_"
                + target
                + str(treenumber)
                + ".dot"
            )
            with open(tree_file, "r") as f:
                tree_output = "".join(f.read().splitlines())
            src = Source(tree_output)
            return src
        else:
            tree_file = (
                "srlearn/train/models/bRDNs/Trees/"
                + target
                + "Tree"
                + str(treenumber)
                + ".tree"
            )
            with open(tree_file, "r") as f:
                tree_output = f.read()
            return tree_output

    def _get_training_time(self):
        """
        Return the training time as a float representing the total number of
        seconds seconds.
        """
        with open("srlearn/train_output.txt", "r") as f:
            text = f.read()
        line = re.findall(r"% Total learning time \(\d* trees\):.*", text)
        # Remove the last character "." from the line and split it on spaces.
        splitline = line[0][:-1].split()
        return splitline

    def _training_time_to_float(self, splitline):
        """
        Convert the string representing training time into a float representing
        total seconds.
        """
        seconds = []
        if "milliseconds" in splitline:
            seconds.append(
                (float(splitline[splitline.index("milliseconds") - 1])) / 1000
            )
        if "seconds" in splitline:
            seconds.append(float(splitline[splitline.index("seconds") - 1]))
        if "minutes" in splitline:
            seconds.append(float(splitline[splitline.index("minutes") - 1]) * 60)
        if "hours" in splitline:
            seconds.append(float(splitline[splitline.index("hours") - 1]) * 3600)
        if "days" in splitline:
            seconds.append(float(splitline[splitline.index("days") - 1]) * 86400)
        return sum(seconds)

    def traintime(self) -> float:
        """
        Returns a float representing seconds.
        """
        splitline = self._get_training_time()
        return self._training_time_to_float(splitline)


class test(object):
    """
    .. deprecated:: 0.5.0
       Use :class:`srlearn.rdn` instead.
    """

    # Possibly a partial fix to Issue #3: checking for the .aucTemp.txt.lock
    if os.path.isfile("srlearn/test/AUC/.aucTemp.txt.lock"):
        print("Found lock file srlearn/test/AUC/.aucTemp.txt.lock, removing it:")
        os.remove("srlearn/test/AUC/.aucTemp.txt.lock")

    def __init__(self, model, test_pos, test_neg, test_facts, trees=10):
        write_to_file(test_pos, "srlearn/test/test_pos.txt")
        write_to_file(test_neg, "srlearn/test/test_neg.txt")
        write_to_file(test_facts, "srlearn/test/test_facts.txt")

        print(
            "Deprecation Warning: "
            "'srlearn.boostsrl' is deprecated and will be removed in 0.6.0. "
            "'srlearn.rdn' will replace this functionality."
        )

        self.target = model.target

        CALL = (
            "(cd srlearn; java -jar v1-0.jar -i -model train/models/ "
            + "-test test/ -target "
            + ",".join(self.target)
            + " -trees "
            + str(trees)
            + " -aucJarPath . > test_output.txt 2>&1)"
        )
        call_process(CALL)

    def summarize_results(self):
        with open("srlearn/test_output.txt", "r") as f:
            text = f.read()
        line = re.findall(
            r"%   AUC ROC.*|%   AUC PR.*|%   CLL.*|%   Precision.*|%   Recall.*|%   F1.*",
            text,
        )
        line = [
            word.replace(" ", "")
            .replace("\t", "")
            .replace("%", "")
            .replace("atthreshold=", ",")
            for word in line
        ]

        results = {
            "AUC ROC": line[0][line[0].index("=") + 1 :],
            "AUC PR": line[1][line[1].index("=") + 1 :],
            "CLL": line[2][line[2].index("=") + 1 :],
            "Precision": line[3][line[3].index("=") + 1 :],
            "Recall": line[4][line[4].index("=") + 1 :],
            "F1": line[5][line[5].index("=") + 1 :],
        }
        return results

    def _float_split(self, line):
        """Returns a list where the first item is a string and the second is a float.

        Used when returning inference results.

        Examples
        --------

        >>> test._float_split('target(pred1, pred2, pred3). 0.85691')
        ['target(pred1, pred2, pred3).', 0.85691]"""
        intermediate = line.rsplit(None, 1)
        return [intermediate[0], float(intermediate[1])]

    def inference_results(self, target):
        """Converts BoostSRL results into a Python dictionary."""
        results_file = "srlearn/test/results_" + target + ".db"
        inference_dict = {}

        with open(results_file, "r") as f:
            for line in f.read().splitlines():
                full = self._float_split(line)
                key_predicate = full[0]
                value_regression = full[1]
                inference_dict[key_predicate] = value_regression
        return inference_dict

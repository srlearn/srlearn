# Copyright 2020 Alexander L. Hayes

from srlearn.utils._parse_trees import parse_tree


def test_parse_tree_1():
    _tree = (
        "setParam: stringsAreCaseSensitive = true.\n"
        "\n"
        "usePrologVariables: true.\n"
        "\n"
        "\n"
        "(faculty(A, -0.09269127618926057) :-  /* #neg=198 */ student(A)).\n"
        "(faculty(A, 0.3207118471601502) :-  /* #pos=107 */ sameperson(A, A)).\n"
        "faculty(_, -0.09269127618926093) /* #neg=20 */ .\n"
    )

    features = parse_tree(_tree, use_prolog_variables=True)
    assert features == ["student", "sameperson"]


def test_parse_std_logic_tree_1():
    _tree = (
        "setParam: stringsAreCaseSensitive = true.\n\n"
        "useStdLogicNotation: true.\n\n"
        "(smokes(a) => cancer(a, 0.8581489350995121)).\n"
        "cancer(_, 0.19148226843284552) /* #neg=2 #pos=1 */ .\n"
    )
    features = parse_tree(_tree, use_prolog_variables=False)
    assert features == ["smokes"]

# Copyright 2020 Alexander L. Hayes

from collections import Counter
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


def test_parse_tree_2():
    _tree = (
        "setParam: stringsAreCaseSensitive = true.\n\n"
        "usePrologVariables: true.\n\n\n"
        "(sameauthor(A, B, 0.8581489350995123) :-  /* #pos=15 */ haswordauthor(A, UniqueVar1), haswordauthor(B, UniqueVar1), haswordvenue(UniqueVar2, UniqueVar1), haswordtitle(_, UniqueVar1), author(UniqueVar3, A), venue(UniqueVar3, UniqueVar2)).\n"
        "(sameauthor(A, B, 0.8581489350995123) :-  /* #pos=8 */ haswordauthor(A, UniqueVar4), haswordauthor(B, UniqueVar4), haswordvenue(_, UniqueVar4), haswordtitle(UniqueVar5, UniqueVar4), author(UniqueVar6, A), title(UniqueVar6, UniqueVar5)).\n"
        "(sameauthor(A, B, 0.8435503949535248) :-  /* #neg=2 #pos=135 */ haswordauthor(A, UniqueVar7), haswordauthor(B, UniqueVar7), haswordvenue(_, UniqueVar7), haswordtitle(_, UniqueVar7)).\n"
        "(sameauthor(A, B, 0.8581489350995123) :-  /* #pos=14 */ haswordauthor(A, UniqueVar8), haswordauthor(B, UniqueVar8), haswordauthor(A, UniqueVar9), haswordtitle(UniqueVar10, UniqueVar9), author(UniqueVar11, B), title(UniqueVar11, UniqueVar10)).\n"
        "(sameauthor(A, B, 0.7592896195101551) :-  /* #neg=26 #pos=237 */ haswordauthor(A, UniqueVar12), haswordauthor(B, UniqueVar12), haswordauthor(A, UniqueVar13), haswordtitle(_, UniqueVar13))\n."
        "(sameauthor(A, B, 0.8110901115701004) :-  /* #neg=4 #pos=81 */ haswordauthor(A, UniqueVar14), haswordauthor(B, UniqueVar14), haswordauthor(B, UniqueVar15), haswordvenue(_, UniqueVar15)).\n"
        "(sameauthor(A, B, 0.8581489350995108) :-  /* #pos=113 */ haswordauthor(A, UniqueVar16), haswordauthor(B, UniqueVar16)).\n"
        "sameauthor(_, _, -0.1418510649004877) /* #neg=26 */ .\n"
    )

    features = Counter(parse_tree(_tree, use_prolog_variables=True))
    assert features["haswordauthor"] == 17
    assert features["haswordtitle"] == 5
    assert features["haswordvenue"] == 4
    assert features["author"] == 3
    assert features["title"] == 2
    assert features["venue"] == 1


def test_parse_tree_3():
    _tree = (
        "setParam: stringsAreCaseSensitive = true.\n\n"
        "usePrologVariables: true.\n\n\n"
        "(sameauthor(A, B, 0.7094882029476938) :-  /* #neg=2 #pos=158 */ haswordauthor(A, UniqueVar17), haswordauthor(B, UniqueVar17), haswordauthor(B, UniqueVar18), haswordtitle(UniqueVar19, UniqueVar18), haswordauthor(A, UniqueVar18), haswordvenue(_, UniqueVar17), haswordtitle(UniqueVar19, UniqueVar17)).\n"
        "(sameauthor(A, B, 0.7373144535908095) :-  /* #pos=35 */ haswordauthor(A, UniqueVar20), haswordauthor(B, UniqueVar20), haswordauthor(B, UniqueVar21), haswordtitle(_, UniqueVar21), haswordauthor(A, UniqueVar21), haswordvenue(_, UniqueVar20)).\n"
        "(sameauthor(A, B, 0.5869937596476273) :-  /* #neg=22 #pos=123 */ haswordauthor(A, UniqueVar22), haswordauthor(B, UniqueVar22), haswordauthor(B, UniqueVar23), haswordtitle(_, UniqueVar23), haswordauthor(A, UniqueVar24), haswordtitle(_, UniqueVar24)).\n"
        "(sameauthor(A, B, 0.6847284875533644) :-  /* #neg=4 #pos=93 */ haswordauthor(A, UniqueVar25), haswordauthor(B, UniqueVar25), haswordauthor(B, UniqueVar26), haswordtitle(_, UniqueVar26)).\n"
        "(sameauthor(A, B, 0.6721336978425174) :-  /* #neg=4 #pos=57 */ haswordauthor(A, UniqueVar27), haswordauthor(B, UniqueVar27), haswordauthor(A, UniqueVar28), haswordvenue(_, UniqueVar28), haswordtitle(_, UniqueVar28)).\n"
        "(sameauthor(A, B, 0.7298346530049215) :-  /* #pos=24 */ haswordauthor(A, UniqueVar29), haswordauthor(B, UniqueVar29), haswordauthor(A, UniqueVar30), haswordvenue(_, UniqueVar30)).\n"
        "(sameauthor(A, B, 0.7241233018653317) :-  /* #pos=113 */ haswordauthor(A, UniqueVar31), haswordauthor(B, UniqueVar31)).\n"
        "sameauthor(_, _, -0.12544463852839138) /* #neg=26 */ .\n"
    )

    features = Counter(parse_tree(_tree, use_prolog_variables=True))
    assert features["haswordauthor"] == 23
    assert features["haswordtitle"] == 7
    assert features["haswordvenue"] == 4


def test_parse_std_logic_tree_1():
    _tree = (
        "setParam: stringsAreCaseSensitive = true.\n\n"
        "useStdLogicNotation: true.\n\n\n"
        "(smokes(a) => cancer(a, 0.8581489350995121)).\n"
        "cancer(_, 0.19148226843284552) /* #neg=2 #pos=1 */ .\n"
    )
    features = parse_tree(_tree, use_prolog_variables=False)
    assert features == ["smokes"]

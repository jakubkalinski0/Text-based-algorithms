from Lab2.build_dfa import (
    Alternative,
    Concatenation,
    Empty,
    Epsilon,
    KleeneStar,
    Symbol,
    build_dfa,
    simplify,
)


class TestBrzozowskiDFA:
    def test_kleene_star_a(self):
        a = Symbol("a")
        regex = KleeneStar(a)
        dfa = build_dfa(regex, {"a"})

        assert dfa.accepts("")

        assert dfa.accepts("a")

        assert dfa.accepts("aa")
        assert dfa.accepts("aaa")

        assert not dfa.accepts("b")
        assert not dfa.accepts("ab")

    def test_kleene_star_alternative(self):
        a = Symbol("a")
        b = Symbol("b")
        regex = KleeneStar(Alternative(a, b))
        dfa = build_dfa(regex, {"a", "b"})

        assert dfa.accepts("")

        assert dfa.accepts("a")
        assert dfa.accepts("b")

        assert dfa.accepts("ab")
        assert dfa.accepts("ba")
        assert dfa.accepts("aabb")
        assert dfa.accepts("abba")
        assert dfa.accepts("ababababab")

        assert not dfa.accepts("c")
        assert not dfa.accepts("abc")

    def test_concatenation(self):
        a = Symbol("a")
        b = Symbol("b")
        regex = Concatenation(a, b)
        dfa = build_dfa(regex, {"a", "b"})

        assert not dfa.accepts("")

        assert not dfa.accepts("a")
        assert not dfa.accepts("b")

        assert dfa.accepts("ab")
        assert not dfa.accepts("ba")
        assert not dfa.accepts("abb")
        assert not dfa.accepts("aab")
        assert not dfa.accepts("abc")

    def test_complex_regex(self):
        a = Symbol("a")
        b = Symbol("b")
        regex = Concatenation(a, KleeneStar(Concatenation(b, a)))
        dfa = build_dfa(regex, {"a", "b"})

        assert not dfa.accepts("")

        assert dfa.accepts("a")
        assert dfa.accepts("aba")
        assert dfa.accepts("ababa")
        assert dfa.accepts("abababa")

        assert not dfa.accepts("b")
        assert not dfa.accepts("ab")
        assert not dfa.accepts("ba")
        assert not dfa.accepts("abab")

    def test_nullable(self):
        a = Symbol("a")
        b = Symbol("b")

        assert not Empty().nullable()
        assert Epsilon().nullable()
        assert not Symbol("a").nullable()

        assert not Concatenation(a, b).nullable()
        assert Concatenation(Epsilon(), Epsilon()).nullable()
        assert not Concatenation(a, Epsilon()).nullable()
        assert not Concatenation(Epsilon(), b).nullable()

        assert not Alternative(a, b).nullable()
        assert Alternative(a, Epsilon()).nullable()
        assert Alternative(Epsilon(), b).nullable()

        assert KleeneStar(a).nullable()
        assert KleeneStar(Empty()).nullable()

    def test_derivatives(self):
        a = Symbol("a")
        b = Symbol("b")

        assert str(a.derivative("a")) == "ε"
        assert str(a.derivative("b")) == "∅"

        concat = Concatenation(a, b)
        assert str(concat.derivative("a")) == "(εb)"
        assert str(concat.derivative("b")) == "∅"

        alt = Alternative(a, b)
        assert str(alt.derivative("a")) == "ε"
        assert str(alt.derivative("b")) == "ε"
        assert str(alt.derivative("c")) == "∅"

        star = KleeneStar(a)
        assert str(star.derivative("a")) == "(ε(a)*)"
        assert str(star.derivative("b")) == "∅"

        complex_regex = Concatenation(a, KleeneStar(Concatenation(b, a)))
        assert str(complex_regex.derivative("b")) == "∅"

    def test_simplification(self):
        a = Symbol("a")
        b = Symbol("b")

        assert str(simplify(a)) == "a"
        assert str(simplify(Empty())) == "∅"
        assert str(simplify(Epsilon())) == "ε"

        assert str(simplify(Alternative(a, Empty()))) == "a"
        assert str(simplify(Alternative(Empty(), b))) == "b"
        assert str(simplify(Alternative(a, a))) == "a"

        assert str(simplify(Concatenation(a, Empty()))) == "∅"
        assert str(simplify(Concatenation(Empty(), b))) == "∅"
        assert str(simplify(Concatenation(a, Epsilon()))) == "a"
        assert str(simplify(Concatenation(Epsilon(), b))) == "b"

        assert str(simplify(KleeneStar(KleeneStar(a)))) == "(a)*"
        assert str(simplify(KleeneStar(Epsilon()))) == "ε"
        assert str(simplify(KleeneStar(Empty()))) == "ε"

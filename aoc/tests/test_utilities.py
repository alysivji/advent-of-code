from aoc.utilities import print_


def test__print_decorator(capsys):
    def my_func():
        return 2

    @print_
    def my_func_decorated():
        return 2

    my_func()
    assert capsys.readouterr()

    my_func_decorated()
    assert '2' in capsys.readouterr().out

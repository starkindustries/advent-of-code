import importlib.util


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def helper(day):
    year = 2022
    script = module_from_file("PLACEHOLDER", f"./{year}/{day}/solve.py")
    script.test(f"./{year}/{day}/")


def test01():
    helper("01")


def test02():
    helper("02")


def test03():
    helper("03")


def test04():
    helper("04")


def test05():
    helper("05")


def test06():
    helper("06")


def test07():
    helper("07")


def test08():
    helper("08")


def test09():
    helper("09")


def test10():
    helper("10")


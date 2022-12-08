import importlib.util


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def helper(day):
    script = module_from_file("advent", f"./{day}/solve.py")
    script.test(f"./{day}/")


def test08():
    helper("08")


import time

from pytest_result_sender import plugin


def test_plugin():
    time.sleep(2.5)
    # print(plugin.__file__)

def test_pass():
    pass

def test_fail():
    assert False
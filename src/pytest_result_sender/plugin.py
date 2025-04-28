from datetime import datetime,timedelta

import pytest

data = {
    "passed": 0,
    "failed": 0,
}

def pytest_runtest_logreport(report:pytest.TestReport):
    # print(report)
    if report.when == 'call':
        print("本次用例的执行结果", report.outcome)
        data[report.outcome] += 1
def pytest_collection_finish(session:pytest.Session):
    # 用例加载完成之后执行，包含全部的用例
    data['total']=len(session.items)
def pytest_configure():
    # 配置加载完毕后执行，所有测试用例执行前执行
    data['start_time']=datetime.now()
    # print(f"{datetime.now()} pytest开始执行")

def pytest_unconfigure():
    # 配置卸载完毕后执行，所有测试用例执行后执行
    data['end_time'] = datetime.now()
    data['duration'] = data['end_time']-data['start_time']
    assert timedelta(seconds=3) > data['duration'] > timedelta(seconds=2.5)
    assert data['total'] == 3
    assert data['passed'] == 2
    assert data['failed'] == 1
    # print(f"{datetime.now()} pytest结束执行")
    # print(data)

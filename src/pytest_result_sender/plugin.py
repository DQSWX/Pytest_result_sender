from datetime import datetime, timedelta

import pytest
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

data = {
    "passed": 0,
    "failed": 0,
}


def pytest_addoption(parser):
    parser.addini(
        'send_when',
        help="何时发送邮件，every(每次都发送)，on_fail(失败时发送)"
    )
    parser.addini(
        'receiver_email',
        help="发到何处"
    )


def pytest_runtest_logreport(report: pytest.TestReport):
    # print(report)
    if report.when == 'call':
        print("本次用例的执行结果", report.outcome)
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    # 用例加载完成之后执行，包含全部的用例
    data['total'] = len(session.items)


def pytest_configure(config: pytest.Config):
    # 配置加载完毕后执行，所有测试用例执行前执行
    data['start_time'] = datetime.now()
    data['send_when'] = config.getini("send_when")
    data['receiver_email'] = config.getini("receiver_email")
    # print(f"{datetime.now()} pytest开始执行")


def pytest_unconfigure():
    # 配置卸载完毕后执行，所有测试用例执行后执行
    data['end_time'] = datetime.now()
    data['duration'] = data['end_time'] - data['start_time']
    data['pass-ratio'] = data['passed'] / data['total'] * 100
    data['pass-ratio'] = f"{data['pass-ratio']:.2f}%"
    assert timedelta(seconds=3) > data['duration'] > timedelta(seconds=2.5)
    assert data['total'] == 3
    assert data['passed'] == 2
    assert data['failed'] == 1
    assert data['pass-ratio'] == '66.67%'
    send_email()


def send_email():
    # 配置参数
    SMTP_SERVER = "smtp.163.com"
    SMTP_PORT = 465
    SENDER_EMAIL = "jadeyan1987@163.com"
    AUTH_CODE = "AKfk9qk8kHkeLHnx"  # 替换为实际授权码
    receiver_email = data['receiver_email']

    if data['send_when'] == 'on_fail' and data['failed'] == 0:
        return
    if not data['receiver_email']:
        return
    test_result = f"""
    测试时间：{data['end_time']}
    用例数量：{data['total']} 
    执行时长：{data['duration']} 
    测试通过：{data['passed']} 
    测试失败：{data['failed']} 
    测试通过率：{data['pass-ratio']}
    """
    # 构建邮件对象
    msg = MIMEText(test_result, "plain", "utf-8")
    msg["From"] = formataddr(["自动化测试系统", SENDER_EMAIL])
    msg["To"] = receiver_email
    msg["Subject"] = f"""【测试报告】{datetime.now()}测试结果"""

    try:
        # 使用 SSL 加密连接
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, AUTH_CODE)
            server.sendmail(SENDER_EMAIL, [receiver_email], msg.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(f"发送失败: {str(e)}")

### 1.创建项目

- 选择项目目录
- 创建venv
  - vs code不能Add  Project，只能打开文件夹，后续通过pdm初始化项目虽然也会生成venv，但后续`plugin.__file__`的路径指向并不是pyproject.toml所配置的路径，所以会导致修改项目中的plugin.py而无法生效的问题
  - 使用PyCharm创建项目，会自带生成venv目录，就没有上述问题

- 安装PDM

- 使用PDM初始化项目

  ```python
  pdm init
  ```

- 在`pyproject.toml`配置文件中补充一下内容

  ```python
  # 插件的入口点
  [project.entry-points.pytest11]
  result_log="pytest_result_sender.plugin"
  
  # 源码的位置
  [tool.pdm.build]
  package-dir = "src"
  ```

- 在目录src下的pytest_result_sender文件夹中创建plugin.py文件，在其中编写代码

  ```python
  from datetime import datetime
  
  def pytest_configure():
      # 配置加载完毕后执行，所有测试用例执行前执行
      print(f"{datetime.now()} pytest开始执行")
  
  def pytest_unconfigure():
      # 配置卸载完毕后执行，所有测试用例执行后执行
      print(f"{datetime.now()} pytest结束执行")
  ```

- 添加依赖

  ```python
  pdm add pytest
  ```


- 此时在终端输入Pytest回车即可看到上述代码被已被执行（若Pytest命令不能被识别则需安装Pytest）

- 打包
  - 运行 `pdm build`即可
  - 运行完会生成文件夹dist及两个文件
    - pytest_result_sender-0.1.0.tar.gz ---是预编译的二进制包，安装速度快，适用于大多数Python环境。
    - pytest_result_sender-0.1.0-py3-none-any.whl ---（源码分发包）包含项目的源代码，适用于需要查看或修改源代码的情况，或在特定平台上进行安装。

- 验证
  - 新建一个项目，并将pytest_result_sender-0.1.0-py3-none-any.whl文件复制该项目目录中，在终端运行 `pip install pytest_result_sender-0.1.0-py3-none-any.whl`  ---在安装这个插件时Pytest也会被自动安装，不需单独安装
  - 任意创建一个testcase，终端运行即可得到验证结果
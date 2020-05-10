# 提交前的测试

在准备提交前，请对每一个测试数据文件，进行一次本测试。

lastcheck.py会做以下的事情：
1. 解压压缩包
2. 调用javac编译
3. 调用jwdbg（不是ndbg）测试生成的class文件。不用ndbg是因为怕有的同学输出了ndbg的`[Echo]xxx`。

## 运行测试
1. 将要提交的.zip文件拷贝到本目录，然后命名为`to_submit.zip`
2. windows用户请运行**powershell**或者**cmd**，**别运行git-bash**，会乱码。
3. 检查中文乱码：运行`java -h`，如果有java的帮助提示并没有乱码，那么就行了。（没有输出也代表有乱码）
4. 检查java版本：`java -version`。请确保为1.8左右的版本，因为需要兼容正式评测。不行则去找教程设置PATH。
5. 检查javac版本：`javac -version`。请确保为1.8左右的版本。
6. 运行测试：`python lastcheck.py -case jw06.yml`，这个`jw06.yml`代表测试文件。



## 关于包的要求

https://shimo.im/docs/VwcQDqkpggqdxCXy 这是助教的说明

总结一下，就是：
- 可以有包
- 可以import自己写的包
- 但是，默认包必须要包含Test
- import的其他包不能使得`javac -cp ./src ./src/*.java -Xlint:unchecked -encoding UTF-8`编译失败。


## 拆包工具

符合上述条件的同学可以不用管。不符合的可以试一下这个拆包工具（贡献者：@HolmiumTS ）

但是，**请注意**：
- 阅读该工具的功能说明，除非你知道它在干什么，否则不要盲目使用
- **请在操作前备份数据**

`Format.py`由 @HolmiumTS 提供，#2

用法：`python Format.py [src]`

功能说明：将`[src]`及其子目录下的.java代码提取出来，删除其中的package以及非java开头的import语句，并输出到Format.py所在的目录下
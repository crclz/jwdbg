# NDbg

## 特点
`jwdbg.py`在有一部分情况下，无法准确定位出错的行。

`ndbg.py`解决了这个问题。顺便美化了输出内容。

## 前提条件：修改你的java程序
ndbg要求待测目标程序在读取输入行的时候，输出`[Echo]+这个行`。

例如，假如程序读入`SUDO`，那么就应该紧接着输出一行`[Echo]SUDO`。这种输出是ndbg定位出错命令的依据。

具体做法就是，每一次调用`scanner.nextLine()`时，输出`[Echo].....`。推荐将`nextLine`用另一个方法包装，然后将每个`nextLine()`都换成另一个方法。

## 防止出错
刚刚，你修改了java程序，让java程序多输出了东西。你可能在提交的时候忘记恢复这种行为。

所以，应该采用一个动态的**标志**来控制这种行为，只有检测到这个标志时，你的java程序才应该表现相应的额外行为。

`ndbg.py`提供了便捷途径。它会将环境变量中的`JWDBG`设为`debugging`，作为标志。这个环境变量是临时的，只对当前shell和从shell启动的程序有效。详情请复习系统编程linux的基础知识。

**简单来说，用ndbg进行测试时，在你的java程序的眼里，以下等式成立**：
```java
"debugging".equals(System.getenv("JWDBG"))
```

## 示例代码

MyInputer.java

```java
import java.util.Scanner;

public class MyInputer {
    private Scanner scanner;
    private boolean isDebug;

    public MyInputer() {
        scanner = new Scanner(System.in);

        // 只有当环境变量JWDBG=debugging时，isDebug=true
        isDebug = "debugging".equals(System.getenv("JWDBG"));
    }

    public String nextLine() {
        String line = scanner.nextLine();
        if (isDebug) {
            System.out.println("[Echo]" + line);
        }
        return line;
    }
}
```


然后，全局使用一个`MyInputer`（或者采用单例模式），在所有原来用scanner的地方，替换成：
```java
// before
String x = scanner.nextLine();

// after
String x = myInputer.nextLine();
```

所以，修改你的java程序，让只有当这个表达式为`true`时，才输出`[Echo]...`。

## 常见错误
- Echo lines integration check failure: 你的程序并未按照要求输出`[Echo]...`。请搜索以下你的源文件，确保没有对scanner.nextLine的直接调用（除了包装类中）。

## 二次检查
最后，别忘了使用`jwdbg.py`来进行测试，以防程序有额外的行为。

## 运行方法
运行方法和`jwdbg`一致，只不过将`jwdbg.py`换成了`ndbg.py`。
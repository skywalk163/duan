# L4 外语引用

L4 层通过 `引 语言:` 块嵌入 Python、C、Go、MoonBit 代码，运行在隔离沙箱中。

## Python 引用

```python
引 Python:
    import numpy as np
    def l4_numpy_mean(arr):
        return float(np.mean(arr))
出 l4_numpy_mean

设 数据 = 列(1, 2, 3, 4, 5)
印(l4_numpy_mean(数据))  # 3.0
```

## C 引用

```python
引 C:
    int add(int a, int b) {
        return a + b;
    }
出 add

印(add(10, 20))  # 30
```

## Go 引用

```python
引 Go:
    package main
    func multiply(a, b int) int {
        return a * b
    }
出 multiply

印(multiply(6, 7))  # 42
```

## MoonBit 引用

```python
引 MoonBit:
    fn factorial(n: Int) -> Int {
        if n <= 1 { 1 } else { n * factorial(n - 1) }
    }
出 factorial

印(factorial(5))  # 120
```

## 沙箱隔离

L4 代码运行在独立的沙箱环境中，具有以下安全特性：

- 隔离的命名空间
- 资源限制（CPU、内存）
- 禁止文件系统访问（默认）
- 禁止网络访问（默认）
- 可配置的权限策略
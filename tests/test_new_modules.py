"""
新增模块测试 - SQLite + 补全方案

测试13个新增模块：
高优先级：SQLite数据库、系统接口、外部命令、参数解析
中优先级：复制、时间、文件匹配、对象序列化、美化输出、枚举
低优先级：高级文件、压缩、文本差异
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'stdlib'))

import tempfile
import time


class 测试结果:
    def __init__(self):
        self.通过 = 0
        self.失败 = 0
        self.失败详情 = []
    
    def 记录通过(self, 名称):
        self.通过 += 1
        print(f"  ✅ {名称}")
    
    def 记录失败(self, 名称, 错误):
        self.失败 += 1
        self.失败详情.append((名称, 错误))
        print(f"  ❌ {名称}: {错误}")


def 测试_SQLite数据库(结果: 测试结果):
    print("\n📦 SQLite数据库")
    try:
        import SQLite数据库
        
        # 测试内存数据库
        with SQLite数据库.SQLite数据库(":memory:") as db:
            # 创建表
            db.创建表("用户", {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "姓名": "TEXT",
                "年龄": "INTEGER",
                "城市": "TEXT"
            })
            assert db.表存在("用户") == True
            
            # 插入数据
            db.插入("用户", {"姓名": "张三", "年龄": 25, "城市": "北京"})
            db.插入("用户", {"姓名": "李四", "年龄": 30, "城市": "上海"})
            db.批量插入("用户", [
                {"姓名": "王五", "年龄": 28, "城市": "广州"},
                {"姓名": "赵六", "年龄": 35, "城市": "深圳"},
            ])
            
            # 查询
            assert db.计数("用户") == 4
            用户列表 = db.查询("SELECT * FROM 用户 WHERE 年龄 > ?", (28,))
            assert len(用户列表) == 2
            
            单个 = db.查询一行("SELECT * FROM 用户 WHERE 姓名=?", ("张三",))
            assert 单个 is not None
            assert 单个["姓名"] == "张三"
            assert 单个["年龄"] == 25
            
            # 更新
            db.更新("用户", {"年龄": 26}, "姓名=?", ("张三",))
            张三 = db.查询一行("SELECT * FROM 用户 WHERE 姓名=?", ("张三",))
            assert 张三["年龄"] == 26
            
            # 删除
            db.删除("用户", "姓名=?", ("赵六",))
            assert db.计数("用户") == 3
            
            # 导出导入JSON
            json_str = db.导出为JSON("用户")
            assert "张三" in json_str
            
            # 表列表
            表列表 = db.获取表列表()
            assert "用户" in 表列表
            
            # 表结构
            结构 = db.获取表结构("用户")
            assert len(结构) > 0
            
            # 便捷函数
            assert SQLite数据库.获取SQLite版本() is not None
            assert SQLite数据库.数据库存在(":memory:") == False  # 内存数据库不算
        
        # 测试文件数据库
        临时文件 = tempfile.mktemp(suffix=".db")
        try:
            db = SQLite数据库.打开数据库(临时文件)
            db.执行("CREATE TABLE test (id INTEGER)")
            db.插入("test", {"id": 1})
            db.关闭()
            
            assert SQLite数据库.数据库存在(临时文件) == True
            
            # 备份
            备份文件 = tempfile.mktemp(suffix=".db")
            db2 = SQLite数据库.打开数据库(临时文件)
            db2.备份(备份文件)
            db2.关闭()
            assert os.path.exists(备份文件)
            os.unlink(备份文件)
        finally:
            if os.path.exists(临时文件):
                os.unlink(临时文件)
        
        结果.记录通过("SQLite数据库")
    except Exception as e:
        结果.记录失败("SQLite数据库", str(e))


def 测试_系统接口(结果: 测试结果):
    print("\n📦 系统接口")
    try:
        import 系统接口
        
        # 环境变量
        系统接口.设置环境变量("测试变量", "测试值")
        assert 系统接口.获取环境变量("测试变量") == "测试值"
        assert 系统接口.环境变量存在("测试变量") == True
        系统接口.删除环境变量("测试变量")
        assert 系统接口.环境变量存在("测试变量") == False
        assert isinstance(系统接口.获取所有环境变量(), dict)
        
        # 路径操作
        assert 系统接口.路径存在(".") == True
        assert 系统接口.是目录(".") == True
        assert 系统接口.是文件(__file__) == True
        assert isinstance(系统接口.绝对路径("."), str)
        
        路径 = 系统接口.连接路径("a", "b", "c.txt")
        assert "a" in 路径 and "b" in 路径 and "c.txt" in 路径
        assert 系统接口.取目录名("/a/b/c.txt").endswith("b")
        assert 系统接口.取文件名("/a/b/c.txt") == "c.txt"
        assert 系统接口.取文件扩展名("c.txt") == ".txt"
        assert 系统接口.取文件名无扩展("c.txt") == "c"
        
        # 目录操作
        临时目录 = tempfile.mkdtemp()
        子目录 = 系统接口.连接路径(临时目录, "子目录")
        系统接口.创建目录(子目录)
        assert 系统接口.是目录(子目录)
        列表 = 系统接口.列出目录(临时目录)
        assert "子目录" in 列表
        系统接口.删除目录(子目录)
        
        # 进程信息
        assert isinstance(系统接口.进程ID(), int)
        assert 系统接口.进程ID() > 0
        assert isinstance(系统接口.获取命令行参数(), list)
        
        # 平台信息
        assert 系统接口.操作系统() in ["Windows", "Linux", "Darwin"]
        assert isinstance(系统接口.Python版本(), str)
        assert 系统接口.是否Windows() == True or 系统接口.是否Linux() == True or 系统接口.是否Mac() == True
        
        # 用户信息
        assert len(系统接口.用户主目录()) > 0
        assert len(系统接口.临时目录()) > 0
        
        # 系统常量
        assert 系统接口.路径分隔符() in ['\\', '/']
        assert isinstance(系统接口.CPU核心数(), int)
        assert 系统接口.CPU核心数() >= 1
        
        # 清理
        import shutil
        shutil.rmtree(临时目录)
        
        结果.记录通过("系统接口")
    except Exception as e:
        结果.记录失败("系统接口", str(e))


def 测试_外部命令(结果: 测试结果):
    print("\n📦 外部命令")
    try:
        import 外部命令
        
        # 执行简单命令
        if os.name == 'nt':
            cmd结果 = 外部命令.执行命令("echo hello")
            assert cmd结果.是否成功 == True
            assert "hello" in cmd结果.标准输出
        else:
            cmd结果 = 外部命令.执行命令(["echo", "hello"])
            assert cmd结果.是否成功 == True
            assert "hello" in cmd结果.标准输出
        
        # 命令是否成功
        assert 外部命令.命令是否成功("echo test") == True
        
        # 获取输出
        输出 = 外部命令.执行命令并获取输出("echo test_output")
        assert "test_output" in 输出
        
        # 命令存在检查
        assert isinstance(外部命令.命令存在("python"), bool)
        
        结果.记录通过("外部命令")
    except Exception as e:
        结果.记录失败("外部命令", str(e))


def 测试_参数解析(结果: 测试结果):
    print("\n📦 参数解析")
    try:
        import 参数解析
        
        # 基本测试
        解析器 = 参数解析.参数解析器(描述="测试程序", 版本="1.0.0")
        解析器.添加位置参数("文件名", 描述="输入文件")
        解析器.添加参数("--输出", 短名称="o", 描述="输出文件")
        解析器.添加参数("--详细", 短名称="v", 标志=True, 描述="详细模式")
        解析器.添加参数("--级别", 类型=int, 默认值=3, 描述="级别")
        
        # 解析测试
        参数 = 解析器.解析(["input.txt", "-o", "out.txt", "-v", "--级别", "5"])
        assert 参数["文件名"] == "input.txt"
        assert 参数["输出"] == "out.txt"
        assert 参数["详细"] == True
        assert 参数["级别"] == 5
        
        # 帮助文本
        帮助 = 解析器.帮助文本()
        assert "测试程序" in 帮助
        
        # 简单解析
        结果2 = 参数解析.简单解析([
            {'名称': '文件', '描述': '输入文件'},
            {'名称': '--输出', '短名称': '-o', '描述': '输出文件'},
        ], ["data.txt"])
        assert 结果2["文件"] == "data.txt"
        
        结果.记录通过("参数解析")
    except Exception as e:
        结果.记录失败("参数解析", str(e))


def 测试_复制(结果: 测试结果):
    print("\n📦 复制")
    try:
        import 复制
        
        # 浅复制
        原始 = [1, 2, [3, 4]]
        浅拷贝 = 复制.浅复制(原始)
        assert 浅拷贝 == 原始
        assert 浅拷贝 is not 原始
        assert 浅拷贝[2] is 原始[2]  # 浅复制，嵌套列表同一引用
        
        # 深复制
        深拷贝 = 复制.深复制(原始)
        assert 深拷贝 == 原始
        assert 深拷贝[2] is not 原始[2]  # 深复制，嵌套列表不同引用
        
        # 便捷函数
        拷贝 = 复制.复制(原始)
        assert 拷贝 == 原始
        
        深 = 复制.复制(原始, 深=True)
        assert 深 == 原始
        assert 深[2] is not 原始[2]
        
        结果.记录通过("复制")
    except Exception as e:
        结果.记录失败("复制", str(e))


def 测试_时间(结果: 测试结果):
    print("\n📦 时间")
    try:
        import 时间
        
        # 时间戳
        assert isinstance(时间.时间戳(), float)
        assert isinstance(时间.时间戳毫秒(), int)
        assert isinstance(时间.时间戳纳秒(), int)
        
        # 休眠
        开始 = 时间.性能计数器()
        时间.休眠(0.01)
        耗时 = 时间.性能计数器() - 开始
        assert 耗时 >= 0.005
        
        # 性能计数器
        t1 = 时间.性能计数器()
        time.sleep(0.005)
        t2 = 时间.性能计数器()
        assert t2 > t1
        
        # 单调时间
        assert isinstance(时间.单调时间(), float)
        
        # 测量执行时间
        def 测试函数():
            sum(range(1000))
            return 42
        
        返回值, 耗时 = 时间.测量执行时间(测试函数)
        assert 返回值 == 42
        assert 耗时 >= 0
        
        # 格式化时间
        格式化结果 = 时间.格式化时间("%Y-%m-%d")
        assert len(格式化结果) == 10
        
        # 秒表
        秒表 = 时间.秒表()
        time.sleep(0.01)
        assert 秒表.读取() >= 0.005
        秒表.停止()
        assert 秒表.读取() >= 0.005
        
        秒表2 = 时间.创建秒表()
        assert 秒表2 is not None
        
        结果.记录通过("时间")
    except Exception as e:
        结果.记录失败("时间", str(e))


def 测试_文件匹配(结果: 测试结果):
    print("\n📦 文件匹配")
    try:
        import 文件匹配
        
        # 创建临时目录
        临时目录 = tempfile.mkdtemp()
        try:
            # 创建测试文件
            for 名称 in ["a.txt", "b.txt", "c.py", "d.json", "子目录/e.txt"]:
                路径 = os.path.join(临时目录, 名称)
                os.makedirs(os.path.dirname(路径), exist_ok=True)
                with open(路径, 'w') as f:
                    f.write("test")
            
            # 测试匹配（非递归）
            txt文件 = 文件匹配.匹配文件("*.txt", 目录=临时目录)
            assert len(txt文件) == 2  # a.txt, b.txt
            
            # 测试匹配（递归）
            txt文件递归 = 文件匹配.匹配文件("**/*.txt", 递归=True, 目录=临时目录)
            assert len(txt文件递归) == 3  # a.txt, b.txt, 子目录/e.txt
            
            py文件 = 文件匹配.查找所有Python文件(临时目录, 递归=True)
            assert len(py文件) == 1
            
            json文件 = 文件匹配.查找所有JSON文件(临时目录)
            assert len(json文件) == 1
            
            # 名称匹配
            assert 文件匹配.名称匹配("test.txt", "*.txt") == True
            assert 文件匹配.名称匹配("test.py", "*.txt") == False
            assert 文件匹配.名称匹配忽略大小写("Test.TXT", "*.txt") == True
            
            # 过滤列表
            列表 = ["a.txt", "b.py", "c.txt", "d.json"]
            过滤结果 = 文件匹配.过滤列表(列表, "*.txt")
            assert 过滤结果 == ["a.txt", "c.txt"]
            
            # 迭代匹配
            迭代结果 = list(文件匹配.迭代匹配("*.txt", 目录=临时目录))
            assert len(迭代结果) == 2
            
        finally:
            import shutil
            shutil.rmtree(临时目录)
        
        结果.记录通过("文件匹配")
    except Exception as e:
        结果.记录失败("文件匹配", str(e))


def 测试_对象序列化(结果: 测试结果):
    print("\n📦 对象序列化")
    try:
        import 对象序列化
        
        原始数据 = {"姓名": "张三", "年龄": 25, "列表": [1, 2, 3], "嵌套": {"a": 1}}
        
        # pickle序列化
        字节数据 = 对象序列化.序列化(原始数据)
        assert isinstance(字节数据, bytes)
        恢复 = 对象序列化.反序列化(字节数据)
        assert 恢复 == 原始数据
        assert 恢复 is not 原始数据
        
        # 文件保存加载
        临时文件 = tempfile.mktemp(suffix=".pkl")
        try:
            对象序列化.保存到文件(原始数据, 临时文件)
            加载 = 对象序列化.从文件加载(临时文件)
            assert 加载 == 原始数据
        finally:
            if os.path.exists(临时文件):
                os.unlink(临时文件)
        
        # 字符串序列化
        字符串 = 对象序列化.序列化为字符串(原始数据)
        assert isinstance(字符串, str)
        恢复2 = 对象序列化.从字符串反序列化(字符串)
        assert 恢复2 == 原始数据
        
        # 深复制
        深拷贝 = 对象序列化.深复制(原始数据)
        assert 深拷贝 == 原始数据
        assert 深拷贝["列表"] is not 原始数据["列表"]
        
        # JSON
        json_str = 对象序列化.JSON序列化(原始数据, 缩进=2)
        assert "张三" in json_str
        json_obj = 对象序列化.JSON反序列化(json_str)
        assert json_obj["姓名"] == "张三"
        
        结果.记录通过("对象序列化")
    except Exception as e:
        结果.记录失败("对象序列化", str(e))


def 测试_美化输出(结果: 测试结果):
    print("\n📦 美化输出")
    try:
        import 美化输出
        
        测试数据 = {
            "姓名": "张三",
            "年龄": 25,
            "技能": ["Python", "Java", "C++"],
            "地址": {"城市": "北京", "区": "朝阳区"}
        }
        
        # 美化输出
        输出 = 美化输出.美化输出(测试数据)
        assert "张三" in 输出
        assert "Python" in 输出
        
        # 美化JSON
        json_str = 美化输出.美化JSON(测试数据, 缩进=2)
        assert '"姓名"' in json_str
        assert '"张三"' in json_str
        
        # 表格格式化
        表格数据 = [
            ["张三", 25, "北京"],
            ["李四", 30, "上海"],
            ["王五", 28, "广州"],
        ]
        表格 = 美化输出.格式化表格(表格数据, 列标题=["姓名", "年龄", "城市"])
        assert "姓名" in 表格
        assert "张三" in 表格
        assert "北京" in 表格
        
        # XML美化
        xml = "<root><item>1</item><item>2</item></root>"
        美化XML = 美化输出.美化XML(xml)
        assert "root" in 美化XML
        
        结果.记录通过("美化输出")
    except Exception as e:
        结果.记录失败("美化输出", str(e))


def 测试_枚举(结果: 测试结果):
    print("\n📦 枚举")
    try:
        import 枚举
        
        # 定义枚举
        class 颜色(枚举.枚举):
            红色 = 1
            绿色 = 2
            蓝色 = 3
        
        # 基本使用
        assert 颜色.红色.值 == 1
        assert 颜色.绿色.名称 == "绿色"
        assert 颜色.蓝色.值 == 3
        
        # 成员列表
        assert 颜色.成员数量() == 3
        assert "红色" in 颜色.所有名称()
        assert 2 in 颜色.所有值()
        
        # 从名称/值获取
        assert 颜色.从名称获取("红色") == 颜色.红色
        assert 颜色.从值获取(2) == 颜色.绿色
        assert 颜色.从名称获取("不存在") is None
        assert 颜色.从值获取(999) is None
        
        # 包含检查
        assert 颜色.包含名称("红色") == True
        assert 颜色.包含名称("黄色") == False
        assert 颜色.包含值(1) == True
        assert 颜色.包含值(999) == False
        
        # 导航
        assert 颜色.红色.下一个() == 颜色.绿色
        assert 颜色.绿色.下一个() == 颜色.蓝色
        assert 颜色.蓝色.下一个() is None
        assert 颜色.绿色.上一个() == 颜色.红色
        assert 颜色.红色.上一个() is None
        
        # 转字典
        d = 颜色.到字典()
        assert d == {"红色": 1, "绿色": 2, "蓝色": 3}
        
        # 动态创建
        方向 = 枚举.创建枚举("方向", {"上": 1, "下": 2, "左": 3, "右": 4})
        assert 方向.上.值 == 1
        assert 方向.右.值 == 4
        
        # 快速创建整数枚举
        等级 = 枚举.创建整数枚举("等级", ["初级", "中级", "高级"])
        assert 等级.初级.值 == 1
        assert 等级.高级.值 == 3
        
        结果.记录通过("枚举")
    except Exception as e:
        结果.记录失败("枚举", str(e))


def 测试_高级文件(结果: 测试结果):
    print("\n📦 高级文件")
    try:
        import 高级文件
        
        临时目录 = tempfile.mkdtemp()
        try:
            # 创建测试文件和目录
            文件1 = os.path.join(临时目录, "file1.txt")
            文件2 = os.path.join(临时目录, "file2.txt")
            子目录 = os.path.join(临时目录, "subdir")
            os.makedirs(子目录)
            
            with open(文件1, 'w') as f:
                f.write("内容1")
            with open(文件2, 'w') as f:
                f.write("内容2")
            
            # 复制文件
            复制文件 = os.path.join(临时目录, "copy.txt")
            高级文件.复制文件(文件1, 复制文件)
            assert os.path.exists(复制文件)
            
            # 复制目录
            复制目录路径 = os.path.join(临时目录, "subdir_copy")
            with open(os.path.join(子目录, "a.txt"), 'w') as f:
                f.write("a")
            高级文件.复制目录(子目录, 复制目录路径)
            assert os.path.isdir(复制目录路径)
            
            # 移动
            移动目标 = os.path.join(临时目录, "moved.txt")
            高级文件.移动(复制文件, 移动目标)
            assert os.path.exists(移动目标)
            assert not os.path.exists(复制文件)
            
            # 磁盘使用情况
            磁盘信息 = 高级文件.磁盘使用情况(临时目录)
            assert "总空间" in 磁盘信息
            assert "可用空间" in 磁盘信息
            assert 磁盘信息["总空间"] > 0
            
            # 目录大小
            大小 = 高级文件.目录大小(临时目录)
            assert 大小 > 0
            
            # 查找命令
            python路径 = 高级文件.查找命令("python")
            assert python路径 is not None
            assert 高级文件.命令存在("python") == True
            
            # 文件树
            树 = 高级文件.文件树(临时目录, 显示大小=False)
            assert "file1.txt" in 树
            assert "subdir" in 树
            
            # 归档
            归档文件 = os.path.join(临时目录, "archive")
            生成的归档 = 高级文件.归档(子目录, 归档文件, "zip")
            assert os.path.exists(生成的归档)
            
            # 解压
            解压目录 = os.path.join(临时目录, "unpacked")
            os.makedirs(解压目录)
            高级文件.解压(生成的归档, 解压目录)
            assert os.path.exists(os.path.join(解压目录, "a.txt"))
            
        finally:
            import shutil
            shutil.rmtree(临时目录)
        
        结果.记录通过("高级文件")
    except Exception as e:
        结果.记录失败("高级文件", str(e))


def 测试_压缩(结果: 测试结果):
    print("\n📦 压缩")
    try:
        import 压缩
        
        临时目录 = tempfile.mkdtemp()
        try:
            # 创建测试文件
            源文件 = os.path.join(临时目录, "test.txt")
            with open(源文件, 'w', encoding='utf-8') as f:
                f.write("Hello World!\n" * 100)
            
            # ZIP压缩
            zip文件 = os.path.join(临时目录, "test.zip")
            压缩.创建ZIP(源文件, zip文件)
            assert 压缩.是ZIP文件(zip文件) == True
            
            # 列出ZIP内容
            内容 = 压缩.列出ZIP内容(zip文件)
            assert len(内容) == 1
            assert 内容[0]['文件名'] == "test.txt"
            
            # 读取ZIP中的文件
            内容字节 = 压缩.读取ZIP文件(zip文件, "test.txt")
            assert b"Hello World" in 内容字节
            
            # 检查文件存在
            assert 压缩.ZIP文件存在(zip文件, "test.txt") == True
            assert 压缩.ZIP文件存在(zip文件, "nonexist") == False
            
            # 添加到ZIP
            额外文件 = os.path.join(临时目录, "extra.txt")
            with open(额外文件, 'w') as f:
                f.write("extra")
            压缩.添加到ZIP(zip文件, 额外文件)
            assert len(压缩.列出ZIP内容(zip文件)) == 2
            
            # 解压ZIP
            解压目录 = os.path.join(临时目录, "zip_extracted")
            os.makedirs(解压目录)
            压缩.解压ZIP(zip文件, 解压目录)
            assert os.path.exists(os.path.join(解压目录, "test.txt"))
            
            # GZIP
            gz文件 = os.path.join(临时目录, "test.txt.gz")
            压缩.GZIP压缩(源文件, gz文件)
            assert os.path.exists(gz文件)
            
            gz解压文件 = os.path.join(临时目录, "test_gz.txt")
            压缩.GZIP解压(gz文件, gz解压文件)
            with open(gz解压文件, 'r') as f:
                assert "Hello World" in f.read()
            
            # 内存压缩
            原始 = "测试压缩数据" * 100
            压缩字节 = 压缩.压缩字符串(原始)
            assert len(压缩字节) < len(原始.encode('utf-8'))
            解压文本 = 压缩.解压字符串(压缩字节)
            assert 解压文本 == 原始
            
            # CRC32
            crc = 压缩.CRC32(b"test data")
            assert isinstance(crc, int)
            assert crc > 0
            
            # Adler32
            adler = 压缩.Adler32(b"test data")
            assert isinstance(adler, int)
            assert adler > 0
            
        finally:
            import shutil
            shutil.rmtree(临时目录)
        
        结果.记录通过("压缩")
    except Exception as e:
        结果.记录失败("压缩", str(e))


def 测试_文本差异(结果: 测试结果):
    print("\n📦 文本差异")
    try:
        import 文本差异
        
        文本1 = """第一行
第二行
第三行
第四行
第五行"""
        
        文本2 = """第一行
第二行修改
第三行
新插入的行
第五行
第六行"""
        
        # 比较文本
        diff = 文本差异.比较文本(文本1, 文本2)
        assert isinstance(diff, list)
        assert len(diff) > 0
        
        # 差异字符串
        diff_str = 文本差异.差异字符串(文本1, 文本2)
        assert "---" in diff_str
        assert "+++" in diff_str
        
        # 相似度
        相似度 = 文本差异.相似度(文本1, 文本2)
        assert 0 < 相似度 < 1
        
        # 行相似度
        行1 = 文本1.splitlines()
        行2 = 文本2.splitlines()
        行相似度 = 文本差异.行相似度(行1, 行2)
        assert 0 < 行相似度 < 1
        
        # 最相似
        候选 = ["apple", "apples", "banana", "orange"]
        相似列表 = 文本差异.查找最相似("appla", 候选, 阈值=0.5)
        assert len(相似列表) > 0
        assert 相似列表[0][0] in ["apple", "apples"]
        
        最相似 = 文本差异.字符串最相似("appla", 候选)
        assert 最相似 is not None
        
        # 逐行比较
        比较结果 = 文本差异.比较行(行1, 行2)
        assert len(比较结果) > 0
        操作类型 = [r[0] for r in 比较结果]
        assert "相等" in 操作类型
        
        # 快速比较
        快速结果 = 文本差异.快速比较(文本1, 文本2)
        assert "相似度" in 快速结果
        assert "新增行数" in 快速结果
        assert "删除行数" in 快速结果
        assert 0 < 快速结果["相似度"] < 1
        
        # HTML差异
        html = 文本差异.HTML差异(文本1, 文本2)
        assert "<html" in html.lower() or "<table" in html.lower()
        
        结果.记录通过("文本差异")
    except Exception as e:
        结果.记录失败("文本差异", str(e))


def 主程序():
    print("=" * 60)
    print("🧪 新增模块测试 - SQLite + 补全方案")
    print("=" * 60)
    
    结果 = 测试结果()
    
    测试_SQLite数据库(结果)
    测试_系统接口(结果)
    测试_外部命令(结果)
    测试_参数解析(结果)
    测试_复制(结果)
    测试_时间(结果)
    测试_文件匹配(结果)
    测试_对象序列化(结果)
    测试_美化输出(结果)
    测试_枚举(结果)
    测试_高级文件(结果)
    测试_压缩(结果)
    测试_文本差异(结果)
    
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    print(f"✅ 通过: {结果.通过}")
    print(f"❌ 失败: {结果.失败}")
    print(f"📈 通过率: {(结果.通过 / (结果.通过 + 结果.失败) * 100) if (结果.通过 + 结果.失败) > 0 else 0:.1f}%")
    
    if 结果.失败详情:
        print("\n❌ 失败详情：")
        for 名称, 错误 in 结果.失败详情:
            print(f"  - {名称}: {错误}")
    
    print("\n" + "=" * 60)
    return 结果.失败 == 0


if __name__ == "__main__":
    成功 = 主程序()
    sys.exit(0 if 成功 else 1)

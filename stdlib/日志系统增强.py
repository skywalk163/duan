"""
日志系统增强模块 - 分级、滚动、格式化

提供增强的日志功能，包括：
- 日志分级（DEBUG, INFO, WARNING, ERROR, CRITICAL）
- 滚动日志（按大小、按时间）
- 多种输出格式
- 日志过滤
- 自定义处理器
"""
import logging
import logging.handlers
import sys
import os
from typing import Optional, Dict, Any


class 日志级别:
    """日志级别常量"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    
    级别名称 = {
        DEBUG: 'DEBUG',
        INFO: 'INFO',
        WARNING: 'WARNING',
        ERROR: 'ERROR',
        CRITICAL: 'CRITICAL'
    }


class 日志格式化器:
    """日志格式化器"""
    
    @staticmethod
    def 创建标准格式(包含时间: bool = True, 包含级别: bool = True, 
                      包含模块: bool = True, 包含线程: bool = False) -> logging.Formatter:
        """创建标准日志格式"""
        格式部分 = []
        
        if 包含时间:
            格式部分.append('%(asctime)s')
        if 包含级别:
            格式部分.append('%(levelname)s')
        if 包含模块:
            格式部分.append('%(name)s')
        if 包含线程:
            格式部分.append('%(threadName)s')
        
        格式部分.append('%(message)s')
        
        return logging.Formatter(' | '.join(格式部分))
    
    @staticmethod
    def 创建JSON格式() -> logging.Formatter:
        """创建JSON格式"""
        return logging.Formatter(
            '{"时间":"%(asctime)s","级别":"%(levelname)s","模块":"%(name)s","消息":"%(message)s"}'
        )
    
    @staticmethod
    def 创建简洁格式() -> logging.Formatter:
        """创建简洁格式"""
        return logging.Formatter('%(levelname)s: %(message)s')
    
    @staticmethod
    def 创建详细格式() -> logging.Formatter:
        """创建详细格式"""
        return logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s'
        )


class 日志处理器:
    """日志处理器工厂"""
    
    @staticmethod
    def 创建控制台处理器(级别: int = logging.DEBUG, 
                           格式化器: logging.Formatter = None) -> logging.Handler:
        """创建控制台处理器"""
        处理器 = logging.StreamHandler(sys.stdout)
        处理器.setLevel(级别)
        
        if 格式化器:
            处理器.setFormatter(格式化器)
        
        return 处理器
    
    @staticmethod
    def 创建文件处理器(文件名: str, 级别: int = logging.DEBUG,
                        格式化器: logging.Formatter = None, 
                        编码: str = 'utf-8') -> logging.Handler:
        """创建文件处理器"""
        处理器 = logging.FileHandler(文件名, encoding=编码)
        处理器.setLevel(级别)
        
        if 格式化器:
            处理器.setFormatter(格式化器)
        
        return 处理器
    
    @staticmethod
    def 创建滚动文件处理器(文件名: str, 级别: int = logging.DEBUG,
                           格式化器: logging.Formatter = None,
                           最大大小: int = 1024 * 1024 * 10,
                           备份数量: int = 5,
                           编码: str = 'utf-8') -> logging.handlers.RotatingFileHandler:
        """创建按大小滚动的文件处理器"""
        处理器 = logging.handlers.RotatingFileHandler(
            文件名, maxBytes=最大大小, backupCount=备份数量, encoding=编码
        )
        处理器.setLevel(级别)
        
        if 格式化器:
            处理器.setFormatter(格式化器)
        
        return 处理器
    
    @staticmethod
    def 创建时间滚动处理器(文件名: str, 级别: int = logging.DEBUG,
                           格式化器: logging.Formatter = None,
                           间隔: str = 'D',
                           备份数量: int = 7,
                           编码: str = 'utf-8') -> logging.handlers.TimedRotatingFileHandler:
        """创建按时间滚动的文件处理器"""
        处理器 = logging.handlers.TimedRotatingFileHandler(
            文件名, when=间隔, backupCount=备份数量, encoding=编码
        )
        处理器.setLevel(级别)
        
        if 格式化器:
            处理器.setFormatter(格式化器)
        
        return 处理器


class 日志过滤器:
    """日志过滤器"""
    
    def __init__(self, 允许级别列表: list = None, 拒绝级别列表: list = None,
                 包含关键词: list = None, 排除关键词: list = None):
        self._允许级别列表 = 允许级别列表
        self._拒绝级别列表 = 拒绝级别列表
        self._包含关键词 = 包含关键词
        self._排除关键词 = 排除关键词
    
    def filter(self, 记录: logging.LogRecord) -> bool:
        """过滤日志记录"""
        if self._允许级别列表 and 记录.levelno not in self._允许级别列表:
            return False
        
        if self._拒绝级别列表 and 记录.levelno in self._拒绝级别列表:
            return False
        
        if self._包含关键词:
            包含 = any(关键词 in 记录.getMessage() for 关键词 in self._包含关键词)
            if not 包含:
                return False
        
        if self._排除关键词:
            for 关键词 in self._排除关键词:
                if 关键词 in 记录.getMessage():
                    return False
        
        return True


class 日志记录器:
    """增强的日志记录器"""
    
    def __init__(self, 名称: str = __name__, 级别: int = logging.DEBUG):
        self._记录器 = logging.getLogger(名称)
        self._记录器.setLevel(级别)
        self._记录器.propagate = False
    
    def 添加处理器(self, 处理器: logging.Handler):
        """添加处理器"""
        self._记录器.addHandler(处理器)
    
    def 添加过滤器(self, 过滤器: logging.Filter):
        """添加过滤器"""
        self._记录器.addFilter(过滤器)
    
    def 设置级别(self, 级别: int):
        """设置日志级别"""
        self._记录器.setLevel(级别)
    
    def 调试(self, 消息: str, **额外信息):
        """记录DEBUG级别日志"""
        self._记录器.debug(消息, extra=额外信息)
    
    def 信息(self, 消息: str, **额外信息):
        """记录INFO级别日志"""
        self._记录器.info(消息, extra=额外信息)
    
    def 警告(self, 消息: str, **额外信息):
        """记录WARNING级别日志"""
        self._记录器.warning(消息, extra=额外信息)
    
    def 错误(self, 消息: str, **额外信息):
        """记录ERROR级别日志"""
        self._记录器.error(消息, extra=额外信息)
    
    def 严重(self, 消息: str, **额外信息):
        """记录CRITICAL级别日志"""
        self._记录器.critical(消息, extra=额外信息)
    
    def 异常(self, 消息: str, **额外信息):
        """记录异常日志"""
        self._记录器.exception(消息, extra=额外信息)
    
    def 记录(self, 级别: int, 消息: str, **额外信息):
        """记录指定级别日志"""
        self._记录器.log(级别, 消息, extra=额外信息)
    
    def 获取记录器(self) -> logging.Logger:
        """获取原始记录器"""
        return self._记录器


class 日志管理器:
    """日志管理器"""
    
    def __init__(self):
        self._记录器映射: Dict[str, 日志记录器] = {}
        self._全局级别 = logging.DEBUG
    
    def 设置全局级别(self, 级别: int):
        """设置全局日志级别"""
        self._全局级别 = 级别
    
    def 获取记录器(self, 名称: str) -> 日志记录器:
        """获取或创建日志记录器"""
        if 名称 not in self._记录器映射:
            self._记录器映射[名称] = 日志记录器(名称, self._全局级别)
        return self._记录器映射[名称]
    
    def 配置控制台日志(self, 级别: int = logging.INFO,
                          格式化器: logging.Formatter = None):
        """配置控制台日志"""
        格式化器 = 格式化器 or 日志格式化器.创建标准格式()
        处理器 = 日志处理器.创建控制台处理器(级别, 格式化器)
        
        for 记录器 in self._记录器映射.values():
            记录器.添加处理器(处理器)
    
    def 配置文件日志(self, 文件名: str, 级别: int = logging.DEBUG,
                      格式化器: logging.Formatter = None,
                      滚动: bool = True, 最大大小: int = 1024 * 1024 * 10,
                      备份数量: int = 5):
        """配置文件日志"""
        格式化器 = 格式化器 or 日志格式化器.创建详细格式()
        
        if 滚动:
            处理器 = 日志处理器.创建滚动文件处理器(
                文件名, 级别, 格式化器, 最大大小, 备份数量
            )
        else:
            处理器 = 日志处理器.创建文件处理器(文件名, 级别, 格式化器)
        
        for 记录器 in self._记录器映射.values():
            记录器.添加处理器(处理器)
    
    def 配置时间滚动日志(self, 文件名: str, 级别: int = logging.DEBUG,
                          格式化器: logging.Formatter = None,
                          间隔: str = 'D', 备份数量: int = 7):
        """配置时间滚动日志"""
        格式化器 = 格式化器 or 日志格式化器.创建详细格式()
        处理器 = 日志处理器.创建时间滚动处理器(
            文件名, 级别, 格式化器, 间隔, 备份数量
        )
        
        for 记录器 in self._记录器映射.values():
            记录器.添加处理器(处理器)
    
    def 添加全局过滤器(self, 过滤器: logging.Filter):
        """添加全局过滤器"""
        for 记录器 in self._记录器映射.values():
            记录器.添加过滤器(过滤器)


# 便捷函数
def 获取日志记录器(名称: str = __name__) -> 日志记录器:
    """获取日志记录器"""
    return 日志记录器(名称)


def 创建日志记录器(名称: str = __name__, 级别: int = logging.DEBUG,
                    控制台输出: bool = True, 文件输出: bool = False,
                    文件名: str = 'app.log') -> 日志记录器:
    """创建配置好的日志记录器"""
    记录器 = 日志记录器(名称, 级别)
    
    if 控制台输出:
        格式化器 = 日志格式化器.创建标准格式()
        处理器 = 日志处理器.创建控制台处理器(级别, 格式化器)
        记录器.添加处理器(处理器)
    
    if 文件输出:
        格式化器 = 日志格式化器.创建详细格式()
        处理器 = 日志处理器.创建滚动文件处理器(文件名, 级别, 格式化器)
        记录器.添加处理器(处理器)
    
    return 记录器


def 快速配置(级别: int = logging.INFO, 控制台: bool = True, 
              文件: bool = False, 文件名: str = 'app.log'):
    """快速配置日志"""
    logging.basicConfig(
        level=级别,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        handlers=[]
    )
    
    处理器列表 = []
    
    if 控制台:
        处理器列表.append(logging.StreamHandler(sys.stdout))
    
    if 文件:
        处理器列表.append(logging.handlers.RotatingFileHandler(
            文件名, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
        ))
    
    logging.getLogger().handlers = 处理器列表


class 日志上下文管理器:
    """日志上下文管理器"""
    
    def __init__(self, 记录器: 日志记录器, 消息: str, 级别: int = logging.INFO):
        self._记录器 = 记录器
        self._消息 = 消息
        self._级别 = 级别
    
    def __enter__(self):
        """进入上下文"""
        self._记录器.记录(self._级别, f'开始: {self._消息}')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        if exc_type:
            self._记录器.错误(f'结束: {self._消息} - 异常: {exc_val}')
        else:
            self._记录器.记录(self._级别, f'完成: {self._消息}')


def 日志上下文(记录器: 日志记录器, 消息: str, 级别: int = logging.INFO) -> 日志上下文管理器:
    """创建日志上下文管理器"""
    return 日志上下文管理器(记录器, 消息, 级别)


class 结构化日志:
    """结构化日志工具"""
    
    @staticmethod
    def 创建结构化消息(事件: str, **数据) -> str:
        """创建结构化消息"""
        消息部分 = [f'事件={事件}']
        for 键, 值 in 数据.items():
            消息部分.append(f'{键}={值}')
        return ' '.join(消息部分)
    
    @staticmethod
    def 创建API日志(方法: str, 路径: str, 状态码: int, 耗时: float) -> str:
        """创建API日志"""
        return f'API {方法} {路径} {状态码} {耗时:.3f}秒'
    
    @staticmethod
    def 创建数据库日志(操作: str, 表名: str, 影响行数: int, 耗时: float) -> str:
        """创建数据库日志"""
        return f'DB {操作} {表名} 影响={影响行数} {耗时:.3f}秒'
    
    @staticmethod
    def 创建性能日志(操作: str, 耗时: float, 内存: float = None) -> str:
        """创建性能日志"""
        消息 = f'性能 {操作} 耗时={耗时:.3f}秒'
        if 内存:
            消息 += f' 内存={内存:.2f}MB'
        return 消息


# 全局日志管理器实例
_全局日志管理器 = 日志管理器()


def 获取全局日志管理器() -> 日志管理器:
    """获取全局日志管理器"""
    return _全局日志管理器


def 设置全局日志级别(级别: int):
    """设置全局日志级别"""
    _全局日志管理器.设置全局级别(级别)


def 配置全局日志(级别: int = logging.INFO, 控制台: bool = True,
                  文件: bool = False, 文件名: str = 'app.log'):
    """配置全局日志"""
    _全局日志管理器.设置全局级别(级别)
    
    if 控制台:
        _全局日志管理器.配置控制台日志(级别)
    
    if 文件:
        _全局日志管理器.配置文件日志(文件名, 级别)
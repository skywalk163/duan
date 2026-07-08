"""
审计日志模块 - 操作记录、追溯

提供审计日志功能，包括：
- 操作记录
- 变更追踪
- 审计查询
- 合规报告
"""
import time
import json
import hashlib
import os
from typing import Any, Callable, Dict, List, Optional


class 审计记录:
    """审计记录"""
    
    def __init__(self, 操作者: str, 操作: str, 目标: str, 
                 详情: Dict[str, Any] = None, 结果: str = '成功',
                 IP地址: str = '', 时间戳: float = None):
        self.操作者 = 操作者
        self.操作 = 操作
        self.目标 = 目标
        self.详情 = 详情 or {}
        self.结果 = 结果
        self.IP地址 = IP地址
        self.时间戳 = 时间戳 or time.time()
        self.记录ID = hashlib.sha256(
            f'{操作者}{操作}{目标}{self.时间戳}'.encode()
        ).hexdigest()[:16]
    
    def 到字典(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            '记录ID': self.记录ID,
            '操作者': self.操作者,
            '操作': self.操作,
            '目标': self.目标,
            '详情': self.详情,
            '结果': self.结果,
            'IP地址': self.IP地址,
            '时间戳': self.时间戳,
            '时间': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.时间戳))
        }
    
    def __repr__(self) -> str:
        return f'审计记录({self.操作者}, {self.操作}, {self.目标}, {self.结果})'


class 审计日志:
    """审计日志"""
    
    def __init__(self, 存储路径: str = None):
        self._记录列表: List[审计记录] = []
        self._存储路径 = 存储路径
        self._变更追踪: Dict[str, List[Dict[str, Any]]] = {}
        self._回调列表: List[Callable] = []
    
    def 记录(self, 操作者: str, 操作: str, 目标: str, 
             详情: Dict[str, Any] = None, 结果: str = '成功',
             IP地址: str = '') -> 审计记录:
        """记录操作"""
        记录 = 审计记录(操作者, 操作, 目标, 详情, 结果, IP地址)
        self._记录列表.append(记录)
        
        for 回调 in self._回调列表:
            try:
                回调(记录)
            except Exception:
                pass
        
        if self._存储路径:
            self._保存到文件(记录)
        
        return 记录
    
    def 追踪变更(self, 目标: str, 字段: str, 旧值: Any, 新值: Any, 操作者: str = ''):
        """追踪变更"""
        变更记录 = {
            '字段': 字段,
            '旧值': 旧值,
            '新值': 新值,
            '操作者': 操作者,
            '时间戳': time.time()
        }
        
        if 目标 not in self._变更追踪:
            self._变更追踪[目标] = []
        self._变更追踪[目标].append(变更记录)
        
        self.记录(操作者, '变更', 目标, 变更记录)
    
    def 获取变更历史(self, 目标: str) -> List[Dict[str, Any]]:
        """获取变更历史"""
        return self._变更追踪.get(目标, []).copy()
    
    def 查询(self, 操作者: str = None, 操作: str = None, 
              目标: str = None, 开始时间: float = None,
              结束时间: float = None, 结果: str = None) -> List[审计记录]:
        """查询审计记录"""
        过滤结果 = self._记录列表
        
        if 操作者:
            过滤结果 = [r for r in 过滤结果 if r.操作者 == 操作者]
        if 操作:
            过滤结果 = [r for r in 过滤结果 if r.操作 == 操作]
        if 目标:
            过滤结果 = [r for r in 过滤结果 if r.目标 == 目标]
        if 开始时间:
            过滤结果 = [r for r in 过滤结果 if r.时间戳 >= 开始时间]
        if 结束时间:
            过滤结果 = [r for r in 过滤结果 if r.时间戳 <= 结束时间]
        if 结果:
            过滤结果 = [r for r in 过滤结果 if r.结果 == 结果]
        
        return 过滤结果
    
    def 获取操作者活动(self, 操作者: str) -> List[审计记录]:
        """获取操作者所有活动"""
        return [r for r in self._记录列表 if r.操作者 == 操作者]
    
    def 获取目标历史(self, 目标: str) -> List[审计记录]:
        """获取目标操作历史"""
        return [r for r in self._记录列表 if r.目标 == 目标]
    
    def 获取失败操作(self) -> List[审计记录]:
        """获取所有失败操作"""
        return [r for r in self._记录列表 if r.结果 != '成功']
    
    def 统计操作次数(self) -> Dict[str, int]:
        """统计操作次数"""
        统计 = {}
        for 记录 in self._记录列表:
            统计[记录.操作] = 统计.get(记录.操作, 0) + 1
        return 统计
    
    def 统计操作者活动(self) -> Dict[str, int]:
        """统计操作者活动次数"""
        统计 = {}
        for 记录 in self._记录列表:
            统计[记录.操作者] = 统计.get(记录.操作者, 0) + 1
        return 统计
    
    def 注册回调(self, 回调函数: Callable):
        """注册回调函数"""
        self._回调列表.append(回调函数)
    
    def 总记录数(self) -> int:
        """获取总记录数"""
        return len(self._记录列表)
    
    def 清空(self):
        """清空记录"""
        self._记录列表 = []
        self._变更追踪 = {}
    
    def _保存到文件(self, 记录: 审计记录):
        """保存到文件"""
        try:
            with open(self._存储路径, 'a', encoding='utf-8') as f:
                f.write(json.dumps(记录.到字典(), ensure_ascii=False) + '\n')
        except Exception:
            pass
    
    def 从文件加载(self, 文件路径: str) -> int:
        """从文件加载记录"""
        加载数量 = 0
        try:
            with open(文件路径, 'r', encoding='utf-8') as f:
                for 行 in f:
                    try:
                        数据 = json.loads(行.strip())
                        记录 = 审计记录(
                            操作者=数据.get('操作者', ''),
                            操作=数据.get('操作', ''),
                            目标=数据.get('目标', ''),
                            详情=数据.get('详情', {}),
                            结果=数据.get('结果', '成功'),
                            IP地址=数据.get('IP地址', ''),
                            时间戳=数据.get('时间戳', time.time())
                        )
                        self._记录列表.append(记录)
                        加载数量 += 1
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            pass
        return 加载数量


class 审计装饰器:
    """审计装饰器"""
    
    def __init__(self, 审计日志实例: 审计日志):
        self._审计日志 = 审计日志实例
    
    def 记录操作(self, 操作名: str = None):
        """记录操作装饰器"""
        def 装饰器(函数):
            def 包装(*参数, **关键字参数):
                操作 = 操作名 or 函数.__name__
                操作者 = 关键字参数.pop('操作者', 'system')
                目标 = 关键字参数.pop('审计目标', '')
                
                try:
                    结果 = 函数(*参数, **关键字参数)
                    self._审计日志.记录(操作者, 操作, 目标, 结果='成功')
                    return 结果
                except Exception as e:
                    self._审计日志.记录(操作者, 操作, 目标, 
                                      详情={'异常': str(e)}, 结果='失败')
                    raise
            return 包装
        return 装饰器


class 合规报告生成器:
    """合规报告生成器"""
    
    def __init__(self, 审计日志实例: 审计日志):
        self._审计日志 = 审计日志实例
    
    def 生成操作统计报告(self) -> Dict[str, Any]:
        """生成操作统计报告"""
        return {
            '总操作数': self._审计日志.总记录数(),
            '操作统计': self._审计日志.统计操作次数(),
            '操作者统计': self._审计日志.统计操作者活动(),
            '失败操作数': len(self._审计日志.获取失败操作()),
        }
    
    def 生成安全审计报告(self) -> Dict[str, Any]:
        """生成安全审计报告"""
        失败操作 = self._审计日志.获取失败操作()
        
        return {
            '总操作数': self._审计日志.总记录数(),
            '失败操作数': len(失败操作),
            '失败率': len(失败操作) / max(self._审计日志.总记录数(), 1) * 100,
            '失败操作详情': [r.到字典() for r in 失败操作[:10]],
        }
    
    def 生成操作者报告(self, 操作者: str) -> Dict[str, Any]:
        """生成操作者报告"""
        活动 = self._审计日志.获取操作者活动(操作者)
        
        return {
            '操作者': 操作者,
            '总操作数': len(活动),
            '操作类型': list(set(r.操作 for r in 活动)),
            '操作目标': list(set(r.目标 for r in 活动)),
        }


# 便捷函数
def 创建审计日志(存储路径: str = None) -> 审计日志:
    """创建审计日志"""
    return 审计日志(存储路径)


def 创建合规报告生成器(审计日志实例: 审计日志) -> 合规报告生成器:
    """创建合规报告生成器"""
    return 合规报告生成器(审计日志实例)
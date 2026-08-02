"""
访问控制模块 - RBAC/ACL角色权限管理

提供权限管理功能，包括：
- 基于角色的访问控制（RBAC）
- 访问控制列表（ACL）
- 权限检查
- 角色继承
"""
from typing import Any, Callable, Dict, List, Optional, Set


class 权限:
    """权限定义"""
    
    def __init__(self, 名称: str, 描述: str = ''):
        self.名称 = 名称
        self.描述 = 描述
    
    def __repr__(self) -> str:
        return f'权限({self.名称})'
    
    def __hash__(self) -> int:
        return hash(self.名称)
    
    def __eq__(self, 其他) -> bool:
        if isinstance(其他, 权限):
            return self.名称 == 其他.名称
        if isinstance(其他, str):
            return self.名称 == 其他
        return False


class 角色:
    """角色定义"""
    
    def __init__(self, 名称: str, 描述: str = ''):
        self.名称 = 名称
        self.描述 = 描述
        self._权限集合: Set[str] = set()
        self._父角色集合: Set[str] = set()
    
    def 添加权限(self, 权限名: str):
        """添加权限"""
        self._权限集合.add(权限名)
    
    def 移除权限(self, 权限名: str) -> bool:
        """移除权限"""
        if 权限名 in self._权限集合:
            self._权限集合.discard(权限名)
            return True
        return False
    
    def 获取权限(self) -> Set[str]:
        """获取权限集合"""
        return self._权限集合.copy()
    
    def 添加父角色(self, 角色名: str):
        """添加父角色（继承）"""
        self._父角色集合.add(角色名)
    
    def 获取父角色(self) -> Set[str]:
        """获取父角色"""
        return self._父角色集合.copy()
    
    def 包含权限(self, 权限名: str) -> bool:
        """检查是否包含权限"""
        return 权限名 in self._权限集合
    
    def __repr__(self) -> str:
        return f'角色({self.名称})'


class RBAC管理器:
    """基于角色的访问控制管理器"""
    
    def __init__(self):
        self._角色字典: Dict[str, 角色] = {}
        self._用户角色映射: Dict[str, Set[str]] = {}
    
    def 创建角色(self, 名称: str, 描述: str = '') -> 角色:
        """创建角色"""
        新角色 = 角色(名称, 描述)
        self._角色字典[名称] = 新角色
        return 新角色
    
    def 获取角色(self, 名称: str) -> Optional[角色]:
        """获取角色"""
        return self._角色字典.get(名称)
    
    def 删除角色(self, 名称: str) -> bool:
        """删除角色"""
        if 名称 in self._角色字典:
            del self._角色字典[名称]
            for 用户角色集 in self._用户角色映射.values():
                用户角色集.discard(名称)
            return True
        return False
    
    def 给角色授权(self, 角色名: str, 权限名: str) -> bool:
        """给角色授权"""
        角色 = self.获取角色(角色名)
        if 角色:
            角色.添加权限(权限名)
            return True
        return False
    
    def 撤销角色权限(self, 角色名: str, 权限名: str) -> bool:
        """撤销角色权限"""
        角色 = self.获取角色(角色名)
        if 角色:
            return 角色.移除权限(权限名)
        return False
    
    def 添加角色继承(self, 子角色名: str, 父角色名: str) -> bool:
        """添加角色继承"""
        子角色 = self.获取角色(子角色名)
        if 子角色:
            子角色.添加父角色(父角色名)
            return True
        return False
    
    def 获取角色所有权限(self, 角色名: str, 已访问: Set[str] = None) -> Set[str]:
        """获取角色所有权限（含继承）"""
        if 已访问 is None:
            已访问 = set()
        
        if 角色名 in 已访问:
            return set()
        已访问.add(角色名)
        
        角色 = self.获取角色(角色名)
        if not 角色:
            return set()
        
        权限集合 = 角色.获取权限()
        
        for 父角色名 in 角色.获取父角色():
            权限集合.update(self.获取角色所有权限(父角色名, 已访问))
        
        return 权限集合
    
    def 分配用户角色(self, 用户ID: str, 角色名: str):
        """给用户分配角色"""
        if 用户ID not in self._用户角色映射:
            self._用户角色映射[用户ID] = set()
        self._用户角色映射[用户ID].add(角色名)
    
    def 移除用户角色(self, 用户ID: str, 角色名: str) -> bool:
        """移除用户角色"""
        if 用户ID in self._用户角色映射:
            self._用户角色映射[用户ID].discard(角色名)
            return True
        return False
    
    def 获取用户角色(self, 用户ID: str) -> Set[str]:
        """获取用户角色"""
        return self._用户角色映射.get(用户ID, set()).copy()
    
    def 获取用户权限(self, 用户ID: str) -> Set[str]:
        """获取用户所有权限"""
        权限集合 = set()
        for 角色名 in self.获取用户角色(用户ID):
            权限集合.update(self.获取角色所有权限(角色名))
        return 权限集合
    
    def 检查用户权限(self, 用户ID: str, 权限名: str) -> bool:
        """检查用户是否拥有权限"""
        return 权限名 in self.获取用户权限(用户ID)
    
    def 检查用户角色(self, 用户ID: str, 角色名: str) -> bool:
        """检查用户是否拥有角色"""
        return 角色名 in self.获取用户角色(用户ID)


class ACL规则:
    """ACL规则"""
    
    def __init__(self, 主体: str, 资源: str, 操作: str, 允许: bool = True):
        self.主体 = 主体
        self.资源 = 资源
        self.操作 = 操作
        self.允许 = 允许
    
    def 匹配(self, 主体: str, 资源: str, 操作: str) -> bool:
        """检查是否匹配"""
        return (self.主体 == 主体 or self.主体 == '*') and \
               (self.资源 == 资源 or self.资源 == '*') and \
               (self.操作 == 操作 or self.操作 == '*')


class ACL管理器:
    """访问控制列表管理器"""
    
    def __init__(self):
        self._规则列表: List[ACL规则] = []
        self._默认允许: bool = False
    
    def 设置默认策略(self, 允许: bool):
        """设置默认策略"""
        self._默认允许 = 允许
    
    def 添加规则(self, 主体: str, 资源: str, 操作: str, 允许: bool = True):
        """添加ACL规则"""
        self._规则列表.append(ACL规则(主体, 资源, 操作, 允许))
    
    def 移除规则(self, 主体: str, 资源: str, 操作: str) -> bool:
        """移除ACL规则"""
        for i, 规则 in enumerate(self._规则列表):
            if 规则.主体 == 主体 and 规则.资源 == 资源 and 规则.操作 == 操作:
                del self._规则列表[i]
                return True
        return False
    
    def 检查权限(self, 主体: str, 资源: str, 操作: str) -> bool:
        """检查权限"""
        for 规则 in self._规则列表:
            if 规则.匹配(主体, 资源, 操作):
                return 规则.允许
        return self._默认允许
    
    def 获取主体规则(self, 主体: str) -> List[ACL规则]:
        """获取主体所有规则"""
        return [r for r in self._规则列表 if r.主体 == 主体]
    
    def 获取资源规则(self, 资源: str) -> List[ACL规则]:
        """获取资源所有规则"""
        return [r for r in self._规则列表 if r.资源 == 资源]
    
    def 清空规则(self):
        """清空所有规则"""
        self._规则列表 = []


def 权限检查装饰器(管理器: RBAC管理器, 权限名: str):
    """权限检查装饰器"""
    def 装饰器(函数):
        def 包装(用户ID, *参数, **关键字参数):
            if not 管理器.检查用户权限(用户ID, 权限名):
                raise PermissionError(f'用户 {用户ID} 没有权限 {权限名}')
            return 函数(用户ID, *参数, **关键字参数)
        return 包装
    return 装饰器


def 角色检查装饰器(管理器: RBAC管理器, 角色名: str):
    """角色检查装饰器"""
    def 装饰器(函数):
        def 包装(用户ID, *参数, **关键字参数):
            if not 管理器.检查用户角色(用户ID, 角色名):
                raise PermissionError(f'用户 {用户ID} 没有角色 {角色名}')
            return 函数(用户ID, *参数, **关键字参数)
        return 包装
    return 装饰器


# 便捷函数
def 创建RBAC管理器() -> RBAC管理器:
    """创建RBAC管理器"""
    return RBAC管理器()


def 创建ACL管理器(默认允许: bool = False) -> ACL管理器:
    """创建ACL管理器"""
    管理器 = ACL管理器()
    管理器.设置默认策略(默认允许)
    return 管理器
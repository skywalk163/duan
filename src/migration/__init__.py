# -*- coding: utf-8 -*-
"""
段言代码迁移工具 (Duan Migration)

提供 v3.3 → v4.0 → v5.x 的代码迁移功能。
"""

from src.migration.v33_to_v40 import MigrationV33ToV40
from src.migration.v40_to_v50 import MigrationV40ToV50

__version__ = '1.1.0'
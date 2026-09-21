import os

# ==================== 配置区域 ====================

# 优先从环境变量读取 Cookie（部署到云服务器时更安全）
# 本地测试时可以把下面的默认值改成你的完整 Cookie
COOKIE = os.environ.get("ELECTRIC_COOKIE", "shiroJID=580988f4-dbeb-4e29-8247-acf11731c550")

# 宿舍参数（已根据你的抓包填写）
AREA_ID = "2408569690932133889"
BUILDING_CODE = "4"
FLOOR_CODE = "3"
ROOM_CODE = "26214"
PLATFORM = "YUNMA_WXAPP"

# 低电量预警阈值（度）
LOW_THRESHOLD = 10.0

# ==================================================

# 工具2 查询时间
def get_current_time():
    from datetime import datetime
    now = datetime.now()
    return f"当前时间是{now.strftime('%Y-%m-%d %H:%M:%S')}"
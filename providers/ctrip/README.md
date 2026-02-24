# Ctrip Provider

携程 (Ctrip) 网站自动化封装

## 功能

- ✅ 机票搜索
- 🚧 酒店搜索（开发中）

## 安装

```bash
pip install -r requirements.txt
playwright install chromium
```

## 使用示例

### 基础用法

```python
import asyncio
from providers.ctrip import CtripProvider

async def main():
    # 初始化Provider
    provider = CtripProvider()
    
    try:
        # 搜索航班
        flights = await provider.search_flights(
            origin="SHA",        # 上海
            destination="PEK",   # 北京
            date="2026-03-01"
        )
        
        # 打印结果
        for flight in flights[:5]:  # 只显示前5个
            print(f"{flight['airline']} {flight['flight_no']}")
            print(f"  出发: {flight['dep_time']} ({flight['dep_airport']})")
            print(f"  到达: {flight['arr_time']} ({flight['arr_airport']})")
            print(f"  价格: ¥{flight['price']}")
            print(f"  时长: {flight['duration']}")
            print()
            
    finally:
        await provider.close()

asyncio.run(main())
```

### 使用上下文管理器

```python
import asyncio
from providers.ctrip import CtripProvider

async def main():
    async with CtripProvider() as provider:
        flights = await provider.search_flights("SHA", "PEK", "2026-03-01")
        print(f"找到 {len(flights)} 个航班")

asyncio.run(main())
```

### 快捷函数

```python
import asyncio
from providers.ctrip import search_flights

async def main():
    flights = await search_flights("SHA", "PEK", "2026-03-01")
    for f in flights:
        print(f"{f['flight_no']}: ¥{f['price']}")

asyncio.run(main())
```

## 城市代码

常用城市代码：

| 城市 | 代码 |
|------|------|
| 北京 | PEK |
| 上海虹桥 | SHA |
| 上海浦东 | PVG |
| 广州 | CAN |
| 深圳 | SZX |
| 成都 | CTU |
| 杭州 | HGH |
| 西安 | XIY |

更多代码可在携程网站查找。

## 返回值格式

```python
{
    "airline": "中国东方航空",      # 航空公司
    "flight_no": "MU5101",         # 航班号
    "dep_time": "08:00",           # 出发时间
    "arr_time": "10:15",           # 到达时间
    "dep_airport": "SHA",          # 出发机场
    "arr_airport": "PEK",          # 到达机场
    "price": 850,                  # 价格（CNY）
    "duration": "2h 15m"           # 飞行时长
}
```

## 注意事项

1. **反爬机制**：携程可能有反爬措施，频繁请求可能导致IP被封
2. **页面结构**：页面结构变化可能导致选择器失效，需要及时更新
3. **登录状态**：搜索不需要登录，但预订需要（当前未实现预订功能）
4. **错误处理**：搜索失败时会自动截图保存到当前目录

## 调试

如果搜索失败，会生成截图文件 `ctrip_error_YYYYMMDD_HHMMSS.png`，可用于排查问题。

## 待办

- [ ] 酒店搜索
- [ ] 火车票搜索
- [ ] 价格趋势查询
- [ ] 多日期比价
- [ ] 代理池支持

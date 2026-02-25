# Ctrip Provider (携程)

**状态：火车票 ✅ 已测试 | 机票 ✅ 已测试**

## 功能

- ✅ **火车票搜索** - 已测试，可用
- ✅ **机票搜索** - 已测试，可用（需使用未来日期）

## 测试结果

### 火车票 (✅ 已验证)

```python
from providers.ctrip import CtripScraper, TrainQuery

scraper = CtripScraper()
query = TrainQuery(from_station='上海', to_station='杭州', date='2026-02-25')
result = scraper.search_train(query)

# 结果: 357 趟列车
# 首趟: Z4081, 01:28-02:51, 硬座 ¥24.5
```

### 机票 (✅ 已验证)

```python
from providers.ctrip import CtripScraper, FlightQuery

scraper = CtripScraper()
query = FlightQuery(from_code='SHA', to_code='BJS', date='2026-02-25')
result = scraper.search_flight(query)

# 结果: 117 个航班
# 首个: KN5956 - 中国联合航空
```

**注意**: 机票查询必须使用**未来日期**，过去日期会报错。

## 安装

```bash
pip install playwright
playwright install chromium
```

## 使用示例

### 火车票查询

```python
from providers.ctrip import CtripScraper, TrainQuery

scraper = CtripScraper()
try:
    query = TrainQuery(
        from_station='上海',
        to_station='杭州',
        date='2026-03-01'  # 必须是未来日期
    )
    result = scraper.search_train(query)
    print(f"找到 {result['total']} 趟列车")
    for train in result['trains'][:5]:
        print(f"{train['train_number']}: {train['departure_time']} - ¥{train['start_price']}")
finally:
    scraper.close()
```

### 机票查询

```python
from providers.ctrip import CtripScraper, FlightQuery

scraper = CtripScraper()
try:
    query = FlightQuery(
        from_code='SHA',  # 上海
        to_code='BJS',    # 北京
        date='2026-03-01'  # 必须是未来日期
    )
    result = scraper.search_flight(query)
    print(f"找到 {result['total']} 个航班")
    for flight in result['flights'][:5]:
        print(f"{flight['flight_no']}: {flight['airline_name']} - ¥{flight['lowest_adult_price']}")
finally:
    scraper.close()
```

## 支持的机场代码

常用城市代码 (IATA):
- SHA - 上海虹桥
- PVG - 上海浦东
- BJS - 北京
- CAN - 广州
- SZX - 深圳
- CTU - 成都
- HGH - 杭州

## 注意事项

- 仅供学习研究，请遵守携程服务条款
- 频繁请求可能导致 IP 被封
- 必须使用**未来日期**查询
- 页面结构变化会影响选择器有效性

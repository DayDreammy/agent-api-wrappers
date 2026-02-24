# Ctrip Provider (携程)

⚠️ **状态：火车票功能已测试通过 ✅，机票功能待修复 🚧**

## 功能

- ✅ **火车票搜索** - 已测试，可用
- 🚧 **机票搜索** - 代码存在，但 API 响应格式已变更，需要修复

## 测试结果

### 火车票 (已验证 ✅)

```python
from ctrip_client import CtripScraper, TrainQuery

scraper = CtripScraper()
query = TrainQuery(from_station='上海', to_station='杭州', date='2026-02-22')
result = scraper.search_train(query)

# 结果示例
{
    "total": 357,
    "trains": [
        {
            "train_number": "Z4081",
            "departure_station_name": "上海松江",
            "arrival_station_name": "杭州南",
            "departure_time": "01:28",
            "arrival_time": "02:51",
            "start_price": 24.5,
            "seats": [...]
        }
    ]
}
```

### 机票 (待修复 🚧)

当前问题：携程航班 API 返回 `{'status': 0, 'msg': 'success'}`，但代码预期 `data.flightItineraryList`。

可能原因：
- API 响应格式已变更
- 需要额外请求参数
- 反爬机制

## 安装

```bash
pip install playwright
playwright install chromium
```

## 使用示例

### 火车票查询

```python
from ctrip_client import CtripScraper, TrainQuery

scraper = CtripScraper()
try:
    query = TrainQuery(
        from_station='上海',
        to_station='杭州',
        date='2026-03-01'
    )
    result = scraper.search_train(query)
    print(f"找到 {result['total']} 趟列车")
    for train in result['trains'][:5]:
        print(f"{train['train_number']}: {train['departure_time']} - {train['arrival_time']} ¥{train['start_price']}")
finally:
    scraper.close()
```

## 代码来源

此代码来自 `my-skills` 仓库的 `ctrip-ticket-api` skill，经过实际测试验证。

## 待办

- [ ] 修复机票搜索功能
- [ ] 添加更多测试用例
- [ ] 处理验证码/登录场景

## 注意事项

- 仅供学习研究，请遵守携程服务条款
- 频繁请求可能导致 IP 被封
- 页面结构变化会影响选择器有效性

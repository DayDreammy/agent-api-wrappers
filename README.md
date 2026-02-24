# Agent API Wrappers

> 把全世界的网站和 APP 变成 Agent 可用的 API

[English README](./README_EN.md)

---

## 🌟 愿景

**10年后，80%的APP会消失，它们只需要以一个API的形式存在。**

当AI Agent成为主流交互方式，人类不再手动点开一个个APP，而是通过自然语言让Agent完成任务。但问题是——**现在的互联网并不是为Agent设计的**。

- 想订票？没有统一的火车票/机票API
- 想购物？每个电商平台都有自己的封闭接口
- 想查信息？网站反爬、验证码、动态加载层层阻碍
- 想自动化？每个网站都要重新写一套爬虫

本项目旨在**建立一套开放、标准化的网站逆向和浏览器自动化方案**，让开发者可以：
1. 快速将任何网站封装成结构化API
2. 复用社区贡献的现成方案
3. 为AI Agent提供可靠、统一的服务接口

---

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/DayDreammy/agent-api-wrappers.git
cd agent-api-wrappers

# 安装依赖
pip install playwright
playwright install chromium

# 查看示例
python examples/ctrip_flight_search.py
```

---

## 📁 项目结构

```
agent-api-wrappers/
├── providers/              # 各网站/APP的封装方案
│   ├── ctrip/             # 携程 (火车票✅ 机票🚧)
│   ├── template/          # ⭐ 新增provider的模板
├── docs/                   # 文档
│   ├── architecture.md    # 架构设计
│   ├── contribution.md    # 贡献指南
│   └── best-practices.md  # 最佳实践
├── examples/               # 使用示例
├── tests/                  # 测试用例
├── core/                   # 核心框架
│   ├── base.py           # BaseProvider基类
└── README.md
```

---

## 🏗️ 架构设计

### 核心思想

每个网站的封装方案（Provider）遵循统一接口：

```python
from core import BaseProvider

class ExampleProvider(BaseProvider):
    """示例 Provider"""
    
    name = "example"
    version = "1.0.0"
    
    async def search(self, query, **kwargs):
        """搜索功能"""
        # 1. 打开页面
        # 2. 填写表单
        # 3. 获取结果
        # 4. 返回结构化数据
        pass
```

完整架构图见 [docs/architecture.md](./docs/architecture.md)

---

## 🛠️ Provider 状态

| 平台 | 功能 | 状态 | 贡献者 | 测试状态 |
|------|------|------|--------|----------|
| 携程 (Ctrip) | 火车票搜索 | ✅ 可用 | @DayDreammy | ✅ 已测试 |
| 携程 (Ctrip) | 机票搜索 | 🚧 需修复 | @DayDreammy | ❌ API响应变更 |
| 12306 | 火车票查询 | 📋 计划中 | - | - |
| 淘宝 | 商品搜索 | 📋 计划中 | - | - |

**想成为第一个贡献者？** 查看 [providers/template/](./providers/template/)

---

## 🤝 如何贡献

### 贡献一个新的 Provider

1. **Fork 仓库**

2. **复制模板**
   ```bash
   cp -r providers/template providers/your_provider
   ```

3. **实现并测试**
   - 继承 `BaseProvider`
   - 实现必要的方法
   - **⚠️ 必须实际测试通过**
   - 添加测试用例

4. **提交 PR**
   - 描述你解决的问题
   - 提供使用示例
   - 附上测试结果
   - 说明已知限制

### ⚠️ 重要：代码质量要求

**未经测试的代码不要上传**

- 不要猜测 CSS 选择器，必须实际抓取验证
- 不要假设 API 响应格式，必须真实调用确认
- 每个 Provider 提交前必须能在本地跑通

完整规范见 [docs/contribution.md](./docs/contribution.md)

---

## 📖 示例

```python
from providers.ctrip import CtripScraper, TrainQuery

# 火车票查询示例
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
        print(f"{train['train_number']}: {train['departure_time']} - ¥{train['start_price']}")
finally:
    scraper.close()
```

---

## 🎯 路线图

### Phase 1: 基础设施 (进行中)
- [x] 项目初始化
- [x] 核心框架设计
- [x] 携程火车票 Provider (已测试 ✅)
- [ ] 修复携程机票 Provider
- [ ] 12306火车票Provider
- [ ] 验证码处理模块

### Phase 2: 生态建设
- [ ] Provider注册中心
- [ ] REST API服务
- [ ] SDK发布 (Python/Node.js)
- [ ] 文档网站

### Phase 3: 规模化
- [ ] 社区贡献指南完善
- [ ] 自动化测试体系
- [ ] 云服务托管
- [ ] 更多Provider覆盖

---

## ⚠️ 免责声明

本项目仅供学习和研究使用。使用本项目时请遵守：
1. 相关网站的服务条款
2. 当地的法律法规
3. 不进行大规模数据抓取
4. 不用于商业牟利

---

## 💬 加入讨论

- **Issues**: 提出需求或报告问题
- **Discussions**: 技术讨论和想法交流
- **PR**: 贡献你的Provider

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

**让我们一起，为Agent时代构建基础设施！** 🚀

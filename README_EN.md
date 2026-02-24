# Agent API Wrappers

> Transform websites and apps into APIs for AI Agents

[中文 README](./README.md)

---n
## 🌟 Vision

**In 10 years, 80% of mobile apps will disappear. They only need to exist as APIs.**

As AI Agents become the primary interaction layer, humans won't manually tap through apps anymore. Instead, they'll simply tell an Agent what to do in natural language. But here's the problem — **the current internet isn't built for Agents**.

- Want to book a flight? No unified API for train or plane tickets
- Want to shop? Every e-commerce platform has its own closed ecosystem
- Want to fetch information? Websites throw captchas, anti-bot measures, and dynamic loading at you
- Want to automate? Every website requires writing custom scrapers from scratch

This project aims to **build an open, standardized framework for website reverse engineering and browser automation**, enabling developers to:

1. Quickly wrap any website into a structured API
2. Reuse community-contributed solutions
3. Provide reliable, unified service interfaces for AI Agents

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/DayDreammy/agent-api-wrappers.git
cd agent-api-wrappers

# Install dependencies
pip install -r requirements.txt

# Run examples
python examples/ctrip_flight_search.py
```

---

## 📁 Project Structure

```
agent-api-wrappers/
├── providers/              # Wrappers for various websites/apps
│   ├── ctrip/             # Ctrip (携程)
│   ├── 12306/             # Railway 12306
│   ├── taobao/            # Taobao
│   └── template/          # Template for new providers
├── docs/                   # Documentation
│   ├── architecture.md    # Architecture design
│   ├── contribution.md    # Contribution guide
│   └── best-practices.md  # Best practices
├── examples/               # Usage examples
├── tests/                  # Test cases
├── core/                   # Core framework
│   ├── browser.py         # Browser automation
│   ├── captcha.py         # Captcha handling
│   └── proxy.py           # Proxy management
└── README.md
```

---

## 🏗️ Architecture

### Core Philosophy

Each website wrapper (Provider) follows a unified interface:

```python
from core import BaseProvider

class CtripProvider(BaseProvider):
    """Example Ctrip Provider"""
    
    name = "ctrip"
    version = "1.0.0"
    
    async def search_flights(self, origin, dest, date, **kwargs):
        """Search for flights"""
        # 1. Open page
        # 2. Fill form
        # 3. Get results
        # 4. Return structured data
        pass
    
    async def book_flight(self, flight_id, passenger_info):
        """Book a flight"""
        pass
```

### Layered Architecture

```
┌─────────────────────────────────────┐
│           Agent / Applications       │
└─────────────┬───────────────────────┘
│             │ REST API / Python SDK
├─────────────▼───────────────────────┤
│      Provider Registry              │
│      (Unified interface & routing)   │
├─────────────┬───────────────────────┤
│             │ Provider API
├─────────────▼───────────────────────┤
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │
│  │Ctrip│ │12306│ │Taobao│ │Others│ │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘   │
│     └───────┴───────┴───────┘      │
│        Provider Layer               │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │    Browser Automation       │   │
│  │  (Playwright / Selenium)    │   │
│  └─────────────────────────────┘   │
├─────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐           │
│  │ Captcha │ │ Proxy   │           │
│  │ Solver  │ │ Pool    │           │
│  └─────────┘ └─────────┘           │
└─────────────────────────────────────┘
```

---

## 🛠️ Supported Providers

| Platform | Feature | Status | Contributor |
|----------|---------|--------|-------------|
| Ctrip (携程) | Flight search | ✅ Available | @DayDreammy |
| Ctrip (携程) | Hotel search | 🚧 In progress | - |
| 12306 | Train ticket query | 📋 Planned | - |
| Taobao | Product search | 📋 Planned | - |

---

## 🤝 How to Contribute

### Contributing a New Provider

1. **Fork the repository**

2. **Copy the template**
   ```bash
   cp -r providers/template providers/your_provider
   ```

3. **Implement core interfaces**
   - Inherit from `BaseProvider`
   - Implement required methods
   - Add test cases

4. **Submit a PR**
   - Describe the problem you're solving
   - Provide usage examples
   - Document known limitations

### Provider Development Guidelines

```python
# providers/example/provider.py

class ExampleProvider(BaseProvider):
    """
    Example Provider
    
    Functionality: XXX feature for XXX website
    Limitations: Requires login, has captcha, etc.
    """
    
    name = "example"
    version = "1.0.0"
    author = "@your_github"
    
    # Required configuration
    required_config = ["username", "password"]  # If login needed
    
    async def login(self, username, password):
        """Login (if required)"""
        pass
    
    async def search(self, query, **kwargs):
        """
        Search functionality
        
        Returns:
            List[Dict]: Structured results
        """
        pass
```

### Documentation Requirements

Each Provider must include:
- `README.md`: Feature description, usage, caveats
- `requirements.txt`: Dependencies
- `examples/`: Usage examples
- `tests/`: Unit tests

---

## 📖 Example: Ctrip Flight Search

```python
import asyncio
from providers.ctrip import CtripProvider

async def main():
    # Initialize Provider
    ctrip = CtripProvider()
    
    # Search flights
    flights = await ctrip.search_flights(
        origin="SHA",        # Shanghai
        destination="PEK",   # Beijing
        date="2026-03-01"
    )
    
    # Print results
    for flight in flights:
        print(f"{flight['airline']} {flight['flight_no']}")
        print(f"  Departure: {flight['dep_time']}")
        print(f"  Arrival: {flight['arr_time']}")
        print(f"  Price: ¥{flight['price']}")
        print()

asyncio.run(main())
```

---

## 🎯 Roadmap

### Phase 1: Infrastructure (In Progress)
- [x] Project initialization
- [x] Core framework design
- [x] Ctrip flight Provider
- [ ] 12306 train ticket Provider
- [ ] Captcha handling module

### Phase 2: Ecosystem Building
- [ ] Provider registry
- [ ] REST API service
- [ ] SDK release (Python/Node.js)
- [ ] Documentation website

### Phase 3: Scale
- [ ] Community contribution guidelines
- [ ] Automated testing framework
- [ ] Cloud hosting service
- [ ] More provider coverage

---

## ⚠️ Disclaimer

This project is for educational and research purposes only. When using this project, please comply with:
1. Terms of service of relevant websites
2. Local laws and regulations
3. No large-scale data scraping
4. No commercial exploitation

---

## 💬 Join the Discussion

- **Issues**: Submit feature requests or bug reports
- **Discussions**: Technical discussions and idea exchanges
- **PRs**: Contribute your Provider

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) for details

---

**Let's build the infrastructure for the Agent era together!** 🚀

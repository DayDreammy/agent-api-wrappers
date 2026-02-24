# Ctrip Provider (携程) - 待实现

⚠️ **状态：尚未实现 (Work in Progress)**

我们正在寻找贡献者来实现携程的浏览器自动化封装。

## 计划功能

- [ ] 机票搜索
- [ ] 酒店搜索

## 为什么还没实现？

**原则：未经测试的代码不上传**

之前本仓库包含了一份未经验证的携程代码（猜测了 CSS 选择器但未实际运行测试）。根据社区规范，我们已将其移除。

## 如何贡献

如果你愿意实现这个 Provider：

1. **Fork 仓库**

2. **本地开发**
   ```bash
   cd providers/ctrip
   # 参考 providers/template/ 目录
   ```

3. **必须实际测试**
   - 用浏览器访问携程网站
   - 使用 Playwright/Selenium 实际抓取页面
   - 验证选择器能正确提取数据
   - 确保代码能真正运行

4. **提交 PR**
   - 附上测试结果截图
   - 说明测试环境（Python 版本、浏览器版本）

## 参考资源

- 携程机票搜索页: https://flights.ctrip.com
- 模板代码: `providers/template/`

## 注意事项

- 携程可能有反爬机制
- 页面结构可能变化，需要定期维护
- 仅供学习研究，请遵守携程服务条款

---

**Want to help?** Open an issue or submit a PR!

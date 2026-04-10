# GitHub Actions 配置修复说明

## 🔧 修复内容

### 原始配置存在的问题

1. **Cron表达式格式错误**
   ```yaml
   # ❌ 错误：不支持逗号分隔
   - cron: '30 0,1,14 * * *'
   ```
   GitHub Actions的schedule不支持在单个cron表达式中使用逗号分隔多个时间点。

2. **时间计算错误**
   ```yaml
   # ❌ 错误的计算
   # 7:30 UTC = 15:30 北京时间
   ```
   实际上：北京时间 = UTC + 8小时

3. **Python模块导入问题**
   GitHub Actions环境可能找不到`src.graphs.graph`模块，缺少PYTHONPATH设置。

4. **条件判断不可靠**
   ```yaml
   if: github.event.schedule == '30 0 * * *'
   ```
   `github.event.schedule`的返回值格式不稳定，可能导致条件判断失败。

---

## ✅ 修复方案

### 方案：拆分为3个独立工作流

创建了3个独立的工作流文件，每个对应一个时间点：

#### 1. 天气预报（07:30）
- 文件：`.github/workflows/weather.yml`
- 时间：UTC 23:30 = 北京时间 07:30（次日）
- 触发：每天自动运行

#### 2. 早安问候（07:31）
- 文件：`.github/workflows/morning.yml`
- 时间：UTC 23:31 = 北京时间 07:31（次日）
- 触发：每天自动运行

#### 3. 晚安问候（22:30）
- 文件：`.github/workflows/evening.yml`
- 时间：UTC 14:30 = 北京时间 22:30
- 触发：每天自动运行

---

## 📝 配置详情

### 天气预报工作流

```yaml
name: 天气预报（北京时间 07:30）

on:
  schedule:
    - cron: '30 23 * * *'  # UTC 23:30 = 北京时间 07:30
  workflow_dispatch:

jobs:
  send-weather:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    - run: pip install -r requirements.txt
    - run: |
        export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src
        python -c "from src.graphs.graph import main_graph; main_graph.invoke({'city': '苏州', 'trigger_type': 'weather'})"
```

---

## ⏰ 时间对照表

| 工作流 | 目标时间（北京时间） | UTC时间 | Cron表达式 |
|--------|---------------------|---------|-----------|
| 天气预报 | 07:30 | 23:30（前一天） | `30 23 * * *` |
| 早安问候 | 07:31 | 23:31（前一天） | `31 23 * * *` |
| 晚安问候 | 22:30 | 14:30 | `30 14 * * *` |

---

## 🎯 优势

### 拆分为独立工作流的好处：

1. **更可靠**：每个工作流独立运行，互不干扰
2. **更清晰**：每个工作流职责单一，易于理解和维护
3. **更易调试**：每个工作流独立日志，问题定位更准确
4. **更灵活**：可以单独控制每个工作流的触发时间

---

## 🔍 验证部署

### 步骤1：刷新GitHub仓库
访问：https://github.com/jinhuansanjie/daily-greeting

### 步骤2：查看工作流
1. 点击 **Actions** 标签
2. 应该能看到3个工作流：
   - 天气预报（北京时间 07:30）
   - 早安问候（北京时间 07:31）
   - 晚安问候（北京时间 22:30）

### 步骤3：手动测试
对每个工作流单独测试：
1. 点击某个工作流（如"天气预报"）
2. 点击 **Run workflow**
3. 选择分支（main）
4. 点击 **Run workflow** 按钮

### 步骤4：查看运行日志
1. 点击工作流运行记录
2. 查看每个步骤的执行状态
3. 查看详细日志输出

---

## 🐛 常见问题排查

### 问题1：工作流没有自动运行

**可能原因：**
- 时间未到
- Cron表达式错误
- GitHub Actions未启用

**解决方法：**
1. 检查Cron表达式是否正确
2. 确认GitHub Actions已启用
3. 手动触发测试

### 问题2：Python模块导入失败

**错误信息：**
```
ModuleNotFoundError: No module named 'src.graphs.graph'
```

**解决方法：**
已在配置中添加：
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src
```

### 问题3：依赖安装失败

**错误信息：**
```
ERROR: Could not find a version that satisfies the requirement...
```

**解决方法：**
检查`requirements.txt`中的依赖版本是否正确

### 问题4：运行超时

**错误信息：**
```
Error: Process completed with exit code 137
```

**解决方法：**
- 检查网络连接
- 检查API密钥是否正确
- 检查代码是否有死循环

---

## 📊 监控运行状态

### 查看运行历史
1. 访问GitHub仓库
2. 点击 **Actions** 标签
3. 可以看到所有工作流的运行记录

### 设置通知
1. 点击仓库 **Settings**
2. 选择 **Notifications**
3. 配置工作流运行通知

---

## 🔄 更新配置

### 修改时间
编辑对应的工作流文件，修改cron表达式：
```yaml
schedule:
  - cron: '新的时间表达式'
```

### 修改城市
编辑对应的工作流文件，修改Python代码中的城市参数：
```python
main_graph.invoke({'city': '新的城市', 'trigger_type': '...'})
```

---

## 📞 获取帮助

如果遇到问题：
1. 查看Actions日志
2. 检查工作流配置
3. 查看GitHub文档：https://docs.github.com/actions

---

## ✅ 部署检查清单

- [x] 修复Cron表达式格式错误
- [x] 修正时间计算
- [x] 添加PYTHONPATH设置
- [x] 拆分为独立工作流
- [x] 推送到GitHub
- [ ] 手动测试每个工作流
- [ ] 确认自动运行正常
- [ ] 配置运行通知

---

**修复完成！工作流现在应该可以正常运行了。** 🎉

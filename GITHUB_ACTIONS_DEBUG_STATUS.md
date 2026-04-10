# GitHub Actions 调试状态

## 已完成的修复

### 1. Python导入路径问题 ✓
- **问题**: 所有Python文件缺少`src`前缀
- **修复**: 已在所有节点文件中添加`from src.xxx import xxx`
- **涉及文件**:
  - src/graphs/graph.py
  - src/graphs/nodes/trigger_node.py
  - src/graphs/nodes/weather_query_node.py
  - src/graphs/nodes/greeting_generate_node.py
  - src/graphs/nodes/tts_node.py
  - src/graphs/nodes/send_message_node.py

### 2. test.yml语法错误 ✓
- **问题**: 第64行有Python语法错误
  ```python
  # 错误的代码
  print('当前目录:', import os; os.getcwd())
  ```
- **修复**: 改为正确的导入方式
  ```python
  import os
  print('当前目录:', os.getcwd())
  ```
- **提交**: `fix: 修复test.yml中的Python语法错误`

### 3. 工作流拆分 ✓
- 创建了3个独立的工作流文件
  - `.github/workflows/weather.yml` - 天气预报（7:30）
  - `.github/workflows/morning.yml` - 早安问候（7:31）
  - `.github/workflows/evening.yml` - 晚安问候（22:30）
- 优势：每个时间点独立触发，互不影响

## 下一步操作

### 立即执行
1. **运行test.yml测试工作流**
   - 进入GitHub仓库Actions页面
   - 点击`test.yml`工作流
   - 点击"Run workflow"按钮
   - 选择`main`分支，点击"Run workflow"绿色按钮
   - **查看每个测试步骤的输出**

2. **根据test.yml结果调试**
   - 如果"测试8：尝试导入main_graph"失败，查看错误信息
   - 可能的问题：
     - 依赖包版本冲突
     - 环境变量未设置
     - 权限问题

### 3个实际工作流的部署顺序
建议按以下顺序验证：

1. **先验证evening.yml（晚安问候）**
   - 修改cron为立即触发（用于测试）
   - 等待运行完成，查看日志
   - 确认企业微信是否收到消息

2. **再验证weather.yml（天气预报）**
   - 按相同步骤测试
   - 确认天气查询、问候语生成、TTS、推送全部正常

3. **最后验证morning.yml（早安问候）**
   - 完成测试后，修改回正确的cron时间
   - 确保所有工作流都正常

## 当前工作流配置

### test.yml（调试用）
- **触发方式**: 手动触发（workflow_dispatch）
- **测试内容**:
  - Python环境
  - 依赖包安装（langgraph, langchain-core, pydantic, coze-coding-dev-sdk）
  - 文件结构检查
  - main_graph导入测试

### weather.yml
```yaml
on:
  schedule:
    - cron: '30 7 * * *'  # 北京时间7:30
```

### morning.yml
```yaml
on:
  schedule:
    - cron: '31 7 * * *'  # 北京时间7:31
```

### evening.yml
```yaml
on:
  schedule:
    - cron: '30 22 * * *'  # 北京时间22:30
```

## 可能遇到的问题

### 问题1：导入main_graph失败
**症状**: ModuleNotFoundError或ImportError
**排查**:
1. 检查PYTHONPATH设置是否正确
2. 检查src目录是否存在
3. 检查文件导入路径是否都带`src`前缀
4. 查看完整的错误堆栈

### 问题2：依赖包版本冲突
**症状**: ImportError或版本警告
**解决方案**:
- 查看完整的错误日志
- 在requirements-github.txt中固定版本号
- 例如：`langgraph==0.2.45`

### 问题3：环境变量未设置
**症状**: KeyError或None值错误
**解决方案**:
- 在GitHub仓库Settings中添加Secrets：
  - `COZE_WORKSPACE_PATH`（如果需要）
  - `WECHAT_WEBHOOK_KEY`（企业微信webhook key）

### 问题4：TTS语音合成失败
**症状**: 语音链接为空或TTS调用失败
**解决方案**:
- 检查coze-coding-dev-sdk版本
- 确认语音模型ID正确（zh_female_vv_uranus_bigtts）
- 查看API调用日志

### 问题5：企业微信推送失败
**症状**: 消息未发送到群聊
**解决方案**:
- 确认webhook key正确
- 检查消息格式是否符合企业微信要求
- 查看HTTP响应状态码

## 测试验证清单

- [ ] test.yml所有测试步骤通过
- [ ] main_graph成功导入
- [ ] weather.yml成功运行
- [ ] morning.yml成功运行
- [ ] evening.yml成功运行
- [ ] 企业微信群收到天气预报消息
- [ ] 企业微信群收到早安问候消息
- [ ] 企业微信群收到晚安问候消息
- [ ] 语音链接可以正常播放
- [ ] 问候语开头为"亲爱的"
- [ ] 默认城市为苏州

## 重要提醒

1. **每次修改代码后必须先运行test.yml**
   - 确保基础功能正常后再测试实际工作流

2. **查看详细日志的方法**
   - 点击失败的工作流运行记录
   - 展开失败的Step
   - 查看完整的输出内容

3. **调试技巧**
   - 从最简单的测试开始（Python环境）
   - 逐个步骤验证（安装依赖 -> 检查文件 -> 导入模块）
   - 保存完整的错误日志

4. **Secrets配置**
   - 如果工作流需要敏感信息，请添加到GitHub Secrets
   - 在工作流中使用`${{ secrets.SECRET_NAME }}`引用

## 联系支持

如果遇到无法解决的问题，请提供以下信息：
1. 失败的工作流名称
2. 完整的错误日志
3. 工作流运行编号
4. 相关代码文件的当前版本

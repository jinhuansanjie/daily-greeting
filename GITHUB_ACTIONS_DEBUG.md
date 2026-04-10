# GitHub Actions 调试指南

## 🔍 查看详细日志

### 第一步：访问GitHub仓库
1. 访问：https://github.com/jinhuansanjie/daily-greeting
2. 点击 **Actions** 标签

### 第二步：查看工作流运行记录
1. 在左侧选择一个工作流（如"早安问候（北京时间 07:31）"）
2. 点击某个运行记录

### 第三步：展开每个步骤查看详细日志

#### 查看各个步骤的日志：

**1. Checkout代码**
```
📝 查看点：
- 是否成功检出代码
- 文件是否存在
```

**2. 设置Python环境**
```
📝 查看点：
- Python版本是否为3.12
- 环境是否设置成功
```

**3. 打印环境信息**
```
📝 查看点：
- 当前目录是否正确
- PYTHONPATH是否包含必要的路径
- 文件结构是否正常
```

**4. 安装依赖**
```
📝 查看点：
- 是否所有依赖都成功安装
- 是否有依赖冲突
- 是否有网络错误
```

**5. 测试导入**
```
📝 查看点：
- 是否显示"导入成功"
- 如果失败，查看具体错误信息
```

**6. 发送问候**
```
📝 查看点：
- 是否显示"开始发送..."
- 是否有异常堆栈
- 发送状态是什么
```

---

## 🐛 常见错误及解决方案

### 错误1：ModuleNotFoundError

**错误信息：**
```
ModuleNotFoundError: No module named 'src.graphs.graph'
```

**原因：**
PYTHONPATH设置不正确

**解决方案：**
已在工作流中添加：
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src
```

---

### 错误2：依赖安装失败

**错误信息：**
```
ERROR: Could not find a version that satisfies the requirement xxx
```

**原因：**
- 依赖版本不存在
- 网络问题
- 依赖冲突

**解决方案：**
```bash
# 升级pip
pip install --upgrade pip

# 检查requirements.txt
pip install --dry-run -r requirements.txt
```

---

### 错误3：cozeloop警告

**错误信息：**
```
WARNING [cozeloop] Noop client not supported. Invalid parameter. workspace_id is required.
```

**说明：**
这是警告信息，不是错误，可以忽略

**原因：**
cozeloop SDK在当前环境中使用了noop模式

---

### 错误4：发送失败

**错误信息：**
```
✗ 发送失败
发送状态: failed
```

**原因：**
- 企业微信Webhook Key错误
- 网络问题
- API限制

**解决方案：**
1. 检查企业微信Webhook Key配置
2. 查看详细的错误日志
3. 检查网络连接

---

### 错误5：超时

**错误信息：**
```
Error: Process completed with exit code 137
```

**原因：**
- 执行时间过长
- 内存不足
- 网络超时

**解决方案：**
1. 检查是否有死循环
2. 优化代码性能
3. 检查网络连接

---

## 📊 日志分析

### 成功的日志示例：
```
Python版本:
Python 3.12.x

当前目录:
/home/runner/work/daily-greeting/daily-greeting

目录结构:
drwxr-xr-x
-rw-r--r--  README.md
-rw-r--r--  requirements.txt
drwxr-xr-x  src/

PYTHONPATH:
/home/runner/work/daily-greeting/daily-greeting:/home/runner/work/daily-greeting/daily-greeting/src

开始安装依赖...
Successfully installed xxx

导入成功

开始发送天气预报...
✓ 天气预报发送成功
```

---

### 失败的日志示例：
```
开始发送早安问候...
Traceback (most recent call last):
  File "<string>", line 10, in <module>
    result = main_graph.invoke({'city': '苏州', 'trigger_type': 'morning'})
  ...
RuntimeError: API Error: xxx
✗ 执行出错: xxx
```

---

## 🔧 调试技巧

### 1. 添加更多日志
在工作流中添加更多print语句：
```python
print("调试信息:", xxx)
```

### 2. 本地模拟GitHub Actions环境
```bash
cd /workspace/projects
bash scripts/test_github_actions.sh
```

### 3. 使用GitHub Actions的调试功能
1. 在仓库设置中启用"Actions Debug Logging"
2. 在工作流中添加：
```yaml
- name: 启用调试
  run: |
    echo "::debug::调试信息"
```

### 4. 分步骤测试
注释掉后面的步骤，逐步测试：
```yaml
# - name: 发送问候
#   run: ...
```

---

## 📞 获取帮助

### 如果问题仍然存在：

1. **截图完整的错误日志**
   - 包括所有步骤的输出
   - 包括堆栈跟踪

2. **提供工作流配置**
   - 复制完整的yml文件内容

3. **提供本地测试结果**
   ```bash
   bash scripts/test_github_actions.sh
   ```

4. **检查GitHub Actions状态**
   - 访问：https://www.githubstatus.com/
   - 确认GitHub Actions服务正常

---

## ✅ 成功标准

工作流成功执行应该看到：
- ✅ 所有步骤都显示绿色
- ✅ 最后的步骤显示"✓ xx发送成功"
- ✅ 没有红色的错误信息
- ✅ 企业微信群收到消息

---

## 📋 调试检查清单

- [ ] 查看完整的工作流日志
- [ ] 检查每个步骤的输出
- [ ] 确认Python版本正确
- [ ] 确认PYTHONPATH设置正确
- [ ] 确认依赖安装成功
- [ ] 确认导入测试通过
- [ ] 确认没有异常堆栈
- [ ] 确认发送状态为success
- [ ] 确认企业微信收到消息

---

## 🎯 下一步

1. 刷新GitHub Actions页面
2. 手动触发工作流
3. 查看详细日志
4. 根据日志定位问题
5. 修复后重新测试

---

**现在请重新手动触发工作流，查看详细的日志输出，然后告诉我具体的错误信息！** 🚀

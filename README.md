# 知造科学 V3

两款互动科学产品：宇宙实验室、科学侦探社。新增动态引力展示、成就、本机排行榜和可选真实 AI 自由问答。

## 快速运行
直接打开 index.html：静态实验、动画、排行榜可运行，AI 提示未连接。

## 开启 AI
安装 Python 3.10+；配置环境变量 OPENAI_API_KEY，并运行 `python server.py`，浏览器打开 `http://localhost:8000`。可通过 OPENAI_MODEL 与 OPENAI_BASE_URL 指定兼容 Chat Completions 的模型服务。密钥仅放服务端。

## 部署包
- `science_v3_flat.zip`：ZIP 根目录直接包含 frontend.deploy.json / backend.deploy.json。
- `science_v3_tmp.zip`：兼容性试验，JSON 位于 ZIP 内 `_tmp/` 目录。只有当平台明确要求 `_tmp` 包装时才使用。

注意：部署平台对两个 JSON 的内容规范未知，文件存在并不等于部署规范已通过。静态托管不能运行 server.py，若要使用真正 AI，需要可运行 Python 的后端服务。排行榜仅保存在浏览器，非跨用户在线排名。

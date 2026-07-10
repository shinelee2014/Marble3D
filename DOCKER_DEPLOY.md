# 🐳 Marble 课程图谱威联通 QNAP NAS (Docker) 部署指南

当前系统已经从最初的浏览器“轻量网页版”升级为**完备的 API 后端驱动版**。

我们编写了原生的 Python 后端（`server.py`），使用 Python 标准库实现，支持**数据持久化落盘**。所有的进度和孩子档案都会实时保存到您本地/NAS 上的 `data/` 目录中，在所有设备（手机、iPad、PC）上都会自动实时同步。

---

## 📦 威联通 QNAP NAS 部署步骤 (Container Station)

### 📌 准备工作
将您电脑上的 `d:\antigravity\app\Taxonomy\` 文件夹下的所有文件打包上传到您威联通 NAS 的共享文件夹中（例如上传到 `/share/Container/marble-taxonomy/` 文件夹下）。

### 🛠️ 方法一：使用 `docker-compose` 部署（极力推荐）
威联通的 **Container Station（容器工作站）** 完美支持 YAML 编排。

1. 打开 **Container Station** -> 点击左侧的 **「应用程序 (Application)」** -> 点击右上角 **「创建 (Create)」**。
2. 输入应用名称（如 `marble-taxonomy`）。
3. 在 YAML 代码框中复制并粘贴项目根目录下的 [**`docker-compose.yml`**](file:///d:/antigravity/app/Taxonomy/docker-compose.yml) 的内容：
   ```yaml
   version: '3.8'

   services:
     marble-taxonomy:
       build: .
       container_name: marble-taxonomy
       ports:
         - "8000:8000"
       volumes:
         - ./data:/app/data
       restart: unless-stopped
   ```
4. 点击 **「验证 YAML」** -> 点击 **「创建」** 即可。它会自动在本机编译运行，并将 `data/` 文件夹挂载出来以防丢失数据。

---

### 🛠️ 方法二：直接通过 Docker 命令行编译部署
如果您熟悉 NAS 的 SSH 终端，可以直接登录 NAS，进入上传的目录并运行：

```bash
# 1. 编译 Docker 镜像
docker build -t marble-taxonomy:latest .

# 2. 启动容器（并将本地的 data/ 文件夹映射到容器内以实现数据持久化）
docker run -d \
  --name marble-taxonomy \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --restart unless-stopped \
  marble-taxonomy:latest
```

---

## 💻 电脑本地直接启动方式

如果您在本地电脑上测试：
1. **不需要运行任何 pip 安装**（不需要 Flask/FastAPI 依赖），直接在项目根目录下双击运行 `server.py` 或在终端运行：
   ```powershell
   python server.py
   ```
2. 在浏览器中访问：👉 [**http://localhost:8000/explorer.html**](http://localhost:8000/explorer.html)
3. 所有的账户与通关信息都会自动写入到本地的 [**`data/profiles_db.json`**](file:///d:/antigravity/app/Taxonomy/data/profiles_db.json) 和 [**`data/mastery_db.json`**](file:///d:/antigravity/app/Taxonomy/data/mastery_db.json) 中，不再依赖浏览器缓存。

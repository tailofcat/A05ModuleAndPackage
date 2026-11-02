# 《模块与包》演示 · A05ModuleAndPackage

用一段能听出效果的音频播放，演示 Python 的**模块导入**与**第三方包安装**两件事。

代码只有 20 行，但把「装包 → import → 调 API」的完整链路走了一遍，效果可听可见，适合课堂演示。

## 环境要求

| 项 | 要求 | 说明 |
|---|---|---|
| 操作系统 | **Windows** | 本项目虚拟环境是 Windows 版（`.venv/Scripts/python.exe`），WSL/Linux 的 bash 里激活不了 |
| 终端 | **CMD 或 PowerShell** | 不要在 WSL 里跑，路径分隔符和解释器都不是一个东西 |
| Python | 3.13+ | 见 `.python-version` |
| 包管理 | [uv](https://docs.astral.sh/uv/) | 用它装依赖、跑脚本 |

> ⚠️ **最容易踩的坑**：在 WSL 终端里 `cd` 到这个目录再执行 `.venv\Scripts\activate` 会报错。
> 请打开 Windows 的 CMD / PowerShell / Windows Terminal，进到项目目录后再操作。
> 从 WSL 想跳到 Windows 终端，直接在 Windows 开始菜单搜 "CMD" 更省事。

## 快速开始

### 方式一：直接跑主程序（推荐）

```cmd
git clone git@github.com:tailofcat/A05ModuleAndPackage.git
cd A05ModuleAndPackage
uv sync
uv run python main.py
```

运行后音乐开始播放，终端会循环提示，输入 `S` 或 `Stop` 回车即停止。

> 已有本地副本的话，前两行 `git clone` / `cd` 可以跳过，直接进到项目目录执行后两行。
>
> 📁 下文所有命令都假定**当前工作目录是项目根目录**（能看到 `main.py` 和 `music/` 的那一层）。
> `main.py` 里的音频路径写的是 `./music/...`，在别的目录执行会找不到文件。

### 方式二：在交互式解释器里手动 import

演示「一个包被导入后能做什么」，更能看清模块和包的区别：

```cmd
uv run python
```

进入 `>>>` 后：

```python
import playsound3
playsound3.playsound('./music/一班名字之歌-四十九颗星.mp3')
```

已激活虚拟环境时也可以这样（等价写法）：

```cmd
.venv\Scripts\activate
python
```

## 目录结构

```
A05ModuleAndPackage/
├── main.py                 # 演示入口：导入 playsound3 并播放/停止
├── pyproject.toml          # 项目元信息与依赖声明
├── uv.lock                 # 依赖锁定文件（应提交，保证他人环境一致）
├── requirements.txt        # pip 格式依赖清单，仅主依赖（不含可选组）
├── music/                  # 音频素材
│   ├── 一班名字之歌-四十九颗星.mp3
│   └── 二三班名字之歌-九十七颗星.mp3
├── .python-version         # 声明 Python 3.13
├── .gitignore
├── .gitattributes
└── LICENSE
```

## 依赖说明

### 依赖安装的两种方式

**方式 A：uv（推荐）**

```cmd
uv sync
```

`uv sync` 按 `uv.lock` 装出与作者完全一致的环境，包含 Windows 专用依赖的条件处理。
默认**只装运行演示所需的主依赖**；`yt-dlp` 放在可选的 `tools` 组里，不会自动安装。
需要下载音频素材时再单独加装：

```cmd
uv sync --group tools
```

**方式 B：pip（没装 uv 时）**

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> `requirements.txt` 由 uv 自动导出，版本与 `uv.lock` 严格一致，**不要手改**。
> 修改依赖后重新生成：
> ```cmd
> uv export --format requirements-txt --no-hashes --no-emit-project --output-file requirements.txt
> ```

### 依赖清单

| 包 | 用途 | 是否必需 |
|---|---|---|
| [`playsound3`](https://pypi.org/project/playsound3/) | 跨平台播放音频文件，支持 `block=False` 异步播放和 `.stop()` | ✅ 主依赖，`main.py` 直接调用 |
| `pywin32` | Windows 下音频播放的底层支持（MCI），由 `playsound3` 自动拉入 | ✅ 主依赖，仅 `sys_platform == 'win32'` 时安装 |
| [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) | 从视频/音频页面下载素材，用来准备 `music/` 里的文件 | ⚙️ 可选组 `tools`，命令行工具，代码不引用 |

`yt-dlp` 属于**可选**依赖，只用于准备素材，不影响演示运行。它几乎没有传递依赖，版本同样被 `uv.lock` 锁定，只是默认不安装。

装工具并下载素材：

```cmd
uv sync --group tools
uv run yt-dlp -P music "<视频或音频页面地址>"
```

> `-P music` 指定输出目录为 `music/`（`--paths` 的缩写），文件名自动按视频标题生成。
>
> ⚠️ 若源站点提供的是分离的音视频流，`yt-dlp` 需要系统里装有 **ffmpeg** 才能合并或转成 mp3/m4a。
> 只下载单文件格式（如已上传的 mp3）则不需要 ffmpeg。检查：`ffmpeg -version`。
>
> 不同站点的可用性会随站点改版变化。报错时先升级到最新版再试（注意：不要用 `yt-dlp -U`，
> 经 uv / pip 安装的副本不能自更新）：
>
> ```cmd
> uv lock --upgrade-package yt-dlp
> uv sync --group tools
> ```

不再需要时，从 `pyproject.toml` 的 `[dependency-groups]` 里删掉整个 `tools` 组，再 `uv lock` 一次即可。

## 音频文件对照

仓库里的实际文件名如下，照抄上面命令即可：

| 实际文件 | 班级 |
|---|---|
| `music/一班名字之歌-四十九颗星.mp3` | 一班，49 人 |
| `music/二三班名字之歌-九十七颗星.mp3` | 二三班，97 人 |

> 音频为班级活动素材，仅作教学演示使用，版权归原作者所有。若需商用请自行取得授权。

## 常见问题

**`ModuleNotFoundError: No module named 'playsound3'`**
依赖没装。执行 `uv sync`，或确认当前解释器是不是 `.venv` 里的那个。

**`playsound3.playsound(...)` 没声音也没报错**
检查音频路径是否相对当前工作目录。脚本里的路径是 `./music/...`，所以必须在项目根目录执行。

**`activate` 找不到命令 / 提示 Permission denied**
你在 WSL 的 bash 里。换 Windows CMD 或 PowerShell。

**`git push` 被拒 / 要求输入密码**
先看远端地址用什么协议（`git remote -v`）：

| 地址形式 | 认证方式 | 常见报错 |
|---|---|---|
| `git@github.com:...` | SSH 公钥 | `Permission denied (publickey)` → 公钥没加到平台 |
| `https://github.com/...` | Personal Access Token | `password authentication was removed` → 密码位要填 Token |

本项目作者用的是 SSH。克隆后想改协议：`git remote set-url origin <新地址>`。

**`uv sync` 报错，或 `uv.lock` 与 `pyproject.toml` 不一致**
先确认 uv 版本足够新（`uv --version`），再执行 `uv lock` 重新解析，最后 `uv sync`。
不想动 lock 就换方式 B，用 `pip install -r requirements.txt` 绕过。

## 许可

[MIT](LICENSE)

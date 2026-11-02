# 《模块与包》演示

一个能用耳朵验证的小项目。它只做三件事，但正好是「模块与包」这一课的全部：

1. **装**一个别人写好的包
2. **导**入它
3. **用**它

代码只有 20 行，效果是一首歌。

---

## 一、先准备两样东西

| 要装的 | 版本 | 干什么用 |
|---|---|---|
| Python | 3.13 或更高 | 运行代码 |
| [uv](https://docs.astral.sh/uv/) | 最新版 | 安装第三方包、运行程序 |

**终端用 Windows 的 CMD 或 PowerShell。** 不要用 WSL / Linux 终端——本项目的虚拟环境是 Windows 版，在 Linux 里用不了。

---

## 二、三步跑起来

### 第 1 步：把项目拿到本地

> 访问网址：https://gitcode.com/lijingcong/A05ModuleAndPackage
> 点击页面中的“下载zip”

或者通过git命令
```cmd
git clone git@github.com:tailofcat/A05ModuleAndPackage.git
```

> 没装 git、或者不想用命令行的，可以在 GitHub 页面点绿色的 **Code → Download ZIP**，解压后用同样效果。



### 第 2 步：进入项目目录
手动打开目录，或者使用命令行
```cmd
cd A05ModuleAndPackage
```

进去之后应该能看到 `main.py` 和 `music` 文件夹。

### 第 3 步：装依赖并运行
以Windows为例，在目录中空白处右键打开"终端或powershell"，输入以下命令（如果前期没有装uv，请查看教程中的uv安装 https://www.runoob.com/python-qt/python-qt-venv-uv.html）
```cmd
uv sync
uv run python main.py
```

**听到音乐就成功了。** 终端会提示输入命令，输入 `S` 回车即可停止。

> `uv sync` 做的事：读取 `pyproject.toml` 里写的依赖清单，把需要的包下载到一个叫 `.venv` 的文件夹里。
> `uv run` 做的事：在这个环境里运行程序。所以**不需要手动激活虚拟环境**。

---

## 三、回头看看发生了什么

```
pyproject.toml  ──"我需要 playsound3"──▶  uv sync  ──▶  .venv/ 里多了个包
                                                              │
main.py  ──"import playsound3"───────────────────────────────┘
```

项目里就这几个文件：

| 文件 | 干什么 |
|---|---|
| `main.py` | 主程序，20 行 |
| `pyproject.toml` | 声明「这个项目需要哪些包」 |
| `uv.lock` | 锁定每个包的确切版本，保证别人装出来跟你一样 |
| `requirements.txt` | 给不用 uv 的人用的依赖清单 |
| `music/` | 音频素材 |
| `.venv/` | uv 下载下来的包，**不会上传到 GitHub** |

---

## 四、再做一遍：亲手 import 一次

上面是「程序自动跑」。现在改成手动输入，能更清楚地看到 `import` 到底做了什么。

```cmd
uv run python
```

出现 `>>>` 提示符后，一行一行输入：

```python
import playsound3
```

回车后什么都没发生——这是正常的。`import` 只是把一个包**拿进来**，还没用它。

```python
playsound3.playsound('./music/一班名字之歌-四十九颗星.mp3')
```

回车，音乐开始播放。

这里能看出三层的名字关系：

| 写法 | 是什么 |
|---|---|
| `playsound3` | **包**（一个装了很多东西的文件夹） |
| `playsound3.playsound` | 包里的**函数**（用点号取出来） |
| `'./music/....mp3'` | 传给函数的**参数** |

---

## 五、uv 和 pip 是什么关系

两个都是 Python 的装包工具，**干的活一样**，uv 是后来的新工具，更快。

同一个项目，两种装法都能用：

**用 uv（推荐，本项目的写法）**

```cmd
uv sync
uv run python main.py
```

**用 pip（老办法，装机自带）**

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

区别就一句话：**用 uv 不用手动激活虚拟环境，用 pip 要先 `activate`。**
（注意最后运行程序时，pip 那边是 `python main.py`，uv 那边是 `uv run python main.py`。）

---

## 六、卡住了看这里

**提示找不到 `uv` 命令**
uv 没装好。去 [docs.astral.sh/uv](https://docs.astral.sh/uv/) 按说明装，然后**重开一个终端**（装完不重开，旧窗口里找不到）。

**`ModuleNotFoundError: No module named 'playsound3'`**
依赖没装。在当前目录执行 `uv sync`。如果已经装过，检查是不是用了 Windows 的 Python，而不是 WSL 里的。

**没声音，也不报错**
多半是不在项目根目录。`main.py` 里写的是 `./music/...` 这种相对路径，必须在能看到 `music` 文件夹的地方运行。

**`activate` 提示找不到命令**
你在 WSL / Linux 终端里。换成 Windows 的 CMD 或 PowerShell。

---

## 附

`music/` 里已经有音频，正常用不到这一节。
如果想自己下载素材，项目额外准备了一个可选的下载工具：

```cmd
uv sync --group tools
uv run yt-dlp -P music "<视频或音频页面地址>"
```

音频为班级活动素材，仅作教学演示，版权归原作者所有。

本项目采用 [MIT 许可证](LICENSE)。

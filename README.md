# 量子学技术

> 一套讲量子技术的书　·　作者 Dr. Dezeming

量子技术不只是量子计算。它还包括量子通信、量子精密测量、量子器件与量子纠错。这套书按这个范围展开，一册入门铺全貌，其余各册钻进具体方向。

## 分册

| 册 | 书名 | 副标题 | 篇幅 | 在线阅读 | 下载 |
|---|---|---|---|---|---|
| 第一册 | 量子技术入门 | 从黑体辐射到量子芯片 | 71 页 | [阅读](books/intro/README.md) | [PDF](output/v1-intro.pdf) |
| 第二册 | 量子力学与实验基础 | 从双缝到单光子 | 106 页 | [阅读](books/foundations/README.md) | [PDF](output/v2-foundations.pdf) |
| 第三册 | 量子计算与算法 | 从量子比特到因式分解 | 102 页 | [阅读](books/computing/README.md) | [PDF](output/v3-computing.pdf) |
| 第四册 | 量子器件与硬件平台 | 超导、离子、原子与光子 | 96 页 | [阅读](books/devices/README.md) | [PDF](output/v4-devices.pdf) |
| 第五册 | 量子纠错与容错 | 从重复码到表面码 | 81 页 | [阅读](books/qec/README.md) | [PDF](output/v5-qec.pdf) |
| 第六册 | 量子通信与量子网络 | 从 BB84 到量子互联网 | 77 页 | [阅读](books/network/README.md) | [PDF](output/v6-network.pdf) |

## 在线阅读

站点部署在 GitHub Pages 上，打开 [https://ai-crystal.github.io/Quantum-Technology/](https://ai-crystal.github.io/Quantum-Technology/) 可以从封面进入，按册浏览并下载 PDF。

## 怎么读

第一册是入门，从黑体辐射讲到量子芯片，把整个领域的脉络走一遍，不深究细节。后面几册各自独立，可以按兴趣挑着读，不必按顺序。

每一册的正文都在 `books/<册名>/chapters/`，插图在 `books/<册名>/images/`，绘图代码在 `books/code/<册名>/`。站点直接引用这些文件，没有第二份副本。

## 构建

双击根目录的 `build.bat` 构建全部，或 `build-<册名>.bat` 只构建某一册。

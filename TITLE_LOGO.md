# 在 ACL 标题中加入 Logo（不改 `acl.sty`）

结论：**不需要修改 `acl.sty`**。ACL 的 `\maketitle` 会把 `\title{...}` 里的内容原样排版；标题不仅可以是文字，也可以包含图片宏。心脏 icon 是在 `main.tex` 里定义并写入 `\title{}` 的。

`acl.sty`（仓库根目录）与 `69c7ffb776a8821cc0f99c65/acl.sty` 内容完全一致，均无 heart / logo / `includegraphics` 相关逻辑。

## 原理

`acl.sty` 中标题的排版只有：

```tex
{\Large\bfseries \@title \par}
```

`\@title` 是 `\title{...}` 存下来的 token，不是纯字符串。因此只要在 `\title{}` 里放入一个会展开成插图的宏，logo 就会和文字一起出现在标题中。样式文件不需要知道标题里有图。

## 实现（全部在 `main.tex`）

### 1. 加载插图包

```tex
\usepackage{graphicx}
```

### 2. 定义“当字符用”的 logo 宏

```tex
\newcommand{\heartbenchicon}{%
  \raisebox{-0.2\height}{\includegraphics[height=1.5em]{figures/heart-bench-logo.png}}%
  \hspace{0.3em}
}
```

细节：

- `height=1.5em`：相对标题字号缩放，换字号时 logo 会跟着变。
- `\raisebox{-0.2\height}`：图片默认贴在基线上会显得偏高，往下沉一点与文字对齐。
- `\hspace{0.3em}`：logo 与后面 `HEART-Bench` 之间留空隙。

图片路径：`figures/heart-bench-logo.png`。

### 3. 写入 `\title`

```tex
\title{\heartbenchicon \ourbench: Do LLMs Make Persona-Consistent Decisions?}
```

其中 `\ourbench` 定义为 `\textsc{HEART-Bench}`。`\maketitle` 时先展开 `\heartbenchicon`（插图），再排 `\ourbench` 和副标题。

## 其他模板

`arxiv.tex` 与 `neurips.tex` 使用同一套 `\heartbenchicon` 宏，同样没有改 sty。

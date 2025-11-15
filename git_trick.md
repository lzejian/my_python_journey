# 问题
11月25日（周一）遇到一个问题，我刚在台式机更新内容，笔记本上我发现vscode只能Fetch远程仓库，而不能merge它。

# 原因
原因出在分支上，为了防止文件被随意merge，**分支必须一致**，vscode的pull按钮才能使用。

> **注意：**
> * vsocde的pull按钮命令为 `git pull`，不指向分支名。
> * 快捷方式是 `git pull origin master`（拉取远程的master到当前分支）。

# 解决方案
1. 直接 `git pull origin master` （推荐）
2. 或者：
    * `git checkout master`
    * `git pull`
    * `git checkout chapter_6`
    * `git merge master`
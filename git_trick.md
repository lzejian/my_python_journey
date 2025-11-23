# 问题
10月25日（周一）遇到一个问题，我刚在台式机更新内容，笔记本上我发现vscode只能Fetch远程仓库，而不能merge它。

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

######################################################

# 问题
11月23日（周日）遇到一个问题，print(average:.2f)无法运行。

# 原因
原因是因为我把里面当作是一个变量来考虑的。**print无法理解单独的（:）**，它不懂你要写字典，还是if：等等....。

> **注意：**
> .2f并非是把数字变成了浮点型，而是变成一个字符串，所以要加f""。

# 解决方案
改成print(f"{average:.2f}")
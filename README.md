# Tools 目录项目

该项目为系统脚本项目，为实现多方面的功能编写可执行 `shell` 脚本，并且已将当前路径添加到环境变量中，只要在终端输入脚本名称就可执行脚本。

> 环境

- **系统：** MacOS
- **CPU：** M1 Pro (arm64)
- **SHELL：** zsh

## 项目

> [Mihomo Party](https://github.com/mihomo-party-org/mihomo-party) 内核替换

`Mihomo Party` 默认使用的是官方 [`mihomo`](https://github.com/MetaCubeX/mihomo) 内核，但是 [`vernesong`](https://github.com/vernesong/mihomo) 大佬为官方内核新增了 `SMART` 类型的智能分组，我们的新配置文件已支持 `SMART` 类型，当时官方内核并不支持，所以我们要将 `Mihomo Party` 软件所使用的官方内核替换为 `vernesong` 大佬的官改内核。

**脚本名称：** msmart

**官改最新版本：** <https://github.com/vernesong/mihomo/releases/download/Prerelease-Alpha/version.txt>

**内核下载链接：** <https://github.com/vernesong/mihomo/releases/download/Prerelease-Alpha/mihomo-darwin-arm64-{版本号}.gz>

**基础版本官改内核链接：** <https://abcxxx.com/mihomo-darwin-arm64-vernesong>

**`Mihomo Party` 内核路径：** /Applications/Mihomo\ Party.app/Contents/Resources/sidecar/mihomo-alpha

需求：

0. 通过 `mihomo-alpha -v` 获取当前内核版本，正常输出如下："Mihomo Meta alpha-smart-c9feacd darwin arm64 with go1.24.4 Sun Jul  6 14:49:31 UTC 2025
Use tags: with_gvisor"；如果找不到内核，直接执行 `第3步`。

1. 我们需要通过在输出内容中的 `**第一行**` 中找到 `当前内核版本` - `alpha-smart-c9feacd` 。
2. 判断当前内核版本是否有 `smart` ，如果没有，
3. 先将本地缓存的官改内核复制 `Mihomo Party` 的内核，并重启 `Mihomo Party` ，等待10秒钟，让 `Mihomo Party` 重启完毕，接着执行 `第5步`。
4. 如果没有本地缓存的官改内核， 先关闭 `Mihomo Party` 应用，并等待5秒钟再继续，由于我们关闭了 `Mihomo Party`，终端带代理已经不存在了，所以我们要使用 `curl` 的 `--noproxy '*'` 参数下载一个 `基础版本官改内核` 替换 `Mihomo Party` 的当前内核，并重启 `Mihomo Party`， 等待10秒钟再继续。
5. 获取最新官改版本号。
6. 如果最新内核版本号和当前使用的内核版本号相同则不进行更新，提示用户并终止脚本。
7. 如果版本号不同：
8. 检查之前下载并解压的内核是否存在，如果存在检查内核版本版本并复制。
9. 如果不存在，则下载最新内核解压并复制。
10. 复制到 `Mihomo Party` 的内核（替换内核文件需要 `sudo` 权限）。
11. 修改官改内核的所有者：`root:admin`。
12. 修改官改内核权限为：`+sx`。
13. 重启 `Mihomo Party` 程序。

# 请期待雀魂MAX原作者的一番街MAX，本仓库已归档。

# 麻雀一番街Try

本项目目前只支持麻雀一番街解锁全角色、全皮肤，其余功能正在开发。

这是一个对[雀魂MAX](https://github.com/Avenshy/MajsoulMax)的拙劣模仿，同样采用了mitmproxy中间人攻击方式，但是我的代码水平远远不够，封装的远没有雀魂MAX透彻、完成度也远不及雀魂MAX。写该项目的过程中使用了ChatGPT等AI工具。

**请注意，该项目纯粹是学习、交流使用，请使用者于下载24小时内自行删除，请不要用于商业用途，否则后果自负。如有侵权请联系，我会尽力尽快配合。**

还有，不要嫌（至少不要骂）我的代码烂，如果你觉得烂，那你就去建设它（），我很欢迎代码水平比我强的人的PR！

作者是懒比，本项目不保证任何人的使用！**官方极有可能检测到本工具并封号，如产生任何后果与作者无关，使用即代表同意此点。**

解锁效果仅在本地有效，其他人看到的还是你原来的效果。

# 使用方法

通过git clone或其他方式下载源码到本地，在Python>=3.10环境下，打开命令行，在当前目录运行``mitmproxy -p 12345 -s main.py --set block_global=false --set block_private=false --ssl-insecure``启动程序（首次运行需``pip install -r requirements.txt``安装依赖）

**使用前，请务必关闭Clash、V2ray等代理服务**

运行Proxifier并配置
 - Profile > Proxy Servers > Add
 - Address: 127.0.0.1
 - Port: 12345
 - Protocol: HTTPS
 - 填写完后点击Check，确保看到Test 1下显示绿色的Test passed，其他的不用管
 - OK

Profile > Proxification Rules > Add
 - Name: 随便起个名字
 - Enabled: ✅
 - Applications: 根据你运行游戏的应用填写，例如Steam客户端填写mahjong-jp.exe
 - Action: Proxy HTTPS 127.0.0.1
 - OK

# 目前已知问题

使用的时候会报错，只要没有影响功能就不用管。（因为代码写的太屎了，等重构吧）

有的时候开始游戏后会卡死，这种情况把脚本和Proxifer全部退出后重启游戏即可解决。

缺少换立直棒、特效、桌布、解锁全语音等功能，等后期更新。

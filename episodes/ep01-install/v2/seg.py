import json
C=lambda t,x:{"t":t,"text":x}
S=[
dict(id="hook",type="A",a=10.0,b=22.4,page={"type":"big","badge":"开场","title":"眼红又劝退","quote":"看别人用 AI 自动干活\n自己一搜 [满屏英文术语]","note":"还没开始学，心已经累了","side":{"kicker":"这套课给谁","icon":"user","headline":"零基础的\n普通人","sub":"不讲术语 · 跟着点"}},
 caps=[C(10.5,"看别人用 WorkBuddy [自动干活]"),C(13.1,"眼红得不行"),C(14.4,"结果自己一搜教程"),C(15.8,"满屏的 [英文术语]"),C(18.3,"这时候还没开始学"),C(20.3,"心已经 [非常累了]")]),
dict(id="goal",type="A",a=22.4,b=39.3,page={"type":"steps","badge":"本课目标","title":"第 1 课：把它请进电脑","steps":[{"title":"招人进来","desc":"官网下载 · 安装 · 扫码进入"},{"title":"塞本活字典","desc":"装上中文技能包「蓝皮书」"},{"title":"直接问它","desc":"哪里不会，随问随答"}],"side":{"kicker":"只需要","icon":"clock","headline":"3 分钟","sub":"把 AI 员工请进门"}},
 caps=[C(22.5,"别担心，不用到处搜教程了"),C(24.9,"今天是《把 AI 养成你的员工》[第 1 课]"),C(27.7,"只需要 [3 分钟]"),C(29.4,"把这个外包兄弟 [请进你的电脑]"),C(33.6,"再往它脑子里塞一本 [随问随答的活字典]"),C(36.7,"以后哪里不会，直接问它就行")]),
dict(id="site",type="B",a=39.3,b=51.2,page={"title":"第一步：招人进来","subtitle":"认准官方网站下载","screen":{"url":"WorkBuddy 官网","step":"STEP 1"},"side":{"kicker":"认准","icon":"globe","headline":"官方标志\n的网站","sub":"认准再下载"}},
 screen={"kind":"zoom","raw":"win.mov","raw_start":39.3,"events":"ev_s3.jsonl"},
 caps=[C(39.4,"第一步：先把人 [招进来]"),C(40.7,"怎么招呢？"),C(41.7,"在浏览器里直接搜 [WorkBuddy]"),C(43.5,"认准 [官方标志] 的网站"),C(46.6,"点进来"),C(48.0,"点 [下载]"),C(48.9,"然后点这里的下载链接")]),
dict(id="install",type="A",a=51.2,b=69.4,page={"type":"compare","badge":"安装","title":"安装避坑","compare":{"left":{"label":"苹果电脑","name":"Mac","points":["拖进「应用程序」文件夹","拖完就装好"]},"right":{"label":"Windows","name":"改安装路径","points":["别一路闭眼点「下一步」","默认 C 盘 → 改为 D 盘","不然 C 盘容易爆红"]}},"side":{"kicker":"Windows 必看","icon":"folder","headline":"C 盘\n改 D 盘","sub":"剪视频、存文件都占地方"}},
 caps=[C(51.3,"[苹果电脑] 注意了"),C(53.6,"直接拖进 [应用程序] 文件夹"),C(55.7,"Windows 的朋友一定要 [注意避坑]"),C(58.8,"千万别一路闭眼点「下一步」"),C(62.0,"把默认路径的 [C 盘改为 D 盘]"),C(64.5,"不然以后它帮你剪视频、存文件"),C(66.5,"几个月下来 [C 盘直接爆红]")]),
dict(id="login",type="A",a=69.4,b=75.6,page={"type":"big","badge":"登录","title":"打开就能用","quote":"装好打开\n[扫个码] 就能进来","note":"那么，重点来了","side":{"kicker":"进门方式","icon":"phone","headline":"扫码\n登录","sub":"不用记账号密码"}},
 caps=[C(69.5,"装好，我们打开"),C(72.4,"[扫个码] 就能进来"),C(74.2,"那么，[重点来了]")]),
dict(id="blank",type="A",a=75.6,b=86.4,page={"type":"big","badge":"痛点","title":"装完不知道问啥？","quote":"对着空白输入框\n[一顿发懵]","note":"就像新员工第一天上班，得先发本《员工手册》","side":{"kicker":"新员工入职","icon":"book","headline":"先发\n员工手册","sub":"它才知道怎么帮你"}},
 caps=[C(75.7,"很多人装完对着空白输入框 [一顿发懵]"),C(79.8,"第一句都不知道问啥"),C(81.1,"就像新员工第一天上班"),C(82.7,"你不得给他发本 [《员工手册》]？")]),
dict(id="book",type="A",a=86.4,b=97.5,page={"type":"list","badge":"活字典","title":"中文技能包「蓝皮书」","items":[{"title":"官方 28 章使用文档","icon":"book"},{"title":"打包成中文技能包","icon":"skill"},{"title":"跟着点三下就装上","icon":"cursor","warm":True}],"side":{"kicker":"名字叫","icon":"book","headline":"蓝皮书","sub":"随问随答的活字典"}},
 caps=[C(86.6,"我把官方厚厚一沓的 [28 章] 使用文档"),C(91.2,"打包成了一个 [中文技能包]"),C(93.5,"叫做 [蓝皮书]"),C(94.2,"你只要跟我 [点三下] 就能装上")]),
dict(id="skill",type="B",a=97.5,b=136.4,page={"title":"安装蓝皮书","subtitle":"技能 → 搜索 → 安装","screen":{"url":"WorkBuddy · 技能","step":"STEP 2"},"side":{"kicker":"搜索框输入","icon":"skill","headline":"lhg-wb\n-bluebook","sub":"安装 → 去试试"}},
 screen={"kind":"demo","off":0},
 caps=[C(98.0,"点左边的 [技能]"),C(100.2,"选中技能"),C(102.0,"在 [搜索框] 里搜索技能"),C(106.9,"输入 [lhg-wb]"),C(112.9,"搜到了，它就出来了"),C(117.9,"这里点击 [安装]"),C(127.2,"点击 [去试试]")]),
dict(id="ask",type="B",a=136.4,b=255.6,page={"title":"直接问它","subtitle":"按官方手册作答","screen":{"url":"WorkBuddy · 对话","step":"STEP 3"},"side":{"kicker":"第一句就问","icon":"chat","headline":"零基础\n先干哪三件？","sub":"不用再去外面搜教程"}},
 screen={"kind":"demo"},
 caps=[C(136.5,"你看，现在根本不用去外面搜教程"),C(139.2,"[直接问它]"),C(141.5,"“我是零基础，你能帮我干 [哪三件] 最省时间的事？”"),C(146.2,"（它正在翻手册作答…）"),C(195.3,"它马上根据官方手册 [列得明明白白]"),C(220.6,"分析得很细"),C(238.2,"甚至连怎么 [免积分用模型]"),C(241.2,"怎么连 [绿泡泡]"),C(243.3,"它都能 [手把手教你]"),C(246.2,"甚至连怎么免积分用模型"),C(250.6,"怎么连 [绿泡泡]"),C(253.1,"它都能手把手教你")]),
dict(id="next",type="A",a=255.6,b=303.5,page={"type":"big","badge":"下一课","title":"下一课预告","quote":"左边这排按钮\n怎么点才 [不会删错文件]？","note":"2 分钟摸透工作台 · 顺便连上绿泡泡","side":{"kicker":"关注我","icon":"play","headline":"下一课\n摸透工作台","sub":"按钮 · 选项一次讲清"}},
 caps=[C(255.7,"现在人招进来了"),C(257.2,"活字典也发给它了"),C(258.4,"但左边这一排按钮到底怎么点"),C(264.0,"才不会 [删错] 你电脑里的文件？"),C(277.5,"左边这排按钮和下方这些选项"),C(290.6,"到底怎么点"),C(291.6,"才不会删错你电脑里的文件"),C(293.8,"[关注我]，下一课"),C(295.2,"带你 [2 分钟] 摸透它的工作台"),C(297.7,"顺便把你的 [绿泡泡] 连上去")]),
dict(id="cta",type="A",a=303.5,b=327.0,page={"type":"cta","badge":"福利","title":"怕技能名打错？","cta":{"lead":"评论区扣","word":"蓝皮书","get":"领 [必装技能名称清单]"},"side":{"kicker":"技能名","icon":"key","headline":"lhg-wb\n-bluebook","sub":"复制粘贴不出错"}},
 caps=[C(303.6,"怕刚才技能名字打错的朋友"),C(320.4,"在评论区扣 [蓝皮书]"),C(322.4,"我把全套 [必装名称清单] 发给你")]),
]
json.dump(S,open('segs.json','w'),ensure_ascii=False,indent=0)
print(len(S),sum(len(s['caps']) for s in S))

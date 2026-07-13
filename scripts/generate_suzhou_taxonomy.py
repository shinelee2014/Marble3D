import json
import os

def main():
    # Make sure we are in the correct directory
    os.makedirs("d:/antigravity/app/Taxonomy/data", exist_ok=True)
    os.makedirs("d:/antigravity/app/Taxonomy/scripts", exist_ok=True)

    # 1. Define local curriculum subjects and standard age maps
    # Grade mapping:
    # Grade 1: Age 6-7
    # Grade 2: Age 7-8
    # Grade 3: Age 8-9
    # Grade 4: Age 9-10
    # Grade 5: Age 10-11
    # Grade 6: Age 11-12
    
    # We will define a structured list of topics.
    topics = []
    dependencies = []
    
    # Help lists
    subjects = ["语文", "数学", "英语", "科学", "道德与法治", "信息技术", "生活技能"]
    
    # Unique IDs generator
    # We'll prefix IDs with standard prefixes: sz_chn_*, sz_math_*, sz_eng_*, sz_sci_*, sz_mor_*, sz_inf_*, sz_lab_*
    
    # ==========================================
    # SUBJECT: 数学 (苏教版 K-6)
    # ==========================================
    math_data = [
        # Grade 1
        {"grade": 1, "id": "sz_math_1_1", "name": "20以内数的认识与加减法", "domain": "数与代数", "desc": "学习20以内物体的数量、数位、大小比较及不进位/进位加减法，掌握手口一致数数与基本凑十法。", "evidence": ["能快速点数出20以内的积木并报数", "能用凑十法熟练心算15-8等算式"], "prompt": "{{name}}，桌上有8个红苹果和5个青苹果，一共几个？你是怎么用凑十法算的？"},
        {"grade": 1, "id": "sz_math_1_2", "name": "认识图形（一）", "domain": "图形与几何", "desc": "认识长方体、正方体、圆柱和球等立体图形，学习分类与堆叠。", "evidence": ["能在日常中指出肥皂盒是长方体、魔方是正方体", "能用积木搭高楼并解释球为什么容易滚下来"], "prompt": "{{name}}，找一找客厅里有哪些东西是长方体的，哪些是圆柱体的？"},
        {"grade": 1, "id": "sz_math_1_3", "name": "100以内数的认识与加减", "domain": "数与代数", "desc": "认识100以内的数位（个位、十位、百位），掌握整十数加减及两位数加减一位数的笔算。", "evidence": ["能口算 40+30 和两位数不退位减法", "懂得35里面有3个十和5个一"], "prompt": "{{name}}，妈妈买了35个草莓，爸爸吃了20个，还剩几个？"},
        {"grade": 1, "id": "sz_math_1_4", "name": "认识人民币", "domain": "数与代数", "desc": "认识元、角、分及面值，学会简单的付钱、找零和等值兑换。", "evidence": ["能在超市买小零食时递给收银员正确的纸币", "知道 1 元可以换 10 个 1 角"], "prompt": "{{name}}，一块橡皮要8角，你给老板1元，老板应该找你多少钱？"},
        
        # Grade 2
        {"grade": 2, "id": "sz_math_2_1", "name": "表内乘法", "domain": "数与代数", "desc": "理解乘法的含义（求几个相同加数的和的简便运算），熟记1-9乘法口诀并应用。", "evidence": ["能脱口而出‘七八五十六’等乘法口诀", "看到 4 盘苹果，每盘 5 个，能快速列出 4x5 算式"], "prompt": "{{name}}，每只兔子吃3个萝卜，6只兔子一共要吃多少个？你能用口诀背出来吗？"},
        {"grade": 2, "id": "sz_math_2_2", "name": "表内除法", "domain": "数与代数", "desc": "理解等分和包含的含义，熟练运用乘法口诀求商，初步认识余数。", "evidence": ["能将24个糖果平均分给4个小朋友并列出算式", "知道除法是乘法的逆运算"], "prompt": "{{name}}，把18个苹果平均装在3个袋子里，每个袋子装几个？"},
        {"grade": 2, "id": "sz_math_2_3", "name": "厘米和米", "domain": "图形与几何", "desc": "认识长度单位厘米（cm）和米（m），学会用直尺测量物体长度并估测物距。", "evidence": ["能用直尺准确量出铅笔长多少厘米", "知道课桌高约1米，而不是1厘米"], "prompt": "{{name}}，量量你的这本课外书有多宽？大约是多少厘米？"},
        {"grade": 2, "id": "sz_math_2_4", "name": "时、分、秒的认识", "domain": "数与代数", "desc": "认识钟面上的时针、分针、秒针，学会读写整时、半时和几时几分，理解 1时=60分。", "evidence": ["能看着挂钟准确说出当前是几点几分", "知道秒针走一小格是一秒，眨眼大概是一秒"], "prompt": "{{name}}，分针指着6，时针在4和5之间，现在是几点几分？"},
        
        # Grade 3
        {"grade": 3, "id": "sz_math_3_1", "name": "两三位数乘一位数", "domain": "数与代数", "desc": "掌握两三位数乘一位数的笔算乘法（包含进位），能解决倍数关系的应用题。", "evidence": ["能笔算 125x8 并得出正确答案", "能列式解答“小红有6张画片，小明是她的3倍”"], "prompt": "{{name}}，小超市每天卖出120瓶牛奶，5天一共卖出多少瓶？列式并口算一下。"},
        {"grade": 3, "id": "sz_math_3_2", "name": "千克和克", "domain": "综合与实践", "desc": "认识重量单位克（g）和千克（kg），理解 1千克=1000克，学会用秤测量重量。", "evidence": ["知道一袋盐重约500克，两袋盐重1千克", "能掂量并估测一个苹果大概重多少克"], "prompt": "{{name}}，如果一个苹果重200克，几个这样的苹果重1千克？"},
        {"grade": 3, "id": "sz_math_3_3", "name": "长方形和正方形周长", "domain": "图形与几何", "desc": "掌握长方形和正方形的特征，理解周长的含义并熟练计算周长公式。", "evidence": ["能指出操场的周长是绕操场跑一圈的长度", "能计算长 5 厘米、宽 3 厘米的长方形卡片周长为 16 厘米"], "prompt": "{{name}}，一个正方形花坛边长是8米，小狗绕它跑一圈是多少米？"},
        {"grade": 3, "id": "sz_math_3_4", "name": "分数的初步认识", "domain": "数与代数", "desc": "初步理解几分之一和几分之几的含义，能进行同分母分数的简单加减运算。", "evidence": ["能将一张纸折出四分之一并涂色", "能口算 1/5 + 2/5 = 3/5"], "prompt": "{{name}}，一块西瓜切成8份，小明吃了3份，小红吃了2份，他们一共吃了这块西瓜的几分之几？还剩几分之几？"},
        
        # Grade 4
        {"grade": 4, "id": "sz_math_4_1", "name": "升和毫升", "domain": "综合与实践", "desc": "认识容量单位升（L）和毫升（mL），理解 1升=1000毫升，建立常见容器的容量感。", "evidence": ["知道一瓶大矿泉水约2升，一小瓶口服液约10毫升", "能做简单的升和毫升的单位换算"], "prompt": "{{name}}，一瓶果汁有500毫升，几瓶这样的果汁加起来是2升？"},
        {"grade": 4, "id": "sz_math_4_2", "name": "三位数乘两位数", "domain": "数与代数", "desc": "掌握三位数乘两位数的笔算与估算，能熟练运用乘法分配律等运算律进行简便计算。", "evidence": ["能列竖式计算 234x12 并验算", "能运用简便方法口算 99x35 = (100-1)x35"], "prompt": "{{name}}，一列动车一小时跑245公里，跑了12小时，一共跑了多少公里？"},
        {"grade": 4, "id": "sz_math_4_3", "name": "平行和相交", "domain": "图形与几何", "desc": "认识射线、直线，理解两条直线的位置关系——平行与垂直，学会画垂线和平行线。", "evidence": ["能在日常中指出铁轨是平行的，十字路口是垂直相交的", "能用三角尺画出已知直线的垂线"], "prompt": "{{name}}，在同一张白纸上，如果两条直线怎么延长都不碰头，这两条直线是什么关系？"},
        {"grade": 4, "id": "sz_math_4_4", "name": "解决问题的策略（列表/画图）", "domain": "数与代数", "desc": "学会用整理信息的方法（列表、画线段图）来分析复杂的两步/三步混合运算应用题。", "evidence": ["能根据题目中的数量关系画出对应的线段图", "能用列表法把多组未知数理清并列式"], "prompt": "{{name}}，小明买3本故事书花24元，小红想买8本同样的故事书，需要多少钱？你能不能画线段图表示出来？"},
        
        # Grade 5
        {"grade": 5, "id": "sz_math_5_1", "name": "负数的初步认识", "domain": "数与代数", "desc": "认识负数，理解正数和负数可以表示相反方向或意义的量（如温度、海拔、收支）。", "evidence": ["在温度计上能读出零下5度为 -5°C", "坐电梯时知道地下二层表示为 -2 层"], "prompt": "{{name}}，如果小明存入100元记作+100元，那么他取出60元应该怎么记？"},
        {"grade": 5, "id": "sz_math_5_2", "name": "多边形的面积", "domain": "图形与几何", "desc": "掌握平行四边形、三角形和梯形的面积计算公式，理解割补、拼摆的面积推导方法。", "evidence": ["能通过割补法把平行四边形转化成长方形来解释其面积公式", "计算出底 6 厘米，高 4 厘米的三角形面积是 12 平方厘米"], "prompt": "{{name}}，一个三角形的底是10米，高是6米，它的面积是多少？如果拼成平行四边形呢？"},
        {"grade": 5, "id": "sz_math_5_3", "name": "小数乘法和除法", "domain": "数与代数", "desc": "掌握小数乘除法的计算法则，理解小数点移动引起小数大小变化的规律，能解决实际问题。", "evidence": ["计算出 0.3x0.2 = 0.06，并解释为什么是两位小数", "会把商用四舍五入法保留两位小数"], "prompt": "{{name}}，一斤苹果4.5元，买3.6斤需要付多少钱？小数点应该点在哪里？"},
        {"grade": 5, "id": "sz_math_5_4", "name": "因数与倍数", "domain": "数与代数", "desc": "认识因数和倍数，掌握2、3、5的倍数特征，理解质数、合数、公因数与公倍数。", "evidence": ["能快速判断出15的因数有1、3、5、15", "找出6和8的最小公倍数是24"], "prompt": "{{name}}，一个数既是12的倍数，又是12的因数，这个数是多少？它是不是质数？"},
        
        # Grade 6
        {"grade": 6, "id": "sz_math_6_1", "name": "长方体和正方体（体积/表面积）", "domain": "图形与几何", "desc": "掌握长方体和正方体的特征，熟练计算其表面积与体积，建立立方米、升、毫升的换算感。", "evidence": ["能算出长5cm,宽4cm,高3cm的长方体纸盒表面积是94平方厘米", "能算出它的体积是60立方厘米"], "prompt": "{{name}}，把一个棱长是3分米的正方体木块放进水里，它占了多少升的空间？它的表面积是多少？"},
        {"grade": 6, "id": "sz_math_6_2", "name": "分数乘法和除法", "domain": "数与代数", "desc": "掌握分数乘除法的计算法则，理解分数乘除应用题中“单位1”的判定并列方程解决。", "evidence": ["能口算 4/5 * 5/8 = 1/2", "解决“一本书看了3/4，正好是60页，求全书页数”的应用题"], "prompt": "{{name}}，小刚体重35千克，小明体重是小刚的4/5，小明有多重？如果是小明体重的4/5是小刚，小明多重？"},
        {"grade": 6, "id": "sz_math_6_3", "name": "比和百分数", "domain": "数与代数", "desc": "理解比与除法、分数的联系，掌握化简比和求比值，理解百分数的意义及百分率计算。", "evidence": ["将 12:18 化简为最简整数比 2:3", "算出全班50人，今天缺勤2人，出勤率是96%"], "prompt": "{{name}}，调制一杯含糖率是10%的糖水，如果糖有20克，需要多少克水？比值是多少？"},
        {"grade": 6, "id": "sz_math_6_4", "name": "比例与比例尺", "domain": "图形与几何", "desc": "理解比例的意义和基本性质，解比例方程，认识正比例与反比例，应用比例尺计算。", "evidence": ["会根据 3:x = 6:10 解出 x = 5", "在 1:100000 的地图上量得两地距离 5 厘米，算出实际距离 5 千米"], "prompt": "{{name}}，如果小明的身高和他的影长成正比例，他在量出自己身高 1.5 米时影长 1.2 米，旁边大树影长 8 米，大树多高？"},
    ]
    
    # Add math to topics
    for item in math_data:
        topics.append({
            "id": item["id"],
            "type": "CONCEPTUAL",
            "subject": "数学",
            "domain": item["domain"],
            "name": item["name"],
            "description": item["desc"],
            "ageRangeStart": 5 + item["grade"],  # Grade 1 maps to Age 6, etc.
            "ageRangeEnd": 6 + item["grade"],
            "centrality": 0.05 + (item["grade"] * 0.01),
            "evidence": item["evidence"],
            "assessmentPrompt": item["prompt"],
            "standards": [f"SZ.MATH.{item['grade']}.{item['id'][-1]}"]
        })

    # Add math inner-dependencies
    # e.g., sz_math_1_1 (20以内加减) -> sz_math_1_3 (100以内加减)
    # sz_math_1_3 -> sz_math_2_1 (表内乘法)
    # sz_math_2_1 -> sz_math_2_2 (表内除法)
    # sz_math_2_2 -> sz_math_3_1 (两三位数乘一位数)
    # sz_math_1_2 (认识立体图形) -> sz_math_3_3 (面积周长)
    # sz_math_3_4 (分数初步) -> sz_math_6_2 (分数乘除)
    # sz_math_6_2 -> sz_math_6_3 (比和百分数) -> sz_math_6_4 (比例)
    math_deps = [
        ("sz_math_1_1", "sz_math_1_3", "20以内加减法是100以内加减法的基础"),
        ("sz_math_1_3", "sz_math_2_1", "加法是乘法的基础，乘法是求相同加数的简便运算"),
        ("sz_math_2_1", "sz_math_2_2", "乘法口诀是表内除法求商的直接逆运算"),
        ("sz_math_2_2", "sz_math_3_1", "一位数乘除法熟练是两三位数乘法笔算的前提"),
        ("sz_math_1_2", "sz_math_2_3", "感知立体图形的边界有助于理解线段和长度度量"),
        ("sz_math_2_3", "sz_math_3_3", "掌握厘米和米等长度单位是计算长方形周长的前提"),
        ("sz_math_3_4", "sz_math_6_2", "分数的初步认识是进行分数乘除法计算的认知起点"),
        ("sz_math_6_2", "sz_math_6_3", "分数除法的逆运算关系直接用于理解比的意义和百分数换算"),
        ("sz_math_6_3", "sz_math_6_4", "比的化简与等值关系是比例方程建立的数学基础")
    ]
    for src, tgt, reason in math_deps:
        dependencies.append({
            "topicId": tgt,
            "prerequisiteId": src,
            "reason": reason
        })

    # ==========================================
    # SUBJECT: 语文 (部编版 K-6)
    # ==========================================
    chn_data = [
        # Grade 1
        {"grade": 1, "id": "sz_chn_1_1", "name": "汉语拼音（声母韵母与拼读）", "domain": "拼音与识字", "desc": "学习23个声母、24个韵母和16个整体认读音节，掌握声调标调规则与拼读方法。", "evidence": ["能看着拼音准确读出生字音节", "能自主给简单的汉字标出声调"], "prompt": "{{name}}，拼读一下这三个音节：b-à-ba，m-ā-ma，sh-ū-b-ā-o？"},
        {"grade": 1, "id": "sz_chn_1_2", "name": "汉字笔画与基本偏旁", "domain": "拼音与识字", "desc": "掌握汉字书写的基本笔顺规则（先横后竖、先撇后捺等）和常见偏旁（三点水、单人旁等）。", "evidence": ["写字时不会乱笔顺，能说出‘江’是三点水旁", "能用手指在空中比划‘水’字的笔顺"], "prompt": "{{name}}，‘国’字是怎么写的？是不是先写里面的‘玉’再封口？‘你’字是什么偏旁？"},
        {"grade": 1, "id": "sz_chn_1_3", "name": "看图写话初步", "domain": "阅读与写作", "desc": "观察单幅或多幅图画，用一两句完整的话写出图里有谁、在什么地方、干什么。", "evidence": ["能口头说出图画中的小动物在干嘛", "能写出一句包含时间、地点、人物和事件的话"], "prompt": "{{name}}，看着这张图，你能写一句话告诉妈妈：小猫在什么时候，在哪里，干什么吗？"},
        
        # Grade 2
        {"grade": 2, "id": "sz_chn_2_1", "name": "部首查字法与查字典", "domain": "语言积累", "desc": "学会使用字典的部首查字法，根据生字的部首和除去部首的笔画数定位生字。", "evidence": ["能在两分钟内通过部首查字法找到字典中的指定生字", "知道遇到不会读的字可以用部首查字法"], "prompt": "{{name}}，‘露’这个字你不会读，它的部首是什么？除掉部首还有几画？去查查字典看它读什么？"},
        {"grade": 2, "id": "sz_chn_2_2", "name": "近义词与反义词", "domain": "词语学习", "desc": "掌握常用词汇的近义词（如美丽与漂亮）和反义词（如高与矮、多与少）。", "evidence": ["能口头脱口说出‘开心’的反义词和近义词", "在句子中能用近义词做替换"], "prompt": "{{name}}，‘寻找’的近义词是什么？‘安全’的反义词是什么？"},
        {"grade": 2, "id": "sz_chn_2_3", "name": "简单比喻句与拟人句", "domain": "阅读与写作", "desc": "认识比喻句（把什么比作什么）和拟人句（把事物当作人来写），体会句子的生动感。", "evidence": ["能说出“弯弯的月亮像小船”里把月亮比作了什么", "能说出“小鸟在枝头唱歌”是拟人手法"], "prompt": "{{name}}，天空中的白云像什么？你能写个句子，把白云比作别的东西吗？"},
        
        # Grade 3
        {"grade": 3, "id": "sz_chn_3_1", "name": "词语搭配与成语积累", "domain": "词语学习", "desc": "掌握“的、地、得”的用法和成语，学会积累并使用课文中的成语。", "evidence": ["能正确写出“飞快地跑”、“跑得快”、“美丽的花”", "能在写话中使用“自言自语”等成语"], "prompt": "{{name}}，‘认真（）写字’和‘扫（）干干净净’，括号里应该填‘的、地、得’中的哪一个？"},
        {"grade": 3, "id": "sz_chn_3_2", "name": "童话与寓言理解", "domain": "阅读理解", "desc": "阅读童话和寓言故事，能说出故事里的角色和它传达的道理（寓意）。", "evidence": ["看完《守株待兔》后能说出为什么不能不劳而获", "能分角色有感情地朗读童话故事"], "prompt": "{{name}}，听完《揠苗助长》的故事，那个农夫为什么急着拔禾苗？最后为什么禾苗都枯死了？它告诉我们什么道理？"},
        {"grade": 3, "id": "sz_chn_3_3", "name": "基础习作与标点符号规范", "domain": "阅读与写作", "desc": "写一段通顺的话，能正确使用逗号、句号、问号、叹号，初步学会使用引号。", "evidence": ["写作时不再一段到底，知道句末要加句号", "能正确在对话中使用冒号和双引号"], "prompt": "{{name}}，当写到“妈妈说”时，后面应该用什么标点符号？说话的内容用什么符号包起来？"},
        
        # Grade 4
        {"grade": 4, "id": "sz_chn_4_1", "name": "缩句与扩句技巧", "domain": "句式训练", "desc": "学会提炼句子的主干（去掉修饰词，留下主谓宾），以及在主干上添加形容词和副词进行扩写。", "evidence": ["能把“美丽的小红快步走进了教室”缩写为“小红走进教室”", "能把“星星眨眼”扩写成生动的句子"], "prompt": "{{name}}，把“可爱的蓝精灵在森林里快活地唱歌”缩写成最简单的一句话，应该是什么？"},
        {"grade": 4, "id": "sz_chn_4_2", "name": "段落大意与中心句归纳", "domain": "阅读理解", "desc": "阅读段落，找出或归纳段落的中心句（主旨句），总结段落大意。", "evidence": ["能快速指出段落开头或结尾的概括性句子", "能用一句话说出某个自然段讲了什么"], "prompt": "{{name}}，读一读这一段，作者是围绕哪一句话来写秋天的美丽的？"},
        {"grade": 4, "id": "sz_chn_4_3", "name": "书信与应用文写作", "domain": "阅读与写作", "desc": "掌握书信、请假条等应用文的格式（称呼、正文、祝颂语、署名和日期）。", "evidence": ["能写出一张格式完全正确的请假条", "知道书信的称呼要在第一行顶格写"], "prompt": "{{name}}，写信时的“祝您身体健康”应该写在什么位置？名字和日期又写在哪里？"},
        
        # Grade 5
        {"grade": 5, "id": "sz_chn_5_1", "name": "说明文阅读与说明方法", "domain": "阅读理解", "desc": "理解说明文的结构，辨析常用的说明方法（列数字、作比较、举例子、打比方）。", "evidence": ["能指出“太阳离我们约1.5亿公里”使用了列数字的说明方法", "能说出说明文是为了介绍客观事物的特征"], "prompt": "{{name}}，课文里说“松鼠像猫一样敏捷”，这用了什么说明方法？为什么作者要拿猫来比？"},
        {"grade": 5, "id": "sz_chn_5_2", "name": "成语典故与词义辨析", "domain": "语言积累", "desc": "学习历史成语典故（如负荆请罪、完璧归赵），辨析同义词的感情色彩和词性差异。", "evidence": ["能讲出《负荆请罪》背后的历史人物和故事", "能区分“果断”和“武断”在感情色彩上的褒贬不同"], "prompt": "{{name}}，你知道‘廉颇负荆请罪’是向谁请罪吗？‘果断’和『武断』哪个是夸人的词？"},
        {"grade": 5, "id": "sz_chn_5_3", "name": "中长篇记叙文写作（人物与事件）", "domain": "阅读与写作", "desc": "能够写一篇400字以上的中长篇记叙文，交代清楚时间、地点、人物、起因、经过、结果，并有简单的细节描写。", "evidence": ["能写出某次难忘活动的经过，有心理和神态描写", "文章逻辑清晰，段落之间有合理过渡"], "prompt": "{{name}}，我们要写一篇写人的作文，你打算抓他的什么外貌特征或日常习惯来突出他的性格？"},
        
        # Grade 6
        {"grade": 6, "id": "sz_chn_6_1", "name": "病句修改技巧", "domain": "句式训练", "desc": "辨析并修改常见的病句类型（成分残缺、搭配不当、前后矛盾、语序混乱）。", "evidence": ["能指出“我断定他大概是生病了”错在矛盾，并修改为“我断定他生病了”", "能用修改符号纠正句子中的主谓不搭配"], "prompt": "{{name}}，“听了老师的报告，受到了很大的启发”这句话少了什么？应该怎么改？"},
        {"grade": 6, "id": "sz_chn_6_2", "name": "基础文言文阅读与实词", "domain": "古诗文学习", "desc": "阅读简单的小学文言文（如《学弈》、《两小儿辩日》），掌握“之、乎、者、也”的基本意思及通假字。", "evidence": ["能通顺地朗读并断句文言文课文", "知道“弈秋，通国之善弈者也”里“之”是“的”的意思"], "prompt": "{{name}}，‘思援弓缴而射之’中，‘之’指的是什么？‘善’是什么意思？"},
        {"grade": 6, "id": "sz_chn_6_3", "name": "文学常识与修辞手法总复习", "domain": "语言积累", "desc": "梳理并辨析八大修辞手法（比喻、拟人、排比、夸张、反问、设问、对偶、借代），了解中国古代文学常识（唐宋八大家等）。", "evidence": ["能准确指出“危楼高百尺，手可摘星辰”是夸张手法", "知道李白是诗仙，杜甫是诗圣"], "prompt": "{{name}}，‘这难道不是世界上最伟大的爱吗？’这是一个什么句子？它表示肯定还是否定？"},
    ]

    for item in chn_data:
        topics.append({
            "id": item["id"],
            "type": "CONCEPTUAL",
            "subject": "语文",
            "domain": item["domain"],
            "name": item["name"],
            "description": item["desc"],
            "ageRangeStart": 5 + item["grade"],
            "ageRangeEnd": 6 + item["grade"],
            "centrality": 0.04 + (item["grade"] * 0.01),
            "evidence": item["evidence"],
            "assessmentPrompt": item["prompt"],
            "standards": [f"SZ.CHN.{item['grade']}.{item['id'][-1]}"]
        })

    # Add chinese inner-dependencies
    # sz_chn_1_1 (拼音) -> sz_chn_2_1 (查字典)
    # sz_chn_1_2 (笔画偏旁) -> sz_chn_2_1
    # sz_chn_1_2 -> sz_chn_1_3 (看图写话)
    # sz_chn_2_2 (近反义词) -> sz_chn_3_1 (词语搭配)
    # sz_chn_2_3 (比喻拟人) -> sz_chn_3_3 (基础习作)
    # sz_chn_3_3 -> sz_chn_4_3 (应用文)
    # sz_chn_4_1 (缩句扩句) -> sz_chn_6_1 (病句修改)
    # sz_chn_4_2 (中心句归纳) -> sz_chn_5_1 (说明文阅读)
    # sz_chn_3_1 -> sz_chn_5_2 (成语典故)
    # sz_chn_5_3 (记叙文写作) -> sz_chn_6_2 (文言文理解) - maybe cognitive reading progression
    chn_deps = [
        ("sz_chn_1_1", "sz_chn_2_1", "掌握汉语拼音读音是查字典拼音索引和核对部首查字读音的基础"),
        ("sz_chn_1_2", "sz_chn_2_1", "识别汉字偏旁和数对多余笔画是部首查字法的核心技能"),
        ("sz_chn_1_2", "sz_chn_1_3", "笔顺正确能提高汉字书写速度，支持快速完成看图写话"),
        ("sz_chn_2_2", "sz_chn_3_1", "积累近反义词能扩展词汇量，从而进行准确的词语搭配"),
        ("sz_chn_2_3", "sz_chn_3_3", "比喻句和拟人句是写出生动有趣的基础习作的有效表达工具"),
        ("sz_chn_3_3", "sz_chn_4_3", "标点符号规范是完成应用文（请假条/书信）书写的格式要求"),
        ("sz_chn_4_1", "sz_chn_6_1", "缩句找句子主干是快速排查句子成分残缺、搭配不当等病句的基础"),
        ("sz_chn_4_2", "sz_chn_5_1", "提炼段落中心句能帮助理清说明文的结构并快速获取核心说明信息"),
        ("sz_chn_3_1", "sz_chn_5_2", "日常词汇搭配与成语积累是深度学习历史成语典故的基础"),
        ("sz_chn_5_2", "sz_chn_6_2", "成语典故中保留了大量古代汉语语法，是学习文言文实词的前置桥梁")
    ]
    for src, tgt, reason in chn_deps:
        dependencies.append({
            "topicId": tgt,
            "prerequisiteId": src,
            "reason": reason
        })

    # ==========================================
    # SUBJECT: 英语 (译林版 K-6)
    # ==========================================
    eng_data = [
        # Grade 3 (Start of Yilin English)
        {"grade": 3, "id": "sz_eng_3_1", "name": "26个字母与音素初步", "domain": "字母与发音", "desc": "掌握26个英文字母的大小写书写和标准读音，初步感知辅音和元音的开口音。", "evidence": ["能正确在四线三格中写出大小写字母", "能顺畅背诵唱出字母歌并认读随机字母"], "prompt": "{{name}}，在大写字母 G 旁边，小写的 g 应该在四线三格的哪几格写？读一下这个字母？"},
        {"grade": 3, "id": "sz_eng_3_2", "name": "名词的单数与基本代词", "domain": "词汇与语法", "desc": "学习人称代词（I, you, he, she, it）及物主代词（my, your）和名词单数的简单指示句。", "evidence": ["能用 This is my... 介绍自己的物品", "能区分 he 指代男孩，she 指代女孩"], "prompt": "{{name}}，如果想用英文介绍“这是我的书包”，应该怎么说？如果形容她，应该用 he 还是 she？"},
        
        # Grade 4
        {"grade": 4, "id": "sz_eng_4_1", "name": "名词复数的规则变化", "domain": "词汇与语法", "desc": "学习名词复数的普通加 s 规律（如 apples, cats）及部分以 es/ies 结尾的规则变化。", "evidence": ["看到两个香蕉能快速说出 two bananas，而不是 banana", "知道 peach 的复数要加 es 变成 peaches"], "prompt": "{{name}}，一本书是 a book，那么三本书用英文怎么说？"},
        {"grade": 4, "id": "sz_eng_4_2", "name": "常用介词与位置关系", "domain": "词汇与语法", "desc": "掌握常用方位介词（in, on, under, behind, near）的意义及位置表达句型。", "evidence": ["能在桌子下找到书时用 It's under the desk 表达", "能根据指令把铅笔盒放 on the table"], "prompt": "{{name}}，如果你的洋娃娃在床底下，用英文怎么回答？“It is... the bed.”？"},
        
        # Grade 5
        {"grade": 5, "id": "sz_eng_5_1", "name": "一般现在时与第三人称单数", "domain": "词汇与语法", "desc": "掌握一般现在时的句型，重点掌握主语为第三人称单数（he, she, it）时，动词要加 s 或 es 的规则。", "evidence": ["说 He likes apples 而不是 He like apples", "在写句子 She goes to school 时知道 go 要加 es"], "prompt": "{{name}}，用英文说“他每天去学校”，动词 go 应该怎么变化？"},
        {"grade": 5, "id": "sz_eng_5_2", "name": "There be 句型初步", "domain": "句型结构", "desc": "学习 There is / There are 句型表示“某处有某物”，掌握其单复数就近原则及否定句/疑问句变化。", "evidence": ["看到桌上有两个苹果能说 There are two apples on the table", "知道 There is a cup... 单数用 is"], "prompt": "{{name}}，“书包里有一本书”和“书包里有三本书”分别怎么用 There be 句型说？"},
        
        # Grade 6
        {"grade": 6, "id": "sz_eng_6_1", "name": "一般过去时与不规则动词", "domain": "词汇与语法", "desc": "掌握一般过去时，学习常见动词过去式变化（规则加ed，以及不规则变化如 go->went, run->ran, is->was, do->did）。", "evidence": ["叙述昨天做的事情时动词能用过去式", "能默写出 buy 的过去式是 bought"], "prompt": "{{name}}，如果想说“我昨天去公园了”，用 go 还是 went？"},
        {"grade": 6, "id": "sz_eng_6_2", "name": "一般将来时句型", "domain": "句型结构", "desc": "掌握一般将来时的两种表达方式：be going to + 动词原形，以及 will + 动词原形，表达未来的计划和预测。", "evidence": ["能用 I am going to watch a film tomorrow 表达明天的计划", "能正确用 will predict 明天的天气"], "prompt": "{{name}}，你明天打算做什么？用“I am going to...”写一个英文句子。"},
    ]

    for item in eng_data:
        topics.append({
            "id": item["id"],
            "type": "CONCEPTUAL",
            "subject": "英语",
            "domain": item["domain"],
            "name": item["name"],
            "description": item["desc"],
            "ageRangeStart": 5 + item["grade"],
            "ageRangeEnd": 6 + item["grade"],
            "centrality": 0.03 + (item["grade"] * 0.01),
            "evidence": item["evidence"],
            "assessmentPrompt": item["prompt"],
            "standards": [f"SZ.ENG.{item['grade']}.{item['id'][-1]}"]
        })

    # Add english inner-dependencies
    # sz_eng_3_1 (字母) -> sz_eng_3_2 (名词代词)
    # sz_eng_3_2 -> sz_eng_4_1 (复数)
    # sz_eng_4_1 -> sz_eng_5_1 (三单动词s变化相似规律)
    # sz_eng_5_1 -> sz_eng_5_2 (There be与主谓一致)
    # sz_eng_5_1 -> sz_eng_6_1 (过去时态对比)
    # sz_eng_6_1 -> sz_eng_6_2 (将来时态对比)
    eng_deps = [
        ("sz_eng_3_1", "sz_eng_3_2", "认识26个字母大小写是读写英文基本单词和代词的前提"),
        ("sz_eng_3_2", "sz_eng_4_1", "理解名词的单数概念是过渡到名词复数变化规则的前提"),
        ("sz_eng_4_1", "sz_eng_5_1", "名词复数加s/es的变形规律与第三人称单数动词加s/es的规则有高度相似性"),
        ("sz_eng_5_1", "sz_eng_5_2", "第三人称单数的主谓一致概念直接运用于 There be 句型中 is/are 的就近选择"),
        ("sz_eng_5_1", "sz_eng_6_1", "掌握一般现在时态是对比学习一般过去时态（时间线向后偏移）的基础"),
        ("sz_eng_6_1", "sz_eng_6_2", "掌握过去时态的表示有利于对比学习未来时态（be going to/will）")
    ]
    for src, tgt, reason in eng_deps:
        dependencies.append({
            "topicId": tgt,
            "prerequisiteId": src,
            "reason": reason
        })

    # ==========================================
    # SUBJECT: 科学 (苏教/教科版)
    # ==========================================
    sci_data = [
        {"grade": 1, "id": "sz_sci_1_1", "name": "身边的植物与动物", "domain": "生命科学", "desc": "观察校园和家周围的常见植物（如油菜花、柳树）和动物，学会描述它们的外形、叶片和活动特征。", "evidence": ["能说出柳树叶子像小船，银杏叶子像扇子", "能指出猫和狗身上的基本结构"], "prompt": "{{name}}，你在公园看到的小草和小花，它们有哪些地方长得一样？都有根和叶子吗？"},
        {"grade": 2, "id": "sz_sci_2_1", "name": "认识天气与四季变化", "domain": "地球与宇宙", "desc": "观察晴天、雨天、阴天、雪天等天气现象，记录并体会春夏秋冬四季交替对植物和人类生活的影响。", "evidence": ["在下雨天知道要带雨伞，天冷知道要加衣服", "能说出春天树木发芽，秋天树叶变黄落地"], "prompt": "{{name}}，现在是夏天，我们在夏天应该穿什么衣服？夏天有哪些水果成熟了？"},
        {"grade": 3, "id": "sz_sci_3_1", "name": "磁铁的奥秘", "domain": "物质科学", "desc": "认识磁铁的形状，探究磁铁可以吸引哪些铁制物体，理解磁铁有南极（S）和北极（N），掌握“同极相斥、异极相吸”的物理规律。", "evidence": ["能用磁铁准确找出硬币或曲别针", "能通过磁极靠近实验说出同名磁极会互相推开"], "prompt": "{{name}}，如果我拿两个磁铁的北极（N）靠近对方，它们会吸在一起还是弹开？"},
        {"grade": 4, "id": "sz_sci_4_1", "name": "声音的产生与传播", "domain": "物质科学", "desc": "通过实验探究声音是由物体振动产生的，理解声音可以通过固体、液体和气体传播，真空中无法传声。", "evidence": ["摸着说话时的声带能感受到震动", "知道敲击水杯时杯子振动产生声音"], "prompt": "{{name}}，你说话的时候用手摸脖子，手有什么感觉？如果不振动了，还能发出声音吗？"},
        {"grade": 5, "id": "sz_sci_5_1", "name": "光与折射现象", "domain": "物质科学", "desc": "理解光的直线传播，探索光照射在水、玻璃等介质中发生的折射现象，解释筷子在水中“折断”和彩虹成因。", "evidence": ["能做实验演示手电筒光束走直线", "能用折射现象解释装水水杯中筷子弯折的原理"], "prompt": "{{name}}，把一根直筷子斜插进水杯里，从旁边看筷子为什么好像折断了？这叫什么现象？"},
        {"grade": 6, "id": "sz_sci_6_1", "name": "太阳系与星空奥秘", "domain": "地球与宇宙", "desc": "认识以太阳为中心的八大行星分布，初步理解地球自转产生昼夜、公转产生四季，学会辨认北斗七星等四季星座。", "evidence": ["能按顺序说出水金地火木土天海八大行星", "能在夜晚天空中指出北斗七星的勺子形状"], "prompt": "{{name}}，地球绕太阳转一圈需要多长时间？这会产生什么变化？绕自己转一圈呢？"},
    ]

    for item in sci_data:
        topics.append({
            "id": item["id"],
            "type": "CONCEPTUAL",
            "subject": "科学",
            "domain": item["domain"],
            "name": item["name"],
            "description": item["desc"],
            "ageRangeStart": 5 + item["grade"],
            "ageRangeEnd": 6 + item["grade"],
            "centrality": 0.04 + (item["grade"] * 0.01),
            "evidence": item["evidence"],
            "assessmentPrompt": item["prompt"],
            "standards": [f"SZ.SCI.{item['grade']}.{item['id'][-1]}"]
        })

    # Add science dependencies
    # sz_sci_2_1 (天气四季) -> sz_sci_6_1 (自转公转)
    # sz_sci_4_1 (声音传播介质) -> sz_sci_5_1 (光的传播介质折射)
    sci_deps = [
        ("sz_sci_2_1", "sz_sci_6_1", "观察四季气候交替是进一步学习地球绕日公转天文学规律的认知前提"),
        ("sz_sci_4_1", "sz_sci_5_1", "波动在介质中的直线与折射传播与声音物理性质有认知相似性")
    ]
    for src, tgt, reason in sci_deps:
        dependencies.append({
            "topicId": tgt,
            "prerequisiteId": src,
            "reason": reason
        })

    # ==========================================
    # SUBJECT: 道德与法治（含中国历史与综合实践）
    # ==========================================
    mor_data = [
        # Grade 1-2
        {"grade": 1, "id": "sz_mor_1_1", "name": "我是小学生与安全生活", "domain": "个人成长", "desc": "适应小学的班级和作息，掌握校园课间安全、上下学交通规则，学会防拐骗和拨打紧急电话。", "evidence": ["知道上下学走斑马线，红灯停绿灯行", "背得出家长的电话，知道不吃陌生人的东西"], "prompt": "{{name}}，如果课间在走廊奔跑，会发生什么危险？迷路了应该找谁帮忙？"},
        {"grade": 2, "id": "sz_mor_2_1", "name": "神话传说与传统节日", "domain": "历史与民俗", "desc": "学习盘古开天、女娲补天等中华神话，了解端午、中秋、春节等传统节日的历史由来与苏州岁时习俗（吃冬至团等）。", "evidence": ["能讲出屈原和端午节包粽子的关联", "能说出冬至大如年，苏州吃冬至夜饭的习俗"], "prompt": "{{name}}，你知道端午节我们为什么要吃粽子、赛龙舟吗？这是为了纪念谁？"},
        
        # Grade 3-4
        {"grade": 3, "id": "sz_mor_3_1", "name": "中华文字与四大发明", "domain": "历史与科技", "desc": "了解甲骨文等古老汉字演变，知道造纸术、指南针、活字印刷术、火药这四大发明的发明者及其对世界文明的杰出贡献。", "evidence": ["能说出蔡伦改造了造纸术，毕昇发明了活字印刷", "能讲出指南针对航海的帮助"], "prompt": "{{name}}，在毕昇发明活字印刷术之前，古人是怎么印书的？为什么活字印刷方便得多？"},
        {"grade": 4, "id": "sz_mor_4_1", "name": "张骞西域与丝绸之路", "domain": "历史与地理", "desc": "学习张骞出使西域的历史故事，了解古代丝绸之路的路线，体会古代中国与世界各国的瓷器、茶叶、丝绸贸易交流。", "evidence": ["能在世界地图上指出中国丝绸运往欧洲的丝绸之路大概方向", "能讲出张骞“凿空”西域的勇敢精神"], "prompt": "{{name}}，两千年前的张骞去西域带回来了什么植物（如葡萄、石榴）？我们的丝绸是怎么运到罗马去的？"},
        
        # Grade 5-6
        {"grade": 5, "id": "sz_mor_5_1", "name": "秦皇汉武与大运河", "domain": "大一统与运河", "desc": "学习秦始皇统一中国度量衡与文字，了解隋唐大运河的修筑目的及其对江南地区（尤其是苏州平江府）商业繁荣的重要意义。", "evidence": ["能在运河地图上指出苏州是运河的重要枢纽节点", "知道度量衡统一对买卖东西的便利"], "prompt": "{{name}}，为什么大运河修通后，苏州的茶叶和丝绸更容易运到北方的京城去？"},
        {"grade": 6, "id": "sz_mor_6_1", "name": "近代救亡与新中国成立", "domain": "近现代史", "desc": "了解鸦片战争后中国的危机，知道孙中山与辛亥革命，学习抗日战争与红军长征精神，理解新中国成立的伟大历史转折。", "evidence": ["能讲出长征中“飞夺泸定桥”等英勇战斗故事", "知道10月1日是国庆节，代表新中国宣告成立"], "prompt": "{{name}}，我们在每年的10月1日庆祝国庆节，这是为了纪念什么历史时刻？"},
    ]

    for item in mor_data:
        topics.append({
            "id": item["id"],
            "type": "CONCEPTUAL",
            "subject": "道德与法治",
            "domain": item["domain"],
            "name": item["name"],
            "description": item["desc"],
            "ageRangeStart": 5 + item["grade"],
            "ageRangeEnd": 6 + item["grade"],
            "centrality": 0.03 + (item["grade"] * 0.01),
            "evidence": item["evidence"],
            "assessmentPrompt": item["prompt"],
            "standards": [f"SZ.MOR.{item['grade']}.{item['id'][-1]}"]
        })

    # Add morality dependencies
    # sz_mor_1_1 -> sz_mor_2_1
    # sz_mor_2_1 -> sz_mor_3_1 (传说故事过渡到文字四大发明历史)
    # sz_mor_3_1 -> sz_mor_4_1
    # sz_mor_4_1 -> sz_mor_5_1
    # sz_mor_5_1 -> sz_mor_6_1
    mor_deps = [
        ("sz_mor_1_1", "sz_mor_2_1", "生活安全规范意识是进一步开展传统节日习俗校外实践活动的前提"),
        ("sz_mor_2_1", "sz_mor_3_1", "从口头神话传说过渡到书面文字演变，理解人类文明的书写方式"),
        ("sz_mor_3_1", "sz_mor_4_1", "四大发明（指南针、造纸等）是古代丝绸之路长途贸易和商队交流的技术保障"),
        ("sz_mor_4_1", "sz_mor_5_1", "陆上丝绸之路向中原拓展的历史是隋唐修建南北大运河巩固大一统的政治背景"),
        ("sz_mor_5_1", "sz_mor_6_1", "理解古代帝制与统一王朝兴衰是进一步学习近代推翻帝制救亡图存历史的认知背景")
    ]
    for src, tgt, reason in mor_deps:
        dependencies.append({
            "topicId": tgt,
            "prerequisiteId": src,
            "reason": reason
        })

    # ==========================================
    # SUBJECT: 信息技术 (信息科技)
    # ==========================================
    inf_data = [
        {"grade": 3, "id": "sz_inf_3_1", "name": "计算机基本操作与打字", "domain": "软件操作", "desc": "学习电脑开关机、鼠标操作、文件夹管理，掌握键盘指法，利用拼音输入法进行中文盲打练习。", "evidence": ["写字板里能正确盲打出一句中文", "能自如用鼠标拖拽图标和创建文件夹"], "prompt": "{{name}}，手放在键盘上时，两个食指应该分别放在哪两个键上（基准键）？打字时应该怎么坐？"},
        {"grade": 4, "id": "sz_inf_4_1", "name": "Scratch 图形化编程初步", "domain": "编程与算法", "desc": "认识Scratch角色和舞台，掌握“当绿旗被点击”、“移动10步”、“右转15度”等核心积木，制作简单的角色动画。", "evidence": ["能拼出让小猫走正方形路线的积木组", "能自己运行绿旗并调试角色移动方向"], "prompt": "{{name}}，怎么用 Scratch 积木让一只猫向前走100步，然后大声说“你好！”？"},
        {"grade": 5, "id": "sz_inf_5_1", "name": "办公软件与电子板报", "domain": "软件操作", "desc": "掌握Word排版文字、插入图片、设置首行缩进，学会PPT幻灯片制作与动画效果，完成一份家园电子板报制作。", "evidence": ["能独立制作一张3页的假期旅游PPT并加入切换动画", "能用Word给自己的作文排版打印"], "prompt": "{{name}}，在Word里要写标题，怎么让标题在纸张正中间显示？"},
        {"grade": 6, "id": "sz_inf_6_1", "name": "网络安全与信息防护", "domain": "网络与社会", "desc": "认识互联网功能，建立防范网络谣言和不良信息的意识，掌握强密码设置规则及防范电脑病毒的安全守则。", "evidence": ["知道不点击垃圾邮件和中奖链接", "能为自己的学习账号设定包含大小写字母与数字的强密码"], "prompt": "{{name}}，为什么不能把自己的真实姓名、学校名字和家庭地址告诉网络游戏里的陌生人？"},
    ]

    for item in inf_data:
        topics.append({
            "id": item["id"],
            "type": "CONCEPTUAL",
            "subject": "信息技术",
            "domain": item["domain"],
            "name": item["name"],
            "description": item["desc"],
            "ageRangeStart": 5 + item["grade"],
            "ageRangeEnd": 6 + item["grade"],
            "centrality": 0.03 + (item["grade"] * 0.01),
            "evidence": item["evidence"],
            "assessmentPrompt": item["prompt"],
            "standards": [f"SZ.INF.{item['grade']}.{item['id'][-1]}"]
        })

    # Dependencies
    # sz_inf_3_1 -> sz_inf_4_1
    # sz_inf_3_1 -> sz_inf_5_1
    # sz_inf_5_1 -> sz_inf_6_1
    inf_deps = [
        ("sz_inf_3_1", "sz_inf_4_1", "掌握键盘输入和基本鼠标拖拽操作是拼装 Scratch 编程积木的代码基础"),
        ("sz_inf_3_1", "sz_inf_5_1", "熟练键盘指法打字是进行 Word 文档排版和 PPT 演示编辑的前提"),
        ("sz_inf_5_1", "sz_inf_6_1", "具备办公及文件保存技能后，进一步学习网络防毒和本地文件加密等信息安全常识")
    ]
    for src, tgt, reason in inf_deps:
        dependencies.append({
            "topicId": tgt,
            "prerequisiteId": src,
            "reason": reason
        })

    # ==========================================
    # SUBJECT: 生活技能 (劳动课)
    # ==========================================
    lab_data = [
        {"grade": 1, "id": "sz_lab_1_1", "name": "整理书包与红领巾佩戴", "domain": "自我服务", "desc": "学会每天对照课表分类收拾书本、文具，掌握少先队红领巾的规范佩戴与解开折叠方法。", "evidence": ["每天晚上能独立在5分钟内收拾好第二天要用的书包", "能熟练打红领巾的死结并摆正"], "prompt": "{{name}}，红领巾是怎么戴的？口诀是“折一折，翻一翻”吗？给妈妈演示一下？"},
        {"grade": 2, "id": "sz_lab_2_1", "name": "垃圾分类与收纳整理", "domain": "家庭劳动", "desc": "学习垃圾分类四分法（可回收物、有害垃圾、厨余垃圾、其他垃圾），独立整理自己的玩具箱和衣柜。", "evidence": ["扔垃圾时能自主把香蕉皮投进绿桶，废电池投进红桶", "能把折好的衣服整齐摆放在衣柜指定抽屉内"], "prompt": "{{name}}，吃剩的骨头和过期的药片，分别应该扔在哪个颜色的垃圾桶里？"},
        {"grade": 3, "id": "sz_lab_3_1", "name": "日常保洁与洗补衣服", "domain": "家庭劳动", "desc": "掌握扫地、拖地、擦桌子的劳动要领，学会独立手洗自己的红领巾、袜子，并学会使用洗衣机。", "evidence": ["能帮妈妈把客厅扫拖得干干净净", "能把脏袜子打上肥皂，搓洗干净并晾晒"], "prompt": "{{name}}，拖地的时候应该从房间的最里面往门口倒退着拖，还是往里走？为什么？"},
        {"grade": 4, "id": "sz_lab_4_1", "name": "基础烹饪与凉拌菜制作", "domain": "日常烹饪", "desc": "认识安全用火用电和厨房刀具，学会洗菜、切黄瓜，能独立制作凉拌西红柿或黄瓜等家常凉拌菜。", "evidence": ["做凉拌西红柿时知道加糖拌匀，刀法安全防切手指", "用完煤气阀知道彻底关紧"], "prompt": "{{name}}，我们做凉拌黄瓜要先洗净、拍碎、加蒜泥和醋，切黄瓜时手指要怎么呈猫爪状扣着？"},
        {"grade": 5, "id": "sz_lab_5_1", "name": "花卉养护与中药种植", "domain": "劳动种植", "desc": "学习花卉及阳台蔬菜的浇水、施肥、修剪规律，在花盆中种植薄荷或小香葱，观察并记录其成长周期。", "evidence": ["能独立管理阳台花草，定期浇水除草", "知道植物叶子发黄往往是浇水过多或缺肥"], "prompt": "{{name}}，我们种的薄荷大概多久需要浇一次水？水应该直接浇到叶子上还是土里？"},
        {"grade": 6, "id": "sz_lab_6_1", "name": "中餐烹饪（炒鸡蛋与煮面条）", "domain": "日常烹饪", "desc": "学会使用炒锅、燃气灶和电饭煲，独立完成炒鸡蛋（煎蛋）、煮挂面及淘米蒸米饭的日常中餐操作。", "evidence": ["能自己给自己下一碗卧鸡蛋面条并加葱花", "能炒出一盘松软好吃的西红柿炒鸡蛋，不烫伤自己"], "prompt": "{{name}}，今天中午妈妈不在家，你打算怎么给自己下一碗面？煮面的时候水开了要加几次冷水？"},
    ]

    for item in lab_data:
        topics.append({
            "id": item["id"],
            "type": "CONCEPTUAL",
            "subject": "生活技能",
            "domain": item["domain"],
            "name": item["name"],
            "description": item["desc"],
            "ageRangeStart": 5 + item["grade"],
            "ageRangeEnd": 6 + item["grade"],
            "centrality": 0.02 + (item["grade"] * 0.01),
            "evidence": item["evidence"],
            "assessmentPrompt": item["prompt"],
            "standards": [f"SZ.LAB.{item['grade']}.{item['id'][-1]}"]
        })

    # Dependencies
    lab_deps = [
        ("sz_lab_1_1", "sz_lab_2_1", "学会分类整理书包可顺利过渡到家庭大范围垃圾分类和物品收纳"),
        ("sz_lab_2_1", "sz_lab_3_1", "具备良好的物品收纳习惯后，进一步学习使用清洁工具进行日常地面和衣物保洁"),
        ("sz_lab_3_1", "sz_lab_4_1", "熟悉厨房及水电用具基本保洁后，进一步在安全刀法指引下学习凉拌菜制作"),
        ("sz_lab_4_1", "sz_lab_6_1", "掌握凉拌切菜等基本厨房安全后，进一步独立使用明火或电磁炉进行炒菜煮面条")
    ]
    for src, tgt, reason in lab_deps:
        dependencies.append({
            "topicId": tgt,
            "prerequisiteId": src,
            "reason": reason
        })

    # ==========================================
    # CROSS-SUBJECT DEPENDENCIES (自适应诊断关联)
    # ==========================================
    # Chinese reading helps reading Math word problems:
    # sz_chn_1_1 (拼音) -> sz_math_1_1 (20以内加减口头题读拼音)
    # sz_chn_4_2 (中心句/段落大意) -> sz_math_4_4 (解决问题的列表/画图策略，要求阅读理解)
    # sz_chn_6_1 (病句逻辑修改) -> sz_math_6_4 (比例正反比逻辑判断)
    # sz_math_2_1 (表内乘法) -> sz_inf_4_1 (Scratch 编程中循环走格子步数运算)
    cross_deps = [
        ("sz_chn_1_1", "sz_math_1_1", "能认读拼音帮助一年级孩子理解加减法应用题中的文字描述"),
        ("sz_chn_4_2", "sz_math_4_4", "能归纳段落大意和核心意图能辅助孩子提炼出复杂应用题中的主干数学数量关系"),
        ("sz_chn_6_1", "sz_math_6_4", "排查句子逻辑主干和病句改错能力有助于在比例应用题中判断正反比的函数逻辑对应关系"),
        ("sz_math_2_1", "sz_inf_4_1", "乘法累加思维直接支撑 Scratch 中循环计数与平移次数算法的设计")
    ]
    for src, tgt, reason in cross_deps:
        dependencies.append({
            "topicId": tgt,
            "prerequisiteId": src,
            "reason": reason
        })

    # ==========================================
    # OUTPUT JSON FILES
    # ==========================================
    topics_output = {
        "version": "1.0.0",
        "topicCount": len(topics),
        "topics": topics
    }
    
    deps_output = {
        "version": "1.0.0",
        "dependencyCount": len(dependencies),
        "dependencies": dependencies
    }
    
    # Save files
    with open("d:/antigravity/app/Taxonomy/data/topics_cn.json", "w", encoding="utf-8") as f:
        json.dump(topics_output, f, indent=2, ensure_ascii=False)
        
    with open("d:/antigravity/app/Taxonomy/data/dependencies_cn.json", "w", encoding="utf-8") as f:
        json.dump(deps_output, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(topics)} topics.")
    print(f"Generated {len(dependencies)} dependency relations.")
    print("Files successfully saved to data/topics_cn.json and data/dependencies_cn.json.")

if __name__ == "__main__":
    main()

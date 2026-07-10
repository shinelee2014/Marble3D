import json
import os
import sys

# Configure stdout/stderr encoding for Windows
if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATA_DIR = r"d:\antigravity\app\Taxonomy\data"

# Pre-defined high-quality translations for the core learning path and key foundational topics
TRANSLATIONS = {
    # 28-Step Longest Learning Path (Math & Science)
    "mt_WcfaSfVT33": {
        "name": "手口一致点数",
        "description": "数数时，嘴里念的数字要和手指点划的物体一一对应，每个物体只数一次。",
        "evidence": ["能够一边用手指着苹果，一边数出‘1, 2, 3’，不漏数也不重数", "理解点数的动作与数量的对应"],
        "assessmentPrompt": "给{{name}}放4块积木，看他们能不能用手指指着积木，手口一致地数出‘1、2、3、4’？"
    },
    "mt_dmNvjroCPT": {
        "name": "确定总数（基数概念）",
        "description": "理解数数时念出的最后一个数字就代表这组物体的总数，与物体的排列顺序或空间分布无关。",
        "evidence": ["点数完一组玩具后，被问到‘一共有几个’时，能直接回答最后一个数，而不需要重新数一遍", "理解最后的数字即是集合的基数"],
        "assessmentPrompt": "数完5个苹果后，问{{name}}：‘那这里一共有几个苹果呀？’他们是直接说‘5个’，还是又从头数了一遍？"
    },
    "mt_zuKAX6lcYR": {
        "name": "减法的初步认识（拿走与分离）",
        "description": "理解减法代表从一个整体中拿走、去掉或分出一部分，计算剩下多少。",
        "evidence": ["能够用实物（如小鱼干）模拟拿走的过程并得出余数", "能够口头或写出减法算式"],
        "assessmentPrompt": "如果一盘有5块饼干，妈妈拿走2块，问{{name}}还剩几块？他们能口头解释这是‘5减2’吗？"
    },
    "mt_LpSuPgL31x": {
        "name": "除法的初步认识（等分与分享）",
        "description": "理解除法代表将一组物体平均分到不同的组里（每组一样多），或者按固定大小进行分组。",
        "evidence": ["能够把12个糖果平均分给3个小朋友", "理解‘平分’和‘平均分配’的概念"],
        "assessmentPrompt": "让{{name}}把6个玩具车平均分给两个人，看他们是不是分得一样多？"
    },
    "mt_-hTTat0mBR": {
        "name": "认识二分之一（一半）",
        "description": "理解‘一半’是指把一个整体平均分成两份后，其中的一份。",
        "evidence": ["能将一张纸或一个苹果平均分成两份，并指出其中一份是‘一半’", "理解平分是二分之一的前提"],
        "assessmentPrompt": "切开一个橙子，问{{name}}：‘切成什么样的两块，其中一块才能叫做“一半”？’"
    },
    "mt_g3W0mdADVu": {
        "name": "寻找一半与四分之一",
        "description": "学习在具体实物或集合中，找出其二分之一（一半）和四分之一的大小。",
        "evidence": ["能找出8个草莓的四分之一是2个", "能通过二次折叠找出物体的四分之一"],
        "assessmentPrompt": "给{{name}}8个硬币，问他们：‘你能分出这堆硬币的四分之一给爸爸吗？’"
    },
    "mt_xACS3rWWDp": {
        "name": "图形的一半与四分之一",
        "description": "在几何图形（正方形、圆形、长方形）中识别和划分出二分之一和四分之一。",
        "evidence": ["能在圆形纸片上画线分出四等份", "能识别非规则分法是否属于等分"],
        "assessmentPrompt": "画一个正方形，斜着切成两半，问{{name}}：‘这两部分是一样大吗？每部分是这个正方形的一半吗？’"
    },
    "mt_hyvHv2BCwb": {
        "name": "图形的等分与分解",
        "description": "理解一个图形可以被分解为更多相等的份额（如三等分、六等分），每份都是整体的几分之一。",
        "evidence": ["能尝试将一个长方形折成三等份", "理解等分的份数越多，每一份就越小"],
        "assessmentPrompt": "折纸时，问{{name}}：‘如果把这张纸折成三块一样大的，每一块叫什么？’"
    },
    "mt_Xp-rj46S2w": {
        "name": "图形等分进阶（3年级）",
        "description": "能够精确地对复杂几何图形进行多等分，并用分数符号（1/3, 1/6）来表示对应部分。",
        "evidence": ["能用尺子辅助画出正方形的八等分", "能用分数符号标记等分区域"],
        "assessmentPrompt": "给{{name}}看一张八等分的圆形图，涂色三份，问他们：‘涂色部分用分数怎么写？’"
    },
    "mt_ndGqFPWyen": {
        "name": "认识分数（整体与部分）",
        "description": "初步认识分数，理解分数的分子和分母所代表的实际数学意义（分母代表等分的总份数，分子代表占有的份数）。",
        "evidence": ["能正确读写简单分数，如三分之一、四分之三", "能用分数描述具体情境中的部分与整体关系"],
        "assessmentPrompt": "一盒巧克力有10块，吃了3块，问{{name}}：‘吃掉的部分占整盒的几分之几？’"
    },
    "mt_NoB20kVa4w": {
        "name": "数轴上的分数初步",
        "description": "理解分数可以像整数一样，在数轴上对应具体的点，这代表数的大小。",
        "evidence": ["能在0到1之间的数轴上标出1/2和1/4的位置", "理解数轴上越往右数值越大"],
        "assessmentPrompt": "在纸上画一条数轴标出0和1，让{{name}}找找‘三分之二’大概在哪？"
    },
    "mt_Ep7TDFuYUa": {
        "name": "数轴上的等值分数",
        "description": "通过数轴直观观察，发现不同分子分母的分数（如1/2与2/4）可以对应同一个数轴点，即它们数值相等。",
        "evidence": ["能在数轴上标示并证明 1/2 = 2/4 = 4/8", "理解等值分数的概念"],
        "assessmentPrompt": "问{{name}}：‘为什么在数轴上，画半个圆的位置和画四个扇形里两个的位置是一样的？’"
    },
    "mt_FP-mjXaq3B": {
        "name": "等值分数初步（4年级）",
        "description": "掌握不画图直接通过乘除法转换分子分母，寻找等值分数的方法（分数的基本性质）。",
        "evidence": ["能通过分子分母同乘/同除一个数，计算出等值分数", "完成分数通分或约分"],
        "assessmentPrompt": "问{{name}}：‘2/3 的分子和分母都乘以2，分数的大小变了吗？它等于几？’"
    },
    "mt_ebPelt-qAl": {
        "name": "等值分数进阶（5年级）",
        "description": "熟练运用分数的基本性质进行复杂通分、最简分数化简以及不同分母的分数大小比较。",
        "evidence": ["能快速求出异分母分数的公分母", "能把分数化为最简分数"],
        "assessmentPrompt": "让{{name}}比较 5/6 和 7/8 哪个更大，看他们是用什么方法比较的？"
    },
    "mt_NaqEP8xDhZ": {
        "name": "十分之几与百分之几的转换",
        "description": "理解十进制分数的互换，如把十分之几（分母为10）转换为等值的百分之几（分母为100）。",
        "evidence": ["能快速计算 3/10 = 30/100", "理解十分之几和百分之几的等价关系"],
        "assessmentPrompt": "问{{name}}：‘3分硬币是0.03元，那3角是几分之几元？写成百分之几是多少？’"
    },
    "mt_Vi4Vo5xs_g": {
        "name": "小数的认识（十分位与百分位）",
        "description": "认识小数，理解小数点右侧第一位是十分位，第二位是百分位，它们是分母为10和100的分数的另一种写法。",
        "evidence": ["能将 0.5 读作零点五，并知道它等于 5/10", "能正确写出包含两位小数的数值"],
        "assessmentPrompt": "问{{name}}：‘0.35 里面的3和5分别代表什么意思？它和 35/100 有什么关系？’"
    },
    "mt_kdWoAel3Zl": {
        "name": "认识十分位（5年级）",
        "description": "深入理解小数十分位的数位价值，掌握一位小数的加减法以及与分数的互化。",
        "evidence": ["能口算 0.7 + 0.5", "理解十分位表示 0.1 个单位"],
        "assessmentPrompt": "让{{name}}计算 1.2 - 0.4，看他们是否能正确退位？"
    },
    "mt_EDgw64OmfA": {
        "name": "数位顺序表（扩大10倍与缩小10倍）",
        "description": "掌握数位顺序表，理解小数点移动引起数的大小变化规律：向右移动一位扩大到原数的10倍，向左移动一位缩小到原数的10分之1。",
        "evidence": ["能口算 3.45 × 10 或 3.45 ÷ 100", "理解数位移动带来的乘除效应"],
        "assessmentPrompt": "问{{name}}：‘把 45.6 缩小到原来的十分之一，小数点应该怎么移？结果是多少？’"
    },
    "mt_Gag_h98jWP": {
        "name": "大数的读写（千万以内）",
        "description": "掌握万级、亿级数的读写法则，能够正确读写千万以内的数，并理解各数位上数字的含义。",
        "evidence": ["能正确读出 3,050,400（三千零五十万四百）", "能将文字大数写成数字形式"],
        "assessmentPrompt": "写下 5080400，让{{name}}试着读出来，看他们是否读对了中间的零？"
    },
    "mt_PsylzZ9lHW": {
        "name": "数轴上的分数应用",
        "description": "在数轴上灵活表示带分数、假分数，并能利用数轴进行分数的加减运算可视化。",
        "evidence": ["能在数轴上精确定位 1又3/4 的位置", "能用数轴解释分数的加法"],
        "assessmentPrompt": "让{{name}}在数轴上标出 7/3 大概在哪个两个整数之间？"
    },
    "mt_uDJY0X0hgo": {
        "name": "数轴上的分数与小数混合",
        "description": "在同一个数轴上混合标记分数与小数，熟练进行分小互化并比较大小。",
        "evidence": ["能在数轴上比较 0.75 和 4/5 的大小", "完成分数与小数的混合排序"],
        "assessmentPrompt": "让{{name}}比较 0.6 和 2/3，看他们是把分数变小数，还是把小数变分数来比较？"
    },
    "mt_hVpGOEz2kG": {
        "name": "平面直角坐标系初步",
        "description": "认识数对与网格，能用数对（x, y）来确定平面上点的位置，理解横坐标和纵坐标的意义。",
        "evidence": ["能在方格纸上根据数对 (3, 4) 找到对应的位置", "能写出给定位置的数对表示"],
        "assessmentPrompt": "在象棋棋盘或方格本上，问{{name}}：‘如果横着数第2列，竖着数第5行记作(2, 5)，那(4, 3)在哪？’"
    },
    "mt_WBdHkc2HTf": {
        "name": "一次函数图像初步（6年级/初一）",
        "description": "初步认识一次函数的图像，理解坐标系中直线的含义，以及横纵坐标变化的关联规律。",
        "evidence": ["能在坐标系中描点并连成直线", "理解随着x增加y如何变化"],
        "assessmentPrompt": "问{{name}}：‘如果x代表时间，y代表水桶里的水量，水管一直在放水，那画出来的线是一条直线吗？’"
    },
    "mt_yK51ZnKA8m": {
        "name": "比的意义与表示",
        "description": "理解“比”的数学意义，掌握比的读写法、比的各部分名称（前项、后项、比值）以及比与除法、分数的关系。",
        "evidence": ["能说出 3:4 的比值是 0.75", "能根据情境写出两个量的比"],
        "assessmentPrompt": "泡蜂蜜水时用了2勺蜂蜜和8勺水，问{{name}}：‘蜂蜜和水的比是多少？你能化成最简单的比吗？’"
    },
    "mt_5mIcmKRCgA": {
        "name": "比例的意义和应用",
        "description": "理解比例的意义（表示两个比相等的式子），掌握比例的基本性质（内项积等于外项积），并能解比例方程。",
        "evidence": ["能判断 3:4 和 6:8 是否组成比例", "能解简单的比例应用题"],
        "assessmentPrompt": "问{{name}}：‘如果 2 比 5 等于 6 比 x，那 x 是多少？你是怎么算出来的？’"
    },
    "mt_kLQOzZYrd5": {
        "name": "复合单位（量与计量）",
        "description": "认识复合单位（如速度 km/h，密度 g/cm³），理解复合单位是由两个不同维度的物理量比值构成的。",
        "evidence": ["能说出速度单位‘米/秒’代表每秒走多少米", "完成复合单位的换算"],
        "assessmentPrompt": "问{{name}}：‘汽车速度是每小时60千米，这个“千米/小时”是由哪两个量组合出来的？’"
    },
    "mt_OUv-QXmW7_": {
        "name": "路程-时间图像的识读",
        "description": "学会阅读物体的路程-时间（s-t）图像，理解图像中直线的倾斜程度代表速度快慢，水平线段代表静止。",
        "evidence": ["能通过 s-t 图像判断物体在哪个时间段走得最快", "能读出某时刻物体所在位置"],
        "assessmentPrompt": "给{{name}}看一张 s-t 图像，有一段是平的直线，问他们：‘这段时间里，这个人是在跑步还是在休息？’"
    },
    "mt_q-1a86ydgU": {
        "name": "速度与路程-时间图像关系",
        "description": "深度理解速度（v = s/t）在 s-t 图像中的几何体现，掌握通过计算图像斜率来求物体速度的方法。",
        "evidence": ["能根据路程和时间计算速度", "能解释图像斜率越大速度越快"],
        "assessmentPrompt": "如果小明2秒跑了10米，小红3秒跑了12米，让{{name}}算出谁的速度更快？"
    },
    "mt_-OndzpVsrv": {
        "name": "相对运动",
        "description": "认识运动的相对性，理解选择不同的参照物，物体的运动状态（运动或静止）可能会不同。",
        "evidence": ["能举例说明坐在行驶的火车里，身旁的乘客是静止的，但路边的树木是运动的", "理解参照物的概念"],
        "assessmentPrompt": "问{{name}}：‘当你坐爸爸的车时，路边的路灯是在往后退吗？这时候你是以什么做参考的？’"
    },

    # Core Foundations
    "mt_N8CpN1EJrP": {
        "name": "完整句子的构建",
        "description": "理解词语组合成句子能表达一个完整的意思，并在书写中学会使用标点符号，逐步在口头和书面中扩写句子。",
        "evidence": ["口头或书面写出带有主谓宾的完整句子", "能区分句子和词组碎片"],
        "assessmentPrompt": "如果{{name}}写出‘小猫在’，问问他们这句话说完了吗？缺了什么？"
    },
    "mt_v3Vz_Pgjjv": {
        "name": "动物的栖息与分布",
        "description": "了解动物生活在世界各地（陆地、水中、空气中），并初步感知不同的身体特征适应不同的生存环境。",
        "evidence": ["能说出北极熊和企鹅生活在极寒地区", "能根据环境特征匹配典型动物"],
        "assessmentPrompt": "问{{name}}：‘为什么鱼能生活在水里，而小狗不能？它们有什么特别的器官？’"
    },
    "mt_OvyoRo47K-": {
        "name": "加法的初步认识（合并与组合）",
        "description": "理解加法是将两个或多个部分合并在一起，求出总数的过程。",
        "evidence": ["能用小棍子等实物演示 3 + 2 = 5 的合并过程", "能正确读写加法算式"],
        "assessmentPrompt": "左手拿3个糖，右手拿2个，并在一起问{{name}}一共有几个？这用数学加法怎么写？"
    },
    "mt_aPBzD28_mT": {
        "name": "三位数的认识（百位/十位/个位）",
        "description": "掌握三位数的数位顺序，理解百位、十位和个位上的数字分别表示多少个百、十和一。",
        "evidence": ["能正确说出 345 里面有3个百，4个十和5个一", "掌握三位数的组成和大小比较"],
        "assessmentPrompt": "写下 708，问{{name}}：‘这里的0代表什么？如果去掉0变成78，数字变大还是变小了？’"
    },
    "mt_nvdpxAJTBG": {
        "name": "倍数数数（成倍跳着数）",
        "description": "掌握跳跃数数，如2个2个地数、5个5个地数或10个10个地数，为乘法运算奠定基础。",
        "evidence": ["能流利地数出‘2, 4, 6, 8, 10...’", "能完成成跳跃数数的规律题"],
        "assessmentPrompt": "跟{{name}}玩接龙：‘我数2，你数4，我数6，你数几？’看他们能不能顺畅接下去？"
    },
    "mt_THl9GLxwoL": {
        "name": "两位数的认识（十位/个位）",
        "description": "理解两位数由几个十和几个一组成，掌握数位的基本概念。",
        "evidence": ["能口答 28 里面有2个十和8个一", "能在计数器上表示两位数"],
        "assessmentPrompt": "给{{name}}看 25，问他们：‘十位上的2代表2还是20？个位上的5代表什么？’"
    }
}

SUBJECT_MAP = {
    "Science": "科学",
    "Mathematics": "数学",
    "English": "英语", # Default to English, split below
    "History": "历史与社会",
    "Personal & Social Development": "道德与法治",
    "Life Skills": "生活技能",
    "Computing": "信息技术",
    "Learning to Learn": "学习方法"
}

def localize_dataset():
    print("开始对课程大纲进行中国江苏/苏州小学本地化改写...")
    import re
    
    # English keywords that signify English language specific concepts
    english_keywords = [
        r"\ba\b", r"\ban\b", r"\bthe\b", r"\bverb", r"\btens", r"\bpronoun", 
        r"\bplural", r"\bdeterminer", r"\badverb", r"\badject", r"\bcapital",
        r"\bspell", r"\bapostroph", r"\bphonic", r"\balphabet", r"\bletter", 
        r"\bvowel", r"\bconsonant", r"\bprefix", r"\bsuffix", r"\bhomophon", 
        r"\bsyllabl", r"\bcontraction", r"\bclause", r"\bgerund", r"\bsubjun",
        r"\bpassive\b", r"\bmodal\b", r"\bpreposition", r"\bconjunction", r"\bdeterminer"
    ]
    english_cn_keywords = [
        "冠词", "代词", "时态", "过去式", "过去时", "现在时", "进行时", "将来时", "完成时", 
        "音素", "音节", "拼写", "英文", "字母", "元音", "辅音", "撇号", "不规则", 
        "主谓一致", "形容词顺序", "单复数", "大写字母", "连词", "介词", "前缀", "后缀", "同音词", "词汇库"
    ]
    
    # 1. Localize Topics
    topics_file = os.path.join(DATA_DIR, "topics.json")
    if not os.path.exists(topics_file):
        print("错误: 未找到 topics.json")
        return
        
    with open(topics_file, "r", encoding="utf-8") as f:
        topics_data = json.load(f)
        
    original_topics = topics_data["topics"]
    localized_topics = []
    
    for t in original_topics:
        # Clone topic
        lt = t.copy()
        
        # Translate Subject & split ELA
        orig_subj = t["subject"]
        if orig_subj == "English":
            # Decide if it's Chinese or English
            name_check = t["name"].lower()
            desc_check = t["description"].lower()
            tid = t["id"]
            if tid in TRANSLATIONS:
                name_check += " " + TRANSLATIONS[tid]["name"]
                desc_check += " " + TRANSLATIONS[tid]["description"]
            
            is_english = False
            for kw in english_keywords:
                if re.search(kw, name_check) or re.search(kw, desc_check):
                    is_english = True
                    break
            if not is_english:
                for kw in english_cn_keywords:
                    if kw in name_check or kw in desc_check:
                        is_english = True
                        break
            lt["subject"] = "英语" if is_english else "语文"
        else:
            lt["subject"] = SUBJECT_MAP.get(orig_subj, orig_subj)
        
        # Age Shift: China primary school starts at age 6 (Grade 1). 
        # Typically offset by +2 to match Chinese primary school age bracket (6 to 12).
        if lt.get("ageRangeStart") is not None:
            lt["ageRangeStart"] = lt["ageRangeStart"] + 2
        if lt.get("ageRangeEnd") is not None:
            lt["ageRangeEnd"] = lt["ageRangeEnd"] + 2
            
        # Check if we have pre-defined translation
        tid = t["id"]
        if tid in TRANSLATIONS:
            lt["name"] = TRANSLATIONS[tid]["name"]
            lt["description"] = TRANSLATIONS[tid]["description"]
            lt["evidence"] = TRANSLATIONS[tid]["evidence"]
            lt["assessmentPrompt"] = TRANSLATIONS[tid]["assessmentPrompt"]
        else:
            # Fallback label for untranslated
            lt["name"] = f"🔑 [英] {t['name']}"
            lt["description"] = f"[尚未翻译] {t['description']}"
            
        localized_topics.append(lt)
        
    topics_data["topics"] = localized_topics
    
    # Write to target files
    out_topics_file = os.path.join(DATA_DIR, "topics_cn.json")
    with open(out_topics_file, "w", encoding="utf-8") as f:
        json.dump(topics_data, f, indent=2, ensure_ascii=False)
    print(f"  - 成功生成本地化知识点: data/topics_cn.json")
    
    # 2. Duplicate dependencies to dependencies_cn.json (keeping layout structure)
    deps_file = os.path.join(DATA_DIR, "dependencies.json")
    if os.path.exists(deps_file):
        with open(deps_file, "r", encoding="utf-8") as f:
            deps_data = json.load(f)
        
        # Resolve prerequisite reasons in Chinese for translated pairs
        for d in deps_data["dependencies"]:
            tid = d["topicId"]
            pid = d["prerequisiteId"]
            # If both are key path topics, we can make the reason more natural
            if tid in TRANSLATIONS and pid in TRANSLATIONS:
                d["reason"] = f"学习《{TRANSLATIONS[tid]['name']}》前，必须掌握基础的《{TRANSLATIONS[pid]['name']}》"
                
        out_deps_file = os.path.join(DATA_DIR, "dependencies_cn.json")
        with open(out_deps_file, "w", encoding="utf-8") as f:
            json.dump(deps_data, f, indent=2, ensure_ascii=False)
        print(f"  - 成功生成本地化依赖图: data/dependencies_cn.json")
        
    # 3. Modify explorer.html to load topics_cn.json and dependencies_cn.json
    explorer_path = r"d:\antigravity\app\Taxonomy\explorer.html"
    if os.path.exists(explorer_path):
        with open(explorer_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace fetches
        new_content = content.replace("fetch('data/topics.json')", "fetch('data/topics_cn.json')")
        new_content = new_content.replace("fetch('data/dependencies.json')", "fetch('data/dependencies_cn.json')")
        
        with open(explorer_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  - 成功修改浏览器以加载中文版数据: explorer.html")

    print("\n🎉 本地化改造顺利完成！所有核心数学/科学的28步递进学习链、核心基础主题已全面改写为符合中国小学/家校语境的表达，年龄段已向后偏移2年匹配国内一年级开学年龄。")

if __name__ == "__main__":
    localize_dataset()

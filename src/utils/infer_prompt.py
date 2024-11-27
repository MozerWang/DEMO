da_utt_zh_input = """对话历史:
{dialogue_history}

需要分析的对话:
{utterance}

基于对话历史，认真分析，按照输出格式给出“需要分析的对话”的意图、情感、情绪类型、立场、策略。

输出格式:
```json
{{
    "person": "参与者姓名",
    "content": "具体对话内容",
    "intent": "这句话的意图",
    "sentiment": "正向/负向/中性",
    "emotion": "愤怒/厌恶/恐惧/愉快/悲伤/蔑视/惊讶 等",
    "stance": [
        {{
            "aspect": "涉及的方面1/事件1",
            "viewpoint": "表达的观点/立场"
        }},
        ...
    ],
    "strategy": {{
        "description": "策略描述",
        "type": "策略引发的对话趋势变化（例如：引导对话、解决冲突、激化矛盾、改变观点等）"
    }}
}}
```
你的输出是："""




da_utt_en_input = """Dialogue history:
{dialogue_history}

Utterance to analyze:
{utterance}

Based on the dialogue history, carefully analyze and provide the intent, sentiment, emotion type, stance, and strategy of the "utterance to analyze" according to the output format.

Output format:
```json
{{
    "person": "Participant Name",
    "content": "Specific dialogue content",
    "intent": "Intent of this utterance",
    "sentiment": "Positive/Negative/Neutral",
    "emotion": "Anger/Contempt/Disgust/Enjoyment/Fear/Sadness/Surprise, etc.",
    "stance": [
        {{
            "aspect": "Aspect1/Event1 involved",
            "viewpoint": "Expressed viewpoint/stance"
        }},
        ...
    ],
    "strategy": {{
        "description": "Strategy description",
        "type": "Dialogue trend change caused by strategy (e.g., guiding the conversation, resolving conflict, intensifying conflict, changing viewpoints, etc.)"
    }}
}}
```
Your output is:"""



# ===========================================================================
# ===========================================================================
# ===========================================================================
da_persona_zh_input = """对话历史:
{dialogue_history}

这是一整段完整对话，你需要分析理解这段话对话,按照输出格式分析对话中的人物。

输出格式:
```json
{{
    "persona": {{
        "participant1": {{
            "name": "参与者1的姓名",
            "gender": "男/女/未知",
            "age": "童年期：6～11岁/少年期：12～15岁/青年期：15～24岁/成年期／壮年期：25～40岁/中年期：40～60岁/老年期：60岁以后/高龄期：70岁以后",
            "big_five": [
                [
                    "开放性",
                    "高"或"低"
                ],
                [
                    "尽责性",
                    "高"或"低"
                ],
                [
                    "外向性",
                    "高"或"低"
                ],
                [
                    "谦逊性",
                    "高"或"低"
                ],
                [
                    "神经质",
                    "高"或"低"
                ]
            ],
            "education": "教育背景描述",
            "occupation": "职业描述",
            "culture": "文化背景描述",
            "speaking_style": "说话风格和语言习惯描述",
            "hobby": "爱好描述",
        }},
        "participant2":{{
            "name": "参与者2的姓名",
            ...(同上)
        }}
    }}
}}
```
你的输出是："""


da_persona_en_input = """Dialogue history:
{dialogue_history}

This is a complete dialogue. You need to analyze and understand this conversation, and then deduce information about the PERSONA following the specified output format.

Output format:
```json
{{
    "persona": {{
        "participant1": {{
            "name": "Name of participant 1",
            "gender": "M/F/Unknown",
            "age": "Childhood: 6-11 years old / Adolescence: 12-15 years old / Youth: 15-24 years old / Adulthood: 25-40 years old / Middle age: 40-60 years old / Old age: 60 years and above / Advanced age: 70 years and above",
            "big_five": [
                [
                    "Openness",
                    "High" or "Low"
                ],
                [
                    "Conscientiousness",
                    "High" or "Low"
                ],
                [
                    "Extraversion",
                    "High" or "Low"
                ],
                [
                    "Agreeableness",
                    "High" or "Low"
                ],
                [
                    "Neuroticism",
                    "High" or "Low"
                ]
            ],
            "education": "Education description",
            "occupation": "Occupation description",
            "culture": "Cultural background of the person",
            "speaking_style": "Speaking style and language habits"
            "hobby": "Hobby description",
        }},
        "participant2": {{
            "name": "Name of participant 2",
            ...(Same as above)
        }}
    }}
}}
```
Your output is:"""

da_scene_zh_input = """对话历史:
{dialogue_history}

这是一整段完整对话，你需要分析理解这段话对话,按照输出格式分析对话中的情景。

输出格式:
```json
{{
    "scene": {{
        "topic": "对话话题",
        "relationship": "对话参与者之间的关系",
        "familiarity": "0-10的整数 (对话参与者之间的熟悉程度。0: 陌生人; 1: 初次见面; 2: 听说过对方但不认识; 4: 多次见面，略微熟悉; 6: 知道并熟悉对方的背景信息; 8: 在一起生活，了解彼此; 10: 关系亲密，在一起多年，非常熟悉彼此的习惯、秘密和脾气)",
        "talkway": "对话方式(直接交谈，电话，视频通话，即时消息，电子邮件，社交媒体，书信等)",
        "workflow": [
            "步骤1", 
            "步骤2", 
            ...(表示整场对话对话的工作流，指的是对话过程中双方信息交换的结构或者顺序，是一种步骤，比如参与者1先做了什么，参与者2做了什么，...，上述步骤并不是与每一句话一一对应的，是对整场对话的信息交换，偏向总结性质)
        ],
        "summary": [
            "参与者1对话总结", 
            "参与者2对话总结"
        ]
    }}
}}
```
你的输出是："""


da_scene_en_input = """Dialogue history:
{dialogue_history}

This is a complete dialogue. You need to analyze and understand this conversation, and then deduce information about the SCENE following the specified output format.

Output format:
```json
{{
    "scene": {{
        "topic": "Dialogue topic",
        "relationship": "Relationship between dialogue participants",
        "familiarity": "An integer from 0-10 (Degree of familiarity between dialogue participants. 0: Strangers; 1: Meet for the first time; 2: Heard of each other but don't know each other; 4: Met multiple times, slightly familiar; 6: Know and are familiar with each other's background information; 8: Stay together and are familiar with each other; 10: Close relationship, stay together for many years, are very familiar with each other's habits, secrets, and temper)",
        "talkway": "Dialogue mode (face-to-face conversation, phone call, video call, instant messaging, email, social media, letter, etc.)",
        "workflow": [
            "Step 1", 
            "Step 2", 
            ...(represents the workflow of the entire dialogue, referring to the structure or sequence of information exchange during the dialogue. It is a series of steps, such as what participant 1 did first, what participant 2 did, etc. These steps do not correspond to each sentence and are more of a summary of the information exchange throughout the dialogue.)
        ],
        "summary": [
            "Participant 1 dialogue summary", 
            "Participant 2 dialogue summary"
        ]
    }}
}}
```
Your output is:"""



da_goal_zh_input = """对话历史:
{dialogue_history}

这是一整段完整对话，你需要分析理解这段话对话,按照输出格式分析对话中的目标。

输出格式:
```json
{{
    "goal": {{
        "goal1": "参与者1的对话目标",
        "goal2": "参与者2的对话目标",
        "goal_completion": "0-10的整数 (全面分析对话者在多大程度上实现了各自的目标。0代表目标实现程度最低,10代表双方目标完全实现。)",
        "reason": "目标完成度打分的详细原因"
    }}
}}
```
你的输出是："""


da_goal_en_input = """Dialogue history:
{dialogue_history}

This is a complete dialogue. You need to analyze and understand this conversation, and then deduce information about the GOAL following the specified output format.

Output format:
```json
{{
    "goal": {{
        "goal1": "Dialogue goal of participant 1",
        "goal2": "Dialogue goal of participant 2",
        "goal_completion": "An integer from 0-10 (Comprehensively analyze to what extent the participants achieved their respective goals. 0 represents the lowest degree of goal achievement, 10 represents complete achievement of both parties' goals.)",
        "reason": "Detailed reasons for the goal completion score"
    }}
}}
```
Your output is:"""



# ===========================================================================
# ===========================================================================
# ===========================================================================
dg_sft_zh_input = """你需要根据提供的对话背景信息，对话历史和对话目标，生成合理的对话内容。

[对话背景信息]
时间：{dialogue[combine][time]}
对话方式：{dialogue[combine][talkway]}
参与者：{dialogue[person1][name]} 和 {dialogue[person2][name]}
两参与者所处的地点和环境：{dialogue[combine][location]}

{p1_name}的信息：{p1_bg}
{p2_name}的信息：{p2_bg}

对话双方的人物关系：{dialogue[combine][relationship]}
对话双方熟悉程度：{dialogue[combine][familiarity]} (0-10的数值, 越接近10越熟悉)
对话话题：{dialogue[topic]}

[对话历史]
{dialogue_history}

[对话目标]
你是{p1_name}，你的目标是：{p1_goal}。
另外一个对话参与者是{p2_name}，对方的目标是未知，你需要猜测和感知对方的对话目标。

你需要写出Turn #{turn}的回复，你可以选择"继续对话"和"结束对话"两种行为。
注意：如果出现以下情况，你可以"结束对话"：1. 你已实现对话目标；2.双方对话已结束；

["继续对话"输出格式]
```json
{{
    "person": "参与者姓名",
    "intent": "这句话的意图",
    "sentiment": "正向/负向/中性",
    "emotion": "愤怒/厌恶/恐惧/愉快/悲伤/蔑视/惊讶 等",
    "stance": [
        {{
            "aspect": "涉及的方面1/事件1",
            "viewpoint": "表达的观点/立场"
        }},
        ...
    ],
    "strategy": {{
        "description": "策略描述",
        "type": "策略引发的对话趋势变化（例如：引导对话、解决冲突、激化矛盾、改变观点等）"
    }}
    "content": "具体对话内容"
}}
```

["结束对话"输出格式]
```json
{{
    "person": "参与者姓名",
    "content": "*ENDING*"
}}
```
你的输出是："""




dg_sft_en_input = """You need to generate reasonable dialogue content based on the provided dialogue background information, dialogue history, and dialogue goal.

[Dialogue Background Information]
Time: {dialogue[combine][time]}
Dialogue Mode: {dialogue[combine][talkway]}
Participants: {dialogue[person1][name]} and {dialogue[person2][name]}
Location and environment of participants: {dialogue[combine][location]} 

Information about {p1_name}: {p1_bg}
Information about {p2_name}: {p2_bg}

Relationship between the dialogue participants: {dialogue[combine][relationship]}
Familiarity level between the dialogue participants: {dialogue[combine][familiarity]} (A value from 0-10, with 10 indicating the highest familiarity)
Dialogue Topic: {dialogue[topic]}

[Dialogue History]
{dialogue_history}

[Dialogue Goal]
You are {p1_name}, your goal is: {p1_goal}. 
The other dialogue participant is {p2_name}. The other party’s goal is unknown, and you need to guess and perceive the other person's dialogue goal.

You need to write the response for Turn #{turn}. You can choose between "Continue the dialogue" and "End the dialogue".
Note: You can "End the dialogue" if: 1. You have achieved the conversation goal; 2. The conversation between the two parties has ended;

["Continue the dialogue" Output Format]
```json
{{
    "person": "Participant Name",
    "intent": "Intent of this utterance",
    "sentiment": "Positive/Negative/Neutral",
    "emotion": "Anger/Contempt/Disgust/Enjoyment/Fear/Sadness/Surprise, etc.",
    "stance": [
        {{
            "aspect": "Aspect1/Event1 involved",
            "viewpoint": "Expressed viewpoint/stance"
        }},
        ...
    ],
    "strategy": {{
        "description": "Strategy description",
        "type": "Dialogue trend change caused by strategy (e.g., guiding the conversation, resolving conflict, intensifying conflict, changing viewpoints, etc.)"
    }}
    "content": "Specific dialogue content"
}}
```

["End the dialogue" Output Format]
```json
{{
    "person": "Participant Name",
    "content": "*ENDING*"
}}
```
Your output is:"""

# ===========================================================================
# ===========================================================================
# ===========================================================================
dg_test_zh_input = """你需要根据提供的对话背景信息，对话历史和对话目标，生成合理的对话内容。

[对话背景信息]
时间：{dialogue[combine][time]}
对话方式：{dialogue[combine][talkway]}
参与者：{dialogue[person1][name]} 和 {dialogue[person2][name]}
两参与者所处的地点和环境：{dialogue[combine][location]}

{p1_name}的信息：{p1_bg}
{p2_name}的信息：{p2_bg}

对话双方的人物关系：{dialogue[combine][relationship]}
对话双方熟悉程度：{dialogue[combine][familiarity]} (0-10的数值, 越接近10越熟悉)
对话话题：{dialogue[topic]}

[对话历史]
{dialogue_history}

[对话目标]
你是{p1_name}，你的目标是：{p1_goal}。
另外一个对话参与者是{p2_name}，对方的目标是未知，你需要猜测和感知对方的对话目标。

你需要写出Turn #{turn}的回复，你可以选择"继续对话"和"结束对话"两种行为。
注意：如果出现以下情况，你可以"结束对话"：1. 你已实现对话目标；2.双方对话已结束；

["继续对话"输出格式]
```json
{{
    "person": "参与者姓名",
    "content": "具体对话内容"
}}
```

["结束对话"输出格式]
```json
{{
    "person": "参与者姓名",
    "content": "*ENDING*"
}}
```
你的输出是："""




dg_test_en_input = """You need to generate reasonable dialogue content based on the provided dialogue background information, dialogue history, and dialogue goal.

[Dialogue Background Information]
Time: {dialogue[combine][time]}
Dialogue Mode: {dialogue[combine][talkway]}
Participants: {dialogue[person1][name]} and {dialogue[person2][name]}
Location and environment of participants: {dialogue[combine][location]} 

Information about {p1_name}: {p1_bg}
Information about {p2_name}: {p2_bg}

Relationship between the dialogue participants: {dialogue[combine][relationship]}
Familiarity level between the dialogue participants: {dialogue[combine][familiarity]} (A value from 0-10, with 10 indicating the highest familiarity)
Dialogue Topic: {dialogue[topic]}

[Dialogue History]
{dialogue_history}

[Dialogue Goal]
You are {p1_name}, your goal is: {p1_goal}. 
The other dialogue participant is {p2_name}. The other party’s goal is unknown, and you need to guess and perceive the other person's dialogue goal.

You need to write the response for Turn #{turn}. You can choose between "Continue the dialogue" and "End the dialogue".
Note: You can "End the dialogue" if: 1. You have achieved the conversation goal; 2. The conversation between the two parties has ended;

["Continue the dialogue" Output Format]
```json
{{
    "person": "Participant Name",
    "content": "Specific dialogue content"
}}
```

["End the dialogue" Output Format]
```json
{{
    "person": "Participant Name",
    "content": "*ENDING*"
}}
```
Your output is:"""


Familiar_map = {
    "0": ["0: 陌生人", "0: Strangers"],
    "1": ["1: 初次见面", "1: Meet for the first time"],
    "2": ["2: 听说过对方但不认识", "2: Heard of each other but don't know each other"],
    "4": ["4: 多次见面，略微熟悉", "4: Met multiple times, slightly familiar"],
    "6": ["6: 知道并熟悉对方的背景信息", "6: Know and are familiar with each other's background information"],
    "8": ["8: 在一起生活，了解彼此", "8: Stay together and are familiar with each other"],
    "10": ["10: 关系亲密，在一起生活多年，非常熟悉彼此的习惯、秘密和脾气", "10: Close relationship, stay together for many years, are very familiar with each other's habits, secrets, and temper"]
}

eval_scene = """You are an impartial and harsh judge evaluating conversation quality. Your task is to rigorously and meticulously assess the performance of the AI assistant in Dialogue Analysis (Scene) strictly based on specific criteria.

[Criteria]
    - Accuracy: To what extent is the assistant's answer semantically consistent with the gold standard.
    - Hallucination: There should be no hallucinations and friction. The assistant should not introduce any information not present in or not implied by the gold answer.

[Gold Answer]
{answer}

[The Assistant's Predicted Answer]
{prediction}

[Requirement]
1. The assistant receives an overall score on a scale of 0 to 10, where a higher score indicates better overall performance. Please note that if the assistant's answer fully meet the above criteria, its overall rating should be the full marks (10). Please note that the gold answer can be considered as a correct answer to the instruction.
2. Analyze how well the Assistant's performance meets each criterion.
3. Please first provide a comprehensive explanation of your evaluation, avoiding any potential bias. Then, output a line indicating the score of the Assistant.
4. Please note that the scoring for each criteria is independent and should not be influenced by each other.

[Output Format]
```json
{{
    "Accuracy":
        {{
            "reason": <reason for accuracy score>,
            "score": <0-10>
        }}, 
    "Hallucination": 
        {{
            "reason": "<reason for hallucination score>", 
            "score": <0-10> 
        }}
}}
```
Now, start your evaluation:"""





eval_goal = """You are an impartial and harsh judge evaluating conversation quality. Your task is to rigorously and meticulously assess the performance of the AI assistant in Dialogue Analysis (Goal) strictly based on specific criteria.

[Criteria]
    - Accuracy: To what extent is the assistant's answer semantically consistent with the gold standard?
    - Hallucination: There should be no hallucinations and friction. The assistant should not introduce any information not present in or not implied by the gold answer.

[Gold Answer]
{answer}

[The Assistant's Predicted Answer]
{prediction}

[Requirement]
1. The assistant receives an overall score on a scale of 0 to 10, where a higher score indicates better overall performance. Please note that if the assistant's answer fully meet the above criteria, its overall rating should be the full marks (10). Please note that the gold answer can be considered as a correct answer to the instruction.
2. Analyze how well the Assistant's performance meets each criterion.
3. Please first provide a comprehensive explanation of your evaluation, avoiding any potential bias. Then, output a line indicating the score of the Assistant.
4. Please note that the scoring for each criteria is independent and should not be influenced by each other.

[Output Format]
```json
{{
    "Accuracy":
        {{
            "reason": <reason for accuracy score>,
            "score": <0-10>
        }}, 
    "Hallucination": 
        {{
            "reason": "<reason for hallucination score>", 
            "score": <0-10> 
        }}   
}}
```
Now, start your evaluation:"""




eval_utterance = """You are an impartial and harsh judge evaluating conversation quality. Your task is to rigorously and meticulously assess the performance of the AI assistant in Dialogue Analysis (Utterance) strictly based on specific criteria.

[Criteria]
    - Accuracy: To what extent is the assistant's answer semantically consistent with the gold standard?
    - Hallucination: There should be no hallucinations and friction. The assistant should not introduce any information not present in or not implied by the gold answer.

[Gold Answer]
{answer}

[The Assistant's Predicted Answer]
{prediction}

[Requirement]
1. The assistant receives an overall score on a scale of 0 to 10, where a higher score indicates better overall performance. Please note that if the assistant's answer fully meet the above criteria, its overall rating should be the full marks (10). Please note that the gold answer can be considered as a correct answer to the instruction.
2. Analyze how well the Assistant's performance meets each criterion.
3. Please first provide a comprehensive explanation of your evaluation, avoiding any potential bias. Then, output a line indicating the score of the Assistant.
4. Please note that the scoring for each criteria is independent and should not be influenced by each other.

[Output Format]
```json
{{
    "Accuracy":
        {{
            "reason": <reason for accuracy score>,
            "score": <0-10>
        }},
    "Hallucination": 
        {{
            "reason": "<reason for hallucination score>", 
            "score": <0-10> 
        }}   
}}
```
Now, start your evaluation:"""




eval_persona = """You are an impartial and harsh judge evaluating conversation quality. Your task is to rigorously and meticulously assess the performance of the AI assistant in Dialogue Analysis (Persona) strictly based on specific criteria.

[Criteria]
    - Accuracy: To what extent is the assistant's answer semantically consistent with the gold standard?
    - Hallucination: There should be no hallucinations and friction. The assistant should not introduce any information not present in or not implied by the gold answer.

[Dialogue Analysis Instruction]
{instruction}

[Gold Answer]
{answer}

[The Assistant's Predicted Answer]
{prediction}

[Requirement]
1. The assistant receives an overall score on a scale of 0 to 10, where a higher score indicates better overall performance. Please note that if the assistant's answer fully meet the above criteria, its overall rating should be the full marks (10). Please note that the gold answer can be considered as a correct answer to the instruction.
2. Analyze how well the Assistant's performance meets each criterion.
3. Please first provide a comprehensive explanation of your evaluation, avoiding any potential bias. Then, output a line indicating the score of the Assistant.
4. Please note that the scoring for each criteria is independent and should not be influenced by each other.

[Output Format]
```json
{{
    "Accuracy":
        {{
            "reason": <reason for accuracy score>,
            "score": <0-10>
        }}, 
    "Hallucination": 
        {{
            "reason": "<reason for hallucination score>", 
            "score": <0-10> 
        }}
}}
```
Now, start your evaluation:"""




eval_dg = """You are an impartial and harsh judge evaluating conversation quality. Your task is to rigorously and meticulously assess the following dialogue based on specific criteria.

[Criteria]
1. goal achievement (0-10):
    - How well the dialogue participants achieve their goals.
    - Identify each participant's goals from the provided background information. Analyze the progress made towards these goals throughout the conversation. 0 points: Neither participant makes any progress towards their goals. 10 points: Complete success; both participants fully achieve all their goals
    
2. believability (0-10):
    - What the extent to which the dialogue participants understand and align with Background Information. How well these elements are reflected in their expressions.
    - Two Participants should correctly understand the backgrpund information and perceive goals, and all the responses should not conflict with these elements. For example: speaking style must not conflict with the character portrait, the content of the response must not conflict with the background information, and the content of the response must not conflict with the respective goals. 0 points: Significant inconsistencies or misunderstandings of background information; Scene, Persona, and Goals cannot be inferred from the dialogue content. 10 points: Perfect alignment with all background elements, demonstrating a thorough understanding of the conversation's context; Background information can be fully deduced from the dialogue content.

3. skillful (0-10):
    - To what extent can the participants think and generate appropriate responses based on the conversation history.
    - The participants in the conversation should correctly understand the dialogue history before responding, and then think about the intention, sentiment, emotion, stance, and strategy to be expressed, so as to generate appropriate responses. 0 points: Poor understanding of dialogue history; responses are often inappropriate and lack strategy. 10 points: All responses can fully utilize the conversation strategy, understand the intentions of both parties, and conform to the conversation history.
    
4. realistic (0-10):
    - Evaluate how realistic the conversation is, as opposed to being simulated, fictitious or implausible.
    - The dialogue should feel natural and human-like, mirroring real-life interactions. AI-generated conversations often exhibit certain telltale signs: Excessive politeness or formality, overly detailed or lengthy responses, lack of emotional expression, difficulty with implicit meanings, repetitive phrasing or response patterns, poor conversational flow or awkward transitions. 0 points: Conversation is clearly AI-generated. 5 points: Mix of realistic and artificial elements. 10 points: Entirely believable as a conversation between two real people.

[Background Information]
Time: {result[time]}
Location and environment: {result[location]}
Dialogue Medium: {result[talkway]}
Dialogue Topic: {result[topic]}
Participants: {result[person1]} and {result[person2]}
Relationship between the dialogue participants: {result[relationship]}
Familiarity level between the dialogue participants: {result[familiarity]}

Information about {result[person1]}: {result[person1_bg]}
Information about {result[person2]}: {result[person2_bg]}

[Dialogue Goal]
Goal of {result[person1]}: {result[goal1]}
Goal of {result[person2]}: {result[goal2]}

[Dialogue Content]
{result[dialogue]}

[Requirement]
1. Reiterate the dialogue content and background information.
2. Analyze how well the dialogue meets each criterion.
3. Provide scores and reasons in JSON format as specified below.
4. Please note that the scoring for each criteria is independent and should not be influenced by each other.

[Output Format]
```json
{{
    "goal achievement":
        {{
            "reason": <reason for goal achievement score>,
            "score": <0-10>
        }}, 
    "believability": 
        {{ 
            "reason": "<reason for believability score>", 
            "score": <0-10> 
        }}, 
    "skillful": 
        {{ 
            "reason": "<reason for skillful score>", 
            "score": <0-10>
        }}, 
    "realistic": 
        {{
            "reason": "<reason for realistic score>", 
            "score": <0-10> 
        }}
}}
```
Now, start your evaluation:"""

Familiar_map = {
    "0": ["0: 陌生人", "0: Strangers"],
    "1": ["1: 初次见面", "1: Meet for the first time"],
    "2": ["2: 听说过对方但不认识", "2: Heard of each other but don't know each other"],
    "4": ["4: 多次见面，略微熟悉", "4: Met multiple times, slightly familiar"],
    "6": ["6: 知道并熟悉对方的背景信息", "6: Know and are familiar with each other's background information"],
    "8": ["8: 在一起生活，了解彼此", "8: Stay together and are familiar with each other"],
    "10": ["10: 关系亲密，在一起生活多年，非常熟悉彼此的习惯、秘密和脾气", "10: Close relationship, stay together for many years, are very familiar with each other's habits, secrets, and temper"]
}

BENCH_DIR="data"
CONFIG_PATH="config/qwen2_7b.yaml"
EVAL_CONFIG_PATH="config/gpt_4o.yaml"
OUTPUT_DIR="output/qwen2_7b"
OUTPUT_PATH="result"
RESULT_DIR="result/output/qwen2_7b"
EVAL_DIR="eval/qwen2_7b"
MODEL_PROCESS_NUM=50
GPT_PROCESS_NUM=30
PORT=8000

# Step 1: Inference for dialogue_agent_interaction_en
python step1_infer.py \
--bench_path "$BENCH_DIR/dialogue_agent_interaction_en.jsonl" \
--config_path "$CONFIG_PATH" \
--data "$OUTPUT_DIR" \
--output_path "$OUTPUT_PATH" \
--output_file "cg_en_infer.jsonl" \
--temperature 1.0 \
--port $PORT \
--process_num $MODEL_PROCESS_NUM \
--api \
--dg \
--en

# Step 1: Inference for dialogue_agent_interaction_zh
python step1_infer.py \
--bench_path "$BENCH_DIR/dialogue_agent_interaction_zh.jsonl" \
--config_path "$CONFIG_PATH" \
--data "$OUTPUT_DIR" \
--output_path "$OUTPUT_PATH" \
--output_file "cg_zh_infer.jsonl" \
--process_num $MODEL_PROCESS_NUM \
--temperature 1.0 \
--api \
--dg \
--port $PORT


# Step 1: Inference for element_awareness_en
python step1_infer.py \
--bench_path "$BENCH_DIR/element_awareness_en.json" \
--config_path "$CONFIG_PATH" \
--data "$OUTPUT_DIR" \
--output_path "$OUTPUT_PATH" \
--output_file "ca_en_infer.jsonl" \
--temperature 0.0 \
--port $PORT \
--process_num $MODEL_PROCESS_NUM \
--api \
--en

# Step 1: Inference for element_awareness_zh
python step1_infer.py \
--bench_path "$BENCH_DIR/element_awareness_zh.json" \
--config_path "$CONFIG_PATH" \
--data "$OUTPUT_DIR" \
--output_path "$OUTPUT_PATH" \
--output_file "ca_zh_infer.jsonl" \
--temperature 0.0 \
--process_num $MODEL_PROCESS_NUM \
--api \
--port $PORT

# # # # #Step 2: Evaluation for Dialogue English
python step2_eval.py \
--result_path "$RESULT_DIR/cg_en_infer.jsonl" \
--config_path $EVAL_CONFIG_PATH \
--output_path "$OUTPUT_PATH" \
--data "$EVAL_DIR" \
--output_file "cg_en_eval.jsonl" \
--process_num $GPT_PROCESS_NUM \
--dg \
--en

# # # # Step 2: Evaluation for Dialogue Chinese
python step2_eval.py \
--result_path "$RESULT_DIR/cg_zh_infer.jsonl" \
--config_path $EVAL_CONFIG_PATH \
--output_path "$OUTPUT_PATH" \
--data "$EVAL_DIR" \
--output_file "cg_zh_eval.jsonl" \
--process_num $GPT_PROCESS_NUM \
--dg

# # # #Step 2: Evaluation for CA Format English
python step2_eval.py \
--result_path "$RESULT_DIR/ca_en_infer.jsonl" \
--config_path $EVAL_CONFIG_PATH \
--output_path "$OUTPUT_PATH" \
--data "$EVAL_DIR" \
--output_file "ca_en_eval.jsonl" \
--process_num $GPT_PROCESS_NUM \
--en

# # # #Step 2: Evaluation for CA Format Chinese
python step2_eval.py \
--result_path "$RESULT_DIR/ca_zh_infer.jsonl" \
--config_path $EVAL_CONFIG_PATH \
--output_path "$OUTPUT_PATH" \
--data "$EVAL_DIR" \
--output_file "ca_zh_eval.jsonl" \
--process_num $GPT_PROCESS_NUM

# Step3: Calculate the Result
python step3_result.py \
--result_path "$OUTPUT_PATH/$EVAL_DIR" \


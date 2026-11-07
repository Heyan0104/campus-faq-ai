
import json
import math
from pathlib import Path
import ollama

# 使用已下載的 AI 模型
MODEL = "qwen3-embedding:0.6b"

# 讀取 FAQ 資料
faq_path = Path(__file__).parent / "faq.json"

with open(faq_path, "r", encoding="utf-8") as file:
    faq_data = json.load(file)


# 計算兩個語意向量的相似度
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0

    return dot / (norm_a * norm_b)


# 將標準問題與其他常見問法轉成向量
def prepare_faq():
    search_items = []

    for faq in faq_data:
        questions = [faq["question"]]
        questions += faq.get("alternative_questions", [])

        for question in questions:
            search_items.append((question, faq))

    response = ollama.embed(
        model=MODEL,
        input=[item[0] for item in search_items]
    )

    return list(zip(response["embeddings"], search_items))


# 比對使用者問題與所有常見問法
def search_faq(user_question, faq_vectors):
    response = ollama.embed(
        model=MODEL,
        input=user_question
    )

    user_vector = response["embeddings"][0]
    results = {}

    for vector, (question, faq) in faq_vectors:
        score = cosine_similarity(user_vector, vector)

        faq_id = faq["id"]

        # 同一筆 FAQ 只保留最高相似度
        if faq_id not in results or score > results[faq_id][0]:
            results[faq_id] = (score, faq)

    return sorted(
        results.values(),
        key=lambda item: item[0],
        reverse=True
    )


print("===== 校園 FAQ AI 語意搜尋系統 =====")
print("正在載入 AI 模型...")

try:
    faq_vectors = prepare_faq()
except Exception as e:
    print("AI 模型連線失敗：", e)
    raise SystemExit(1)

print("AI 模型準備完成！")
print("輸入 exit 可以結束程式")

while True:
    question = input("\n請輸入你的問題：").strip()

    if question.lower() == "exit":
        print("感謝使用，再見！")
        break

    if not question:
        print("請先輸入問題。")
        continue

    try:
        results = search_faq(question, faq_vectors)
    except Exception as e:
        print("搜尋失敗：", e)
        continue

    if not results:
        print("FAQ 資料庫目前沒有內容。")
        continue

    score, faq = results[0]

    print("\n===== 相似度測試資料 =====")

    for test_score, test_faq in results:
        print(
            f"{test_faq['question']}："
            f"{test_score:.2%}"
        )

    # 暫定相似度門檻，之後依測試結果調整
    THRESHOLD = 0.65

    if score < THRESHOLD:
        print("\n目前找不到足夠相關的校園 FAQ。")
        print("請換個方式描述問題。")
        continue

   
    print("\n===== AI 搜尋結果 =====")

    print("\n最相關的 FAQ：")
    for rank, (item_score, item_faq) in enumerate(results[:3], start=1):
        print(f"\n{rank}. {item_faq['question']}")
        print(f"   相似度：{item_score:.2%}")
        print(f"   分類：{item_faq['category']}")
        print(f"   答案：{item_faq['answer']}")
        print(f"   來源：{item_faq['source']}")

    print("\n提醒：請依學校最新公告確認實際辦理規定。")


    print("\n注意：相似度不代表答案正確率，")
    print("目前會顯示最相近的 FAQ，仍需核對內容。")


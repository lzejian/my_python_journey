# 📓 风控审核员错题本：A 题 - 核心风控拦截系统

**📅 记录日期**：2026年3月
**🎯 业务场景**：处理 Shopify 实时订单流，利用 Python 清洗并拦截高风险包裹。
**📝 核心任务**：根据三大风控规则（非北美新号、金额超标、高危违禁品超量），输出拦截订单号。

---

## 🚨 我的踩坑记录 (The Bugs)

### ❌ 坑一：“智障保安”与布尔值灾难
* **错误代码**：`country != "US" or "CA"`
* **系统报错**：所有订单全被拦截（命中率 100%）。
* **G老师业务翻译**：Python 的 `or` 是个死脑筋保安。他把这句话劈成两半：左边查国家，右边查 `"CA"`。因为 `"CA"` 这张纸上永远写着字（永远有墨水），保安认为右半边永远成立（`True`），导致规则对所有正常包裹全部开枪。
* **✅ 终极解法（小抄黑名单法）**：`country not in ["US", "CA"]` 

### ❌ 坑二：暴力强拆与跨层级抓取
* **错误代码**：直接用 `order.get("is_new_account", "") == True`
* **系统报错**：永远抓不到新账号，这条风控规则失效。
* **G老师业务翻译**：新账号的勾选框是印在【客户信息登记表】（`customer_info`）里面的。我直接去大包裹外壳上找，当然找不到。
* **✅ 终极解法（连环 .get 递纸条）**：`order.get("customer_info", {}).get("is_new_account", False)`

### ❌ 坑三：把记录本带出了审单室（全局变量污染）
* **错误代码**：把 `order_id_list = []` 写在了 `def` 函数的最外面。
* **系统报错**：P0 级生产事故，不同批次的订单号被无限累加。
* **G老师业务翻译**：函数就是一间专属审单室。必须把新的记录本放在密室**里面**，审完之后从门缝塞出去（`return`）。放在外面会让所有审单员在同一个本子上乱画。

---

## 🏆 满分 SOP 源码 (The Perfect Code)

```python
def filter_risk_orders(orders, amount_threshold, restricted_item):
    # 1. 拿一本崭新的小本本（必须在密室内部！）
    order_id_list = []
    
    # 2. 流水线开始，拿起每一个包裹
    for order in orders:
        
        # 🛡️ 规则 1：非北美区，且是新账户（连环 .get 防身，not in 查黑名单）
        # 💡 if 就是重量秤：True 就是有勾，直接塞给 if，无需写 == True
        if order.get("customer_info", {}).get("country", "未知") not in ["US", "CA"] and \
           order.get("customer_info", {}).get("is_new_account", False):
            order_id_list.append(order.get("order_id", "未知"))
            continue # 盖红章，直接送走，不用看装箱单了
            
        # 🛡️ 规则 2：金额超标（找不到金额就当 0 块钱）
        elif order.get("total_amount", 0) >= amount_threshold:
            order_id_list.append(order.get("order_id", "未知"))
            continue
            
        # 🛡️ 规则 3：翻装箱单，抓违禁品
        for item in order.get("items", []): # 如果没有装箱单，拿个空单子 [] 糊弄过去
            if item.get("product", "") == restricted_item and item.get("qty", 0) >= 3:
                order_id_list.append(order.get("order_id", "未知"))
                break # 抓到一个违禁品就立刻停止翻单子，流水线会自动走下一个包裹
                
    # 3. 审完交差，把本子从门缝塞出去
    return order_id_list
# Scenarios Summary

## 1. NoConstraintsBin
- **CBR Attributes:**
  - Minimize time (weight 1 - Low relevance).
  - Minimize price (weight 1 - Low relevance).
- **Constraints:** None.

---

## 2. NoConstraintsWeightedPrice
- **CBR Attributes:**
  - Minimize time (weight 3 - Moderate relevance).
  - Minimize price (weight 4 - High relevance).
- **Constraints:** None.

---

## 3. NoConstraintsWeightedTimeToDeliver
- **CBR Attributes:**
  - Minimize time (weight 4 - High relevance).
  - Minimize price (weight 3 - Moderate relevance).
- **Constraints:** None.

---

## 4. 1ConstraintBin
- **CBR Attributes:**
  - Minimize price (weight 1 - Low relevance).
  - Maximize time (weight 1 - Low relevance).
- **Constraints:**
  - Delivery time ≤ 60 minutes (weight 1 - Low relevance).

---

## 5. 1ConstraintLikert
- **CBR Attributes:**
  - Minimize price (weight 3 - Moderate relevance).
  - Minimize time (weight 4 - High relevance).
- **Constraints:**
  - Delivery time ≤ 60 minutes (weight 5 - Very high relevance).

---

## 6. 2ConstraintsBin
- **CBR Attributes:**
  - Minimize time (weight 1 - Low relevance).
  - Minimize price (weight 1 - Low relevance).
- **Constraints:**
  - Delivery time ≤ 60 minutes (weight 1 - Low relevance).
  - Price ≤ 100 (weight 1 - Low relevance).

---

## 7. 2ConstraintsLikert
- **CBR Attributes:**
  - Minimize time (weight 4 - High relevance).
  - Minimize price (weight 3 - Moderate relevance).
- **Constraints:**
  - Delivery time ≤ 60 minutes (weight 5 - Very high relevance).
  - Price ≤ 100 (weight 5 - Very high relevance).

---

## 8. 3ConstraintsBin
- **CBR Attributes:**
  - Minimize time (weight 1 - Low relevance).
  - Minimize price (weight 1 - Low relevance).
- **Constraints:**
  - Delivery time ≤ 60 minutes (weight 1 - Low relevance).
  - Price ≤ 100 (weight 1 - Low relevance).
  - Secure container required (weight 1 - Low relevance).

---

## 9. 3ConstraintsLikert
- **CBR Attributes:**
  - Minimize time (weight 4 - High relevance).
  - Minimize price (weight 3 - Moderate relevance).
- **Constraints:**
  - Delivery time ≤ 60 minutes (weight 5 - Very high relevance).
  - Price ≤ 100 (weight 5 - Very high relevance).
  - Secure container required (weight 3 - Moderate relevance).

---

## 10. HardConstraintsBin
- **CBR Attributes:**
  - Minimize time (weight 1 - Low relevance).
  - Minimize price (weight 1 - Low relevance).
- **Constraints:**
  - Delivery time ≤ 60 minutes (weight 1 - Low relevance).
  - Price ≤ 100 (weight 1 - Low relevance).
  - Secure container required (weight 6 - Hard constraint).

---

## 11. HardConstraintsLikert
- **CBR Attributes:**
  - Minimize time (weight 4 - High relevance).
  - Minimize price (weight 3 - Moderate relevance).
- **Constraints:**
  - Delivery time ≤ 60 minutes (weight 5 - Very high relevance).
  - Price ≤ 100 (weight 4 - High relevance).
  - Secure container required (weight 6 - Hard constraint).

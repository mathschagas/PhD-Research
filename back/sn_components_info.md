# Summary of Mock Components

## 1. Drone
- **Speed:** 40–60 km/h.
- **Cost per km:** 7–12 units.
- **Service cost:** Always 0.
- **Distance to package:** 0–5 km.
- **Safe to rain:** 0 (not safe) to 1 (safe).
- **Secure container:** 0 (no) to 1 (yes).

---

## 2. Car
- **Speed:** 30–80 km/h.
- **Cost per km:** 9–15 units.
- **Service cost:** Always 0.
- **Distance to package:** 0–5 km.
- **Safe to rain:** Always 1 (safe).
- **Secure container:** 0 (no) to 1 (yes).

---

## 3. Bicycle
- **Speed:** 15–25 km/h.
- **Cost per km:** 2–5 units.
- **Service cost:** Always 0.
- **Distance to package:** 0–5 km.
- **Safe to rain:** 0 (not safe) to 1 (safe).
- **Secure container:** 0 (no) to 1 (yes).

---

## 4. Truck
- **Speed:** 30–50 km/h.
- **Cost per km:** 20–30 units.
- **Service cost:** Always 0.
- **Distance to package:** 0–5 km.
- **Safe to rain:** Always 1 (safe).
- **Secure container:** Always 1 (yes).

---

## 5. Pedestrian
- **Speed:** 3–5 km/h.
- **Cost per km:** Always 0.
- **Service cost:** Always 0.
- **Distance to package:** 0–5 km.
- **Safe to rain:** Always 0 (not safe).
- **Secure container:** Always 0 (no).

---

# Key Observations:
- **Safe to Rain:**  
  Only **car** and **truck** are consistently rain-safe (value always 1). Others range from not safe to safe (0–1), except **pedestrian**, which is always unsafe.

- **Secure Container:**  
  Only **truck** always provides a secure container (value 1). Other vehicles may or may not provide secure containers (0–1), while **pedestrian** lacks this feature.

- **Cost Efficiency:**  
  **Bicycle** is the cheapest option per km (2–5 units). **Truck** is the most expensive (20–30 units).

- **Speed:**  
  **Car** has the highest potential speed range (30–80 km/h), while **pedestrian** is the slowest (3–5 km/h).

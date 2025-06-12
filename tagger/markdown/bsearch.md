
# Binary Search

## โจทย์

เขียนฟังก์ชัน binary search เพื่อค้นหาค่าเป้าหมายใน array ที่เรียงลำดับแล้ว

**Input:**

*   `arr`: `vector<int>` ของจำนวนเต็มที่เรียงลำดับจากน้อยไปมาก
*   `target`: `int` จำนวนเต็มที่ต้องการค้นหา

**Output:**

*   `int`: index ของ `target` ใน `arr` ถ้าพบ
*   `-1`: ถ้าไม่พบ `target` ใน `arr`

**ข้อกำหนด:**

*   ต้องใช้ binary search เท่านั้น
*   `arr` จะเรียงลำดับจากน้อยไปมากเสมอ
*   ถ้า `target` ปรากฏมากกว่าหนึ่งครั้งใน `arr` ให้ return index ใดก็ได้

**ตัวอย่าง:**

```
arr = {2, 5, 7, 8, 11, 12}
target = 13

return -1
```

```
arr = {2, 5, 7, 8, 11, 12}
target = 12

return 5
```

## วิธี execute
เข้าไปที่ directory binary_search
รันคำสั่ง make run build


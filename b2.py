# Test case 1: 
# order_id = 999 không có trong orders_db
# hàm chỉ in "Order not found!" nhưng không raise HTTPException(status_code=404)
# nên API vẫn trả về 200.

# Test case 2: 
# giá trị "TRONG_SANG" không thuộc ["PENDING", "SHIPPING", "DELIVERED"]
# API trả về một object chứa "error" nhưng vẫn dùng HTTP 200 
# thay vì mã lỗi phù hợp (400 hoặc 422).

# code sửa:
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

orders_db = [
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]

class StatusUpdate(BaseModel):
    status: str

VALID_STATUS = ["PENDING", "SHIPPING", "DELIVERED"]

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if data.status not in VALID_STATUS:
        raise HTTPException(status_code=400, detail="Trạng thái không hợp lệ")
    order["status"] = data.status
    return {
        "statusCode": 200,
        "message": "Cập nhật thành công",
        "data": order
    }

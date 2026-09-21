import requests
from config import COOKIE, AREA_ID, BUILDING_CODE, FLOOR_CODE, ROOM_CODE, PLATFORM

def query_electricity():
    url = "https://application.xiaofubao.com/app/electric/queryRoomSurplus"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": COOKIE,
        "Host": "application.xiaofubao.com",
        "Origin": "https://application.xiaofubao.com",
        "Referer": "https://application.xiaofubao.com/",
    }
    
    data = {
        "areaId": AREA_ID,
        "buildingCode": BUILDING_CODE,
        "floorCode": FLOOR_CODE,
        "roomCode": ROOM_CODE,
        "platform": PLATFORM,
    }
    
    try:
        resp = requests.post(url, headers=headers, data=data, timeout=12)
        resp.raise_for_status()
        result = resp.json()
        
        if result.get("success") and result.get("statusCode") == 0:
            d = result.get("data", {})
            return {
                "success": True,
                "surplus": float(d.get("surplus", 0)),
                "amount": float(d.get("amount", 0)),
                "room_name": d.get("displayRoomName", "未知房间"),
            }
        else:
            return {
                "success": False,
                "message": result.get("message", "查询失败")
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"请求异常: {str(e)}"
        }

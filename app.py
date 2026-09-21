#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request
from datetime import datetime
from config import LOW_THRESHOLD
from api import query_electricity
from database import init_db, save_record, get_yesterday_surplus, get_history

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    return render_template("index.html", low_threshold=LOW_THRESHOLD)

@app.route("/api/query")
def api_query():
    result = query_electricity()
    
    if not result["success"]:
        return jsonify(result)
    
    surplus = result["surplus"]
    amount = result["amount"]
    room = result["room_name"]
    
    # 计算今日用电量
    yesterday_surplus = get_yesterday_surplus()
    daily_usage = None
    if yesterday_surplus is not None:
        daily_usage = round(yesterday_surplus - surplus, 2)
        if daily_usage < 0:
            daily_usage = 0.0
    
    save_record(surplus, amount, room, daily_usage)
    
    return jsonify({
        "success": True,
        "surplus": surplus,
        "amount": amount,
        "room_name": room,
        "daily_usage": daily_usage,
        "is_low": surplus < LOW_THRESHOLD,
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/api/history")
def api_history():
    limit = request.args.get("limit", 30, type=int)
    rows = get_history(limit)
    data = []
    for date_str, surplus, amount, usage, room in rows:
        data.append({
            "date": date_str,
            "surplus": surplus,
            "amount": amount,
            "daily_usage": usage,
            "room_name": room
        })
    return jsonify({"success": True, "data": data})

if __name__ == "__main__":
    # 手机访问请使用电脑的局域网 IP，例如 http://192.168.1.100:5000
    app.run(host="0.0.0.0", port=5000, debug=False)

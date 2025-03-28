from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/redeem/<string:linkgift>/<string:phone>", methods=["GET"])
def redeem_voucher(linkgift, phone):
    url = f"https://gift.truemoney.com/campaign/vouchers/{linkgift}/redeem"
    
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://gift.truemoney.com",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }
    
    data = {
        "mobile": phone,
        "voucher_hash": linkgift
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        
        if response_data["status"]["code"] == "SUCCESS":
            return jsonify({
                "success": True,
                "amount_baht": response_data["data"]["voucher"]["amount_baht"],
                "message": "รับซองสำเสร็จ!"
            })
        else:
            return jsonify({
                "success": False,
                "message": response_data["status"]["message"]
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Error redeeming voucher",
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

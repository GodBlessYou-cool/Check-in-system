import os
import cv2
import requests
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import quote
from utils.aws_utils import get_config
from utils.face_utils import *

load_dotenv()
config = get_config()

class CustomerDataRetriever:
    def __init__(self, token):
        self.token = token
        self.member_data_url = 'https://staging.stickie.link/api/v1/membership/member_data'

    def get_purchase_summary(self, member_identifier):
        try:
            url = f"{self.member_data_url}?link={quote(member_identifier)}"
            response = requests.get(
                url,
                headers={
                    'Authorization': f"Bearer {self.token}",
                    'Accept': 'application/json'
                },
                timeout=10
            )

            if not response.ok:
                return {'error': True, 'message': f"API error {response.status_code}"}

            data = response.json()
            return self.process_purchase_summary(data)

        except Exception as e:
            return {'error': True, 'message': str(e)}

    def process_purchase_summary(self, data):
        if not data.get('data') or not data['data'].get('user'):
            return {
                'product_summaries': [],
                'total_items': 0
            }

        orders = data['data']['user'].get('orders', [])
        summary = {}
        total_items = 0

        for order in orders:
            order_date = order.get('created_at')
            for product in order.get('order_products', []):
                product_info = product['product']
                product_name = product_info.get('name')
                qty = product['product_quantity']
                total_items += qty

                if product_name not in summary:
                    summary[product_name] = {
                        'quantity': qty,
                        'last_order_date': order_date
                    }
                else:
                    summary[product_name]['quantity'] += qty
                    if order_date > summary[product_name]['last_order_date']:
                        summary[product_name]['last_order_date'] = order_date

        formatted = [
            {
                'product_name': name,
                'total_quantity': data['quantity'],
                'last_order_date': self.format_date(data['last_order_date'])
            }
            for name, data in summary.items()
        ]

        return {
            'product_summaries': formatted,
            'total_items': total_items
        }

    def format_date(self, date_string):
        try:
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d')
        except:
            return date_string.split('T')[0]

def capture_face_from_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return None

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    print("\nLooking for faces. Please come close and look at the camera.")

    captured_image = None
    face_detected_time = None
    capture_delay = 2  # 2 seconds hold required
    min_face_area = 160 * 160  # Closer face required
    face_detecting = False

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to capture frame")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            current_time = datetime.now()

            if len(faces) > 0:
                x, y, w, h = max(faces, key=lambda f: f[2] * f[3])

                face_area = w * h

                if face_area >= min_face_area:
                    if not face_detecting:
                        face_detected_time = current_time
                        face_detecting = True

                    elapsed = (current_time - face_detected_time).total_seconds()
                    cv2.putText(frame, f"Hold Still: {elapsed:.2f}s", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                    if elapsed >= capture_delay:
                        captured_image = frame[y:y + h, x:x + w]
                        print("📸 Face captured!")
                        break
                else:
                    face_detected_time = None
                    face_detecting = False
            else:
                face_detected_time = None
                face_detecting = False

            if len(faces) > 0:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow('Face Detection - Press ESC to quit', frame)
            if cv2.waitKey(1) == 27:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

    if captured_image is not None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"captured_face_{timestamp}.jpg"
        cv2.imwrite(image_path, captured_image)
        return image_path
    return None

def login_to_stickie():
    url = "https://staging.stickie.link/api/v1/login"
    payload = {
        "email": "kishore@stickies.tech",
        "password": "Abc123"
    }
    try:
        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
        return res.json().get("token")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return None

def get_all_membership_data(token):
    url = "https://staging.stickie.link/api/v1/membership/data"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        return res.json().get('data', {}).get('data', [])
    except Exception as e:
        print(f"❌ Error fetching membership data: {e}")
        return None

def main():
    print("=== Face Recognition & Purchase Summary ===\n")

    image_path = capture_face_from_camera()
    if not image_path:
        print("❌ No face captured.")
        return

    try:
        image = cv2.imread(image_path)
        _, img_encoded = cv2.imencode('.jpg', image)
        image_bytes = img_encoded.tobytes()

        print("\n🔍 Matching face in AWS Rekognition...")
        match_response = search_face_in_collection(image_bytes, threshold=80)

        if match_response and match_response.get('FaceMatches'):
            face_id = match_response['FaceMatches'][0]['Face']['FaceId']
            confidence = match_response['FaceMatches'][0]['Similarity']
            print(f"✅ Face matched with {confidence:.2f}% confidence")

            customer = get_customer(face_id)
            if not customer:
                print("⚠️ Face found but no linked customer.")
                return

            name = customer.get('name', 'Unknown')
            member_id = customer.get('member_id')
            print(f"\n👋 Welcome, {name}")
            print(f"🆔 Face ID: {face_id}")
            print(f"🔗 Member ID: {member_id}")

            print("\n🔐 Logging in to Stickie...")
            token = login_to_stickie()
            if not token:
                return

            print("📡 Fetching membership info...")
            members = get_all_membership_data(token)
            if not members:
                print("⚠️ No membership data.")
                return

            for member in members:
                if str(member.get("member_id")) == str(member_id):
                    user = member.get("user", {})
                    link = user.get('link') or member.get('link') or member_id
                    print("\n📋 --- Membership Details ---")
                    print(f"Name: {user.get('name')}")
                    print(f"Email: {user.get('email')}")
                    print(f"Phone: {user.get('phone')}")
                    print(f"Tier: {member.get('tier', {}).get('name', 'Standard')}")
                    print(f"Link: {link}")

                    retriever = CustomerDataRetriever(token)
                    print("\n🧾 Fetching purchase summary...")
                    summary = retriever.get_purchase_summary(link)

                    if isinstance(summary, dict) and summary.get('error'):
                        print(f"❌ Error: {summary['message']}")
                    else:
                        print("\n🛍️ --- Purchase Summary ---")
                        print(f"📦 Total Items Purchased: {summary['total_items']}\n")
                        for idx, item in enumerate(summary['product_summaries'], 1):
                            print(f"{idx}️⃣ Product: {item['product_name']}")
                            print(f"   🔢 Quantity: {item['total_quantity']} pcs")
                            print(f"   📅 Last Ordered: {item['last_order_date']}\n")
                    break
        else:
            print("\n🙅 User not identified.")

    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"🗑️ Removed temp image {image_path}")

if __name__ == "__main__":
    main()

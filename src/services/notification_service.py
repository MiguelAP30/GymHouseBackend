import httpx
from src.schemas.notification import Notification

class NotificationService:
    def __init__(self):
        self.expo_push_api = "https://exp.host/--/api/v2/push/send"

    async def send_notification(self, notification: Notification):
        message = {
            "to": notification.token,
            "title": notification.title,
            "body": notification.message,
            "sound": "default",
            "priority": "high",
            "channelId": "default"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.expo_push_api,
                    json=message,
                    headers={
                        "Accept": "application/json",
                        "Accept-Encoding": "gzip, deflate",
                        "Content-Type": "application/json"
                    }
                )
                return response.json()
        except Exception as e:
            return {"error": str(e)} 
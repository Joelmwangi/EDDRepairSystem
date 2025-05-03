class NotificationService:
    @staticmethod
    def notify_customer(customer, message):
        print(f"Notification sent to {customer.name} ({customer.email}): {message}")


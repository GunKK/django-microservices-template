import notificationApi from '../apis/notificationApi.js';

class NotificationEvent {
    constructor(token, data, userIds, notificationType) {
        this.token = token;
        this.data = data;
        this.userIds = userIds;
        this.notificationType = notificationType;
    }

    async create() {
        // Prepare form data for the notification
        const formData = {
            data: this.data,
            user_ids: this.userIds,
            notify_type: this.notificationType,
        };

        // Call the notification API to create the notification
        try {
            await notificationApi.create(this.token, formData);
            console.log("Notification created successfully.");
        } catch (err) {
            console.error("Error creating notification:", err);
            throw new Error('Failed to create notification');
        }
    }
}

export default NotificationEvent;

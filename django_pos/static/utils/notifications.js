function fethAllNotifications(notifications_url) {
  $.ajax({
    url: notifications_url,
    type: "GET",
    success: function (data) {
      for (let i = 0; i < data.length; i++) {
        let notification = data[i];
        saveNotificationToSessionStorage(
          notification.id,
          notification.title,
          notification.message,
          notification.date
        );
      }
    },
  });
}

function saveNotificationToSessionStorage(id, title, message, date) {
  let notification = {
    id: id,
    title: title,
    message: message,
    date: date,
  };
  let notifications = JSON.parse(sessionStorage.getItem("notifications"));
  if (notifications == null) {
    notifications = [];
  }
  // if the notification is not already saved
  if (!notifications.some((n) => n.id === id)) {
    notifications.push(notification);
    sessionStorage.setItem("notifications", JSON.stringify(notifications));
  }
}

$("#close_notifications_modal").click(function () {
  $("#notificationsModal").modal("hide");
});
$("#close_notif").click(function () {
  $("#viewNotificationModal").modal("hide");
});

function viewNotification(id, title, message, date) {
  // close notifications modal
  $("#notificationsModal").modal("hide");
  //actions on the right

  $("#viewNotificationModalLabel").text(title);
  $("#notification_message").text(message);
  $("#notification_date").text(date);
  $("#viewNotificationModal").modal("show");
}

function loadNotifications() {
  // read notifications from session storage and display them
  var notifications = JSON.parse(sessionStorage.getItem("notifications"));
  if (notifications) {
    var notificationsDiv = document.getElementById("notifications");
    notificationsDiv.innerHTML = "";

    notifications.forEach((notification) => {
      var notificationDiv = document.createElement("div");
      // add on hover to show its clickable like a button
      notificationDiv.onmouseover = function () {
        notificationDiv.style.backgroundColor = "lightgray";
      };
      notificationDiv.onmouseout = function () {
        // reset background color
        notificationDiv.style.backgroundColor = "";
      };
      notificationDiv.style.cursor = "pointer";

      notificationDiv.className = "alert alert-info";
      notificationDiv.role = "alert";
      notificationDiv.innerHTML = `<strong>${notification.title}</strong> ${notification.message}`;
      // date to the right
      var dateSpan = document.createElement("span");
      dateSpan.style.float = "right";
      dateSpan.style.fontSize = "12px";
      dateSpan.style.color = "gray";
      dateSpan.innerHTML = notification.date;
      notificationDiv.appendChild(dateSpan);

      notificationDiv.onclick = function () {
        viewNotification(
          notification.id,
          notification.title,
          notification.message,
          notification.date
        );
      };
      notificationsDiv.appendChild(notificationDiv);
    });
  }
}
loadNotifications();

// refresh notifications every 1 minute
setInterval(() => {
  loadNotifications();
}, 100000);

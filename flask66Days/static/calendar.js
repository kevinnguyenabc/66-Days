checkins = checkins.slice(1, -1).split(",");
checkins = checkins.map((value) => parseInt(value));
console.log(checkins);

let date = new Date(date_created);
console.log(date);

let checkedInColor = "blue";

let events = [];
let newCheckIns = [];

for (let i = 0; i < checkins.length; i++) {
  let newDate = new Date();
  newDate.setDate(date.getDate() + checkins[i]);
  newCheckIns.push(checkins[i]);
  let int = newDate.getTime() - newDate.getTimezoneOffset() * 60 * 1000;
  newDate = new Date(int);
  events.push({
    start: newDate.toISOString().slice(0, 10),
    display: "background",
    overlay: false,
    backgroundColor: "#000F9A",
    id: checkins[i],
  });
}

console.log("events", events);

document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");
  var calendar = new FullCalendar.Calendar(calendarEl, {
    editable: true,
    timeZone: "local",
    initialView: "dayGridMonth",
    events: [
      {
        id: -1,
        start: new Date(date_created).toISOString().split("T")[0],
        display: "background",
        backgroundColor: "green",
        title: "Start",
      },
    ].concat(events),
    dateClick: function (info) {
      console.log("date clicked");

      let id = info.date.getDate() - date.getDate();
      if (newCheckIns.includes(id)) {
        info.dayEl.style.backgroundColor = "";
        newCheckIns = newCheckIns.filter((val) => val !== id);
      } else {
        console.log(date.toJSON().slice(0, 10));
        console.log(info.date.toJSON().slice(0, 10));

        info.dayEl.style.backgroundColor =
          date.toJSON().slice(0, 10) == info.date.toJSON().slice(0, 10)
            ? "#1940A3"
            : "#355489";
        newCheckIns.push(id);
      }
      console.log(newCheckIns);
    },

    eventClick: function (info) {
      console.log("eventclick", events);
      if (info.event.id != -1) {
        info.event.remove();
      }
    },

    validRange: {
      start: new Date(date_created).toISOString().split("T")[0],
      end: Date.now(),
    },
    eventRender: function (event, element) {
      element.find(".fc-title").append("<br/>" + event.description);
    },
  });
  calendar.render();
});

console.log(newCheckIns.toString());
$("#updateCheckInsButton").click(function updateCheckins() {
  jQuery.ajax({
    dataType: "text", // Setting return data type
    contentType: "application/json",
    method: "POST", // Setting request method
    url: "/update_checkins", // Setting request url, mapped to routes.py
    data: JSON.stringify({
      id: id,
      checkIns: checkins,
      newCheckIns: newCheckIns,
    }),
    success: (url) => (window.location.href = url), // Setting callback function to handle data returned successfully by the SingleStarServlet
  });
});

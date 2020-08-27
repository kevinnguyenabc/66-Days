checkins = checkins.slice(1, -1).split(",");
console.log(checkins);

let date = new Date(date_created);
console.log(date);

let checkedInColor = "blue";

let events = [];
let newCheckIns = [];

for (let i = 0; i < checkins.length; i++) {
  let newDate = new Date();
  newDate.setDate(date.getDate() + parseInt(checkins[i]));
  newCheckIns.push(parseInt(checkins[i]));
  let int = newDate.getTime() - newDate.getTimezoneOffset() * 60 * 1000;
  newDate = new Date(int);
  events.push({
    start: newDate.toISOString().slice(0, 10),
    display: "background",
    backgroundColor: "blue",
    id: parseInt(checkins[i]),
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
        title: "Start"
      },
    ].concat(events),
    dateClick: function (info) {
      // alert('Clicked on: ' + info.dateStr);
      // alert('Coordinates: ' + info.jsEvent.pageX + ',' + info.jsEvent.pageY);
      // alert('Current view: ' + info.view.type);
      // change the day's background color just for fun
      console.log("date clicked");
      console.log("inside dateclick events", events);

      let id = info.date.getDate() - date.getDate();
      if (newCheckIns.includes(id)) {
        info.dayEl.style.backgroundColor = "";
        newCheckIns = newCheckIns.filter((val) => val !== id);
      } else {
        info.dayEl.style.backgroundColor = "rgb(30, 50, 211)";
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

  //   function eventExists(dateStr) {
  //     let id = dateStr.getDate() - date.getDate();
  //     console.log(dateStr.getDate() - date.getDate());
  //     console.log("Hello", calendar.getEventById(id));
  //     return calendar.getEventById(id);
  //   }

  function addEvent(id) {
    event = {
      start: newDate.toISOString().split("T")[0],
      display: "background",
      backgroundColor: "blue",
      id: id,
      checked_in: true,
      editable: true,
    };
  }
});

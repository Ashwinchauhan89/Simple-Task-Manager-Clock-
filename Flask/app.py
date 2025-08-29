from flask import Flask, render_template, request, redirect, url_for
from threading import Thread
import time
from datetime import datetime
import uuid

app = Flask(__name__)
reminders = [] 


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form["message"]
        reminder_time = request.form["time"]

        try:
            reminder_dt = datetime.strptime(reminder_time, "%Y-%m-%dT%H:%M")
            reminder_id = str(uuid.uuid4())
            reminders.append({
                "id": reminder_id,
                "time": reminder_dt,
                "message": message,
                "triggered": False
            })
        except ValueError:
            pass

        return redirect(url_for("index"))

    now = datetime.now()
    active_reminders = [r for r in reminders if not r["triggered"] and r["time"] <= now]

    return render_template("index.html", reminders=reminders, active=active_reminders)


@app.route("/delete/<reminder_id>", methods=["POST"])
def delete_reminder(reminder_id):
    global reminders
    reminders = [r for r in reminders if r["id"] != reminder_id]
    return redirect(url_for("index"))


def reminder_checker():
    while True:
        now = datetime.now()
        for reminder in reminders:
            if not reminder["triggered"] and reminder["time"] <= now:
                print(f"[REMINDER] {reminder['message']} at {reminder['time']}")
                reminder["triggered"] = True
        time.sleep(5)


if __name__ == "__main__":
    checker_thread = Thread(target=reminder_checker, daemon=True)
    checker_thread.start()
    app.run(debug=True)



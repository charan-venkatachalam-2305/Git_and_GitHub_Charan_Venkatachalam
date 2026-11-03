import os
import json
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

#Flask App instance creation
app = Flask(__name__)

#Loading the MongoDB credentials
load_dotenv("atlas-credentials.env")

MONGODB_URI = os.getenv("MONGODB_URI")

#Connecting to MongoDB Atlas
client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=5000
    )

db = client.demo
collection = db["flask-tutorial"]

#Home page
@app.route("/")
def index():
    return render_template("index.html", error=None)


#Reading the JSON file using Python File Handling and to return its data
@app.route("/api")
def api():
    try:
        with open("api_data.json", "r") as file:
            data = json.load(file)
        return jsonify(data)

    except (OSError, json.JSONDecodeError):
        return jsonify({"error": "Could not read the JSON file."}), 500



#Receiving the form data and storing it in MongoDB
@app.route("/submit", methods=["POST"])
def submit():
    #Getting the values entered by the user
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    course = request.form.get("course", "").strip()

    try:
        #Checking the database connection using ping
        client.admin.command("ping")

        #Inserting the form data into MongoDB
        collection.insert_one({
            "name": name,
            "email": email,
            "course": course
        })

        #Redirecting only after successful insertion
        return redirect(url_for("success"))

    except Exception:
    #Displaying the error in the terminal
        app.logger.exception("Could not submit data to MongoDB")

    #Displaying the error on the form page
        return render_template(
            "index.html",
            error="Submission failed. Please check the database connection."
        ), 500

#Receiving To-Do item data and storing it in MongoDB
@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    #Getting the values entered by the user
    item_name = request.form.get("itemName", "").strip()
    item_description = request.form.get("itemDescription", "").strip()
    try:
        #Checking the database connection using ping
        client.admin.command("ping")
        #Inserting the To-Do item into MongoDB
        collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description
        })
        return "To-Do item submitted successfully!"
    except Exception:
        #Displaying the error in the terminal
        app.logger.exception("Could not submit To-Do item to MongoDB")
        return "Submission failed. Please check the database connection.", 500

#Success Page
@app.route("/success")
def success():
    return render_template("success.html")


#Running the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
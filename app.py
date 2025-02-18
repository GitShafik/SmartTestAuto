from flask import Flask, request, render_template, redirect, url_for, flash
import pymongo

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["smarttestauto"]
messages = db["messages"]  

@app.route("/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if all([name, email, message]):
            try:
                messages.insert_one({"name": name, "email": email, "message": message})  # ✅ Using `messages`
                print(" Message saved to MongoDB!")  
                flash("Your message has been sent successfully!", "success")
            except Exception as e:
                print(f" Database Insert Error: {e}") 
                flash("Failed to send message. Please try again.", "error")
        else:
            flash("Please fill in all fields.", "error")

        return redirect(url_for("contact"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

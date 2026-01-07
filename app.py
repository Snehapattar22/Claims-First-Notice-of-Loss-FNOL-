from dotenv import load_dotenv
load_dotenv()   

import os
import sqlite3
import uuid
from flask import Flask, request, jsonify, render_template

from database.db import init_db
from documents.documentsProcessor import extract_text_from_document
from llm.empatheticGuide import empathetic_response
from llm.structuredExtractor import extract_claim_details



app = Flask(__name__)
init_db()

UPLOAD_FOLDER = "uploads/claimDocs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit")
def submit():
    return render_template("claim.html")


@app.route("/guide", methods=["POST"])
def guide():
    user_msg = request.json["message"]
    reply = empathetic_response(user_msg)
    return jsonify({"reply": reply})


@app.route("/claim", methods=["POST"])
def claim():
    policy_number = request.form["policy_number"]
    incident_date = request.form["incident_date"]
    location = request.form["location"]
    text = request.form["incident_text"]
    doc = request.files["document"]

    file_path = os.path.join(UPLOAD_FOLDER, doc.filename)
    doc.save(file_path)

    doc_text = extract_text_from_document(file_path)
    combined_text = f"""
    Policy Number: {policy_number}
    Date: {incident_date}
    Location: {location}
    Description: {text}
    {doc_text}
    """

    claim_data = extract_claim_details(combined_text)
    claim_id = str(uuid.uuid4())

    conn = sqlite3.connect("claims.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO claims VALUES (?,?,?,?,?,?,?)
    """, (
        claim_id,
        policy_number,
        claim_data.get("incident_type"),
        incident_date,
        location,
        text,
        "Pending"
    ))
    conn.commit()
    conn.close()

    return f"""
    <h3>Claim Submitted Successfully </h3>
    <p><b>Claim ID:</b> {claim_id}</p>
    """



if __name__ == "__main__":
    app.run(debug=True)

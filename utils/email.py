import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

backend_base_url = os.getenv("BACKEND_URL")

def send_job_email(job):
    subject = f"Új állás: {job.get('title')} ({job.get('ai_recommendation_1_10')}/10)"#
    job_id = job.get("link")  # egyszerű azonosító
    yes_url = f"{backend_base_url}/label?job_id={job_id}&label=1"
    no_url = f"{backend_base_url}/label?job_id={job_id}&label=0"
    

    html = f"""
    <h2>{job.get('title')}</h2>
    <p><b>Hely:</b> {job.get('place')}</p>
    <p><b>Bér:</b> {job.get('wage')}</p>
    <p><b>AI pontszám:</b> {job.get('ai_recommendation_1_10')}/10</p>
    <p>Link: {job.get("link")}</p>
    <p>{job.get('desc')[:1000]}</p>

    <a href="{yes_url}" 
       style="padding:10px 16px;background:#22c55e;color:white;text-decoration:none;border-radius:6px;">
       ✅ Érdekel
    </a>

    &nbsp;

    <a href="{no_url}" 
       style="padding:10px 16px;background:#ef4444;color:white;text-decoration:none;border-radius:6px;">
       ❌ Nem érdekel
    </a>
    """

    msg = MIMEMultipart()
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = os.getenv("TO_EMAIL")
    msg["Subject"] = subject
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        server.send_message(msg)
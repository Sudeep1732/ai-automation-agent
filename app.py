import smtplib
from email.mime.text import MIMEText
from openai import OpenAI
import streamlit as st

# 🔑 PUT YOUR API KEY HERE
client = OpenAI(
    api_key="YOUR-API-KEY",
    base_url="https://openrouter.ai/api/v1"
)
def send_email(to_email, content):
    sender_email = "youremail@gmail.com"
    app_password = "gmail-app-passworf"

    msg = MIMEText(content)
    msg["Subject"] = "AI Study Assistant"
    msg["From"] = sender_email
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(msg)
    server.quit()

    return "✅ Email sent successfully!"

st.title("🤖 AI Automation Agent")
st.caption("An AI agent that understands user intent and performs tasks like summarization and automated email sending.")
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input(
    "Enter your request:",
    placeholder="e.g. Summarize text, explain AI, send email to someone..."
)
email_input = st.text_input(
    "Recipient email:",
    placeholder="e.g. example@gmail.com"
)
st.divider()
if st.button("📄 Summarize Text"):
    summary = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize clearly"},
            {"role": "user", "content": user_input}
        ]
    )
    st.write(summary.choices[0].message.content)

if st.button("🧠 Explain Concept"):
    eli5 = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Explain like a beginner"},
            {"role": "user", "content": user_input}
        ]
    )
    st.write(eli5.choices[0].message.content)
if st.button("📧 Generate & Send Email"):
    if not user_input or not email_input:
        st.warning("Enter both message and email")
    else:
        # Generate email content using AI
        email_content = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Write a professional email"},
                {"role": "user", "content": user_input}
            ]
        ).choices[0].message.content

        result = send_email(email_input, email_content)

        st.success(result)
        st.write("📨 Email Content:")
        st.write(email_content)
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # 🧠 AUTO-DETECT EMAIL TASK
        if "@" in user_input and "email" in user_input.lower():

            # Extract email
            extract = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Extract only the email address"},
                    {"role": "user", "content": user_input}
                ]
            )
            to_email = extract.choices[0].message.content.strip()

            # Generate email
            email_content = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Write a professional email"},
                    {"role": "user", "content": user_input}
                ]
            ).choices[0].message.content

            send_email(to_email, email_content)

            reply = f"📧 Email sent to {to_email}"

        else:
            # Normal response
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )

            reply = response.choices[0].message.content

    except Exception as e:
        reply = f"Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})

# Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑‍🎓 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **AI:** {msg['content']}")

# nexthub-certificate-generator-application


# 🎓 Certificate Generator Web App

An automated certificate generation and distribution web application built with **Flask**. Users can upload a certificate template, Excel sheet with participant details, and generate personalized certificates. The app also supports **email delivery**, **live preview**, and **responsive mobile UI**.

## 🚀 Features

* Upload a certificate template (`.png` or `.jpg`)
* Upload participant data via Excel (`.xlsx`)
* Live preview before download
* Automatic certificate generation with name placement
* Email delivery to recipients (Gmail/SMTP support)
* Mobile-responsive UI
* Download generated certificates as ZIP
* Custom font and positioning options (optional enhancement)

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **Frontend**: HTML, CSS, JavaScript (Bootstrap)
* **Libraries**:

  * `Pillow` for image processing
  * `pandas` for reading Excel files
  * `flask` for web framework
  * `smtplib`, `email` for sending emails

## 📂 Folder Structure

```
certificate-generator/
│
├── static/
│   └── uploads/               # Uploaded certificate templates
│
├── templates/
│   └── index.html             # Main frontend page
│
├── generated_certificates/   # Output directory for generated certificates
│
├── app.py                    # Main Flask application
├── requirements.txt          # Required Python libraries
├── README.md                 # Project documentation
```

## 📦 Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/certificate-generator.git
   cd certificate-generator
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser.

## 🧾 Excel Format

The Excel file should contain a column named **Name** and optionally **Email**:

```
| Name         | Email                |
|--------------|----------------------|
| Alice Smith  | alice@example.com    |
| Bob Johnson  | bob@example.com      |
```

## ✉️ Email Sending Setup

You need to enter your email credentials (email + app password) via the UI.
Make sure to enable "Less Secure Apps" or use **App Passwords** if using Gmail.

## 🖼️ Template Guidelines

* Use a high-resolution `.png` or `.jpg` certificate template
* The placeholder name position can be adjusted via the code/UI settings

## ✅ To-Do (Enhancements)

* [ ] Allow drag-and-drop name positioning (canvas)
* [ ] Add signature & date auto-placement
* [ ] Support for multiple fonts
* [ ] Certificate preview with zoom/pan
* [ ] Admin authentication

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙌 Acknowledgements

* Flask documentation
* Pillow and Pandas community
* Open-source UI libraries


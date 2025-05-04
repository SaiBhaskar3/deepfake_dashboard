from fpdf import FPDF
import os
import datetime

def generate_report(label, confidence, filename="analysis_report.pdf", timestamp=None):
    if timestamp is None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Deepfake Detection Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Generated: {timestamp}", ln=True)
    pdf.cell(200, 10, txt=f"Prediction: {label}", ln=True)
    pdf.cell(200, 10, txt=f"Confidence Score: {confidence}%", ln=True)

    output_dir = os.path.join("static", "reports")
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, filename)

    pdf.output(report_path)
    print(f"📄 Report saved at: {report_path}")
    return filename

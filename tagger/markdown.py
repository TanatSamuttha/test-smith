import fitz  # PyMuPDF
import os    # สำหรับจัดการกับ path ของไฟล์/โฟลเดอร์

def pdf_to_markdown(pdf_folder, markdown_folder, pdf_filename):
    # สร้าง path เต็มของไฟล์ PDF
    pdf_path = os.path.join(pdf_folder, pdf_filename)

    # กำหนดชื่อไฟล์ Markdown (เปลี่ยนนามสกุลจาก .pdf เป็น .md)
    markdown_filename = os.path.splitext(pdf_filename)[0] + ".md"

    # สร้าง path เต็มของไฟล์ Markdown ที่จะบันทึก
    output_markdown_path = os.path.join(markdown_folder, markdown_filename)

    markdown_content = []

    try:
        # ตรวจสอบว่าไฟล์ PDF มีอยู่จริงหรือไม่
        if not os.path.exists(pdf_path):
            print(f"ข้อผิดพลาด: ไม่พบไฟล์ PDF ที่ '{pdf_path}'")
            return

        # ตรวจสอบและสร้างโฟลเดอร์ปลายทางถ้ายังไม่มี
        os.makedirs(markdown_folder, exist_ok=True)

        doc = fitz.open(pdf_path)

        for page_num in range(doc.page_count):
            page = doc[page_num]
            text = page.get_text("text") # ดึงข้อความดิบ

            # เพิ่มหัวข้อบอกเลขหน้าใน Markdown (เลือกใช้หรือไม่ก็ได้)
            markdown_content.append(f"\n\n--- หน้าที่ {page_num + 1} ---\n\n")

            # เพิ่มข้อความที่ดึงมา
            markdown_content.append(text)

        doc.close()

        # รวมข้อความทั้งหมดเป็น string เดียว
        final_markdown = "".join(markdown_content)

        # บันทึกไฟล์ Markdown
        with open(output_markdown_path, "w", encoding="utf-8") as f:
            f.write(final_markdown)

        print(f"แปลง '{pdf_path}' เป็น '{output_markdown_path}' สำเร็จแล้ว")

    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการแปลงไฟล์: {e}")

# --- การใช้งาน ---
# กำหนด path ของโฟลเดอร์ PDF และโฟลเดอร์ Markdown
pdf_input_folder = "tagger/pdf"
markdown_output_folder = "tagger/markdown"

# กำหนดชื่อไฟล์ PDF ที่คุณต้องการแปลง (ต้องอยู่ในโฟลเดอร์ pdf_input_folder)
# เช่น ถ้าไฟล์ของคุณชื่อ "MyDocument.pdf"
pdf_file_to_convert = "yuusha.pdf" # <-- *** แก้ไขชื่อไฟล์ PDF ตรงนี้ ***

# เรียกฟังก์ชันเพื่อเริ่มการแปลง
pdf_to_markdown(pdf_input_folder, markdown_output_folder, pdf_file_to_convert)
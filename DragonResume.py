import PyPDF2
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def merge_pdfs(resume_path, cover_letter_path, output_path):
    pdf_writer = PyPDF2.PdfFileWriter()

    # Read the resume PDF
    try:
        with open(resume_path, 'rb') as resume_file:
            pdf_reader = PyPDF2.PdfFileReader(resume_file)
            if pdf_reader.isEncrypted:
                pdf_reader.decrypt('')
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)
    except Exception as e:
        print(f"Error reading resume file: {e}")
        return

    # Read the cover letter PDF
    try:
        with open(cover_letter_path, 'rb') as cover_letter_file:
            pdf_reader = PyPDF2.PdfFileReader(cover_letter_file)
            if pdf_reader.isEncrypted:
                pdf_reader.decrypt('')
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)
    except Exception as e:
        print(f"Error reading cover letter file: {e}")
        return

    # Write the combined PDF to the output file
    try:
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)
        print(f"Combined PDF saved as {output_path}")
    except Exception as e:
        print(f"Error writing output file: {e}")

def browse_file(entry):
    filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def browse_output(entry):
    filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def main():
    root = tk.Tk()
    root.title("DragonResume")

    tk.Label(root, text="Resume PDF:").grid(row=0, column=0, padx=10, pady=5)
    resume_entry = tk.Entry(root, width=50)
    resume_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_file(resume_entry)).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(root, text="Cover Letter PDF:").grid(row=1, column=0, padx=10, pady=5)
    cover_letter_entry = tk.Entry(root, width=50)
    cover_letter_entry.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_file(cover_letter_entry)).grid(row=1, column=2, padx=10, pady=5)

    tk.Label(root, text="Output PDF:").grid(row=2, column=0, padx=10, pady=5)
    output_entry = tk.Entry(root, width=50)
    output_entry.grid(row=2, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_output(output_entry)).grid(row=2, column=2, padx=10, pady=5)

    def on_merge():
        resume_path = resume_entry.get()
        cover_letter_path = cover_letter_entry.get()
        output_path = output_entry.get()

        if not os.path.exists(resume_path):
            messagebox.showerror("Error", f"Resume file '{resume_path}' not found.")
            return

        if not os.path.exists(cover_letter_path):
            messagebox.showerror("Error", f"Cover letter file '{cover_letter_path}' not found.")
            return

        merge_pdfs(resume_path, cover_letter_path, output_path)
        messagebox.showinfo("Success", f"Combined PDF saved as {output_path}")

    tk.Button(root, text="Merge PDFs", command=on_merge).grid(row=3, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

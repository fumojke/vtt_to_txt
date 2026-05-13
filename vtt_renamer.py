import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox


def clean_vtt_content(vtt_text):
    """Cleans text from WEBVTT and timecodes"""
    text = re.sub(r'WEBVTT', '', vtt_text)
    text = re.sub(r'\d{1,2}:?\d{2}:\d{2}\.\d{3} --> \d{1,2}:?\d{2}:\d{2}\.\d{3}', '', text)
    text = re.sub(r'\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d.3}', '', text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def start_conversion():
    prefix = entry_prefix.get().strip()
    if not prefix:
        messagebox.showwarning("Attention", "Please enter a topic name (e.g. Select Query))")
        return

    source_dir = filedialog.askdirectory(title="Select the folder with subtitles")
    if not source_dir:
        return

    output_dir = os.path.join(source_dir, "cleaned_notes")

    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        def natural_sort_key(s):
            return [int(text) if text.isdigit() else text.lower()
                    for text in re.split(r'(\d+)', s)]

        files = os.listdir(source_dir)
        files.sort(key=natural_sort_key)

        count = 0
        all_text = []

        # NotebookLM Prompt ===
        system_prompt = (
            "SYSTEM INSTRUCTION FOR NOTEBOOKLM:\n"
            f"Topic: {prefix}\n"
            "1. This file contains cleaned subtitles from a SQL course.\n"
            "2. Act as a personal SQL tutor. Use these transcripts as your primary knowledge base.\n"
            "3. Structure your answers based on the lecture titles (marked with ===).\n"
            "4. When explaining code, provide step-by-step logic and relate it to Python if applicable.\n"
            "5. Always suggest a small practical task at the end of each explanation.\n"
            "6. Provide all explanations in Russian, but keep all technical terminology, SQL commands, and industry-specific terms in English.\n"
            "============================================================\n\n"
        )
        all_text.append(system_prompt)

        for filename in files:
            if filename.lower().endswith((".vtt", ".txt")):
                if "_FULL_COURSE_SUMMARY" in filename or "_clean" in filename:
                    continue

                file_path = os.path.join(source_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_content = f.read()

                clean_text = clean_vtt_content(raw_content)

                if clean_text:
                    new_name = os.path.splitext(filename)[0] + "_clean.txt"
                    with open(os.path.join(output_dir, new_name), 'w', encoding='utf-8') as f:
                        f.write(clean_text)

                    all_text.append(f"=== LECTURE: {filename} ===\n{clean_text}\n")
                    count += 1

        if all_text:
            summary_filename = f"{prefix}_FULL_COURSE_SUMMARY.txt"
            with open(os.path.join(output_dir, summary_filename), 'w', encoding='utf-8') as f:
                f.write("\n".join(all_text))

        messagebox.showinfo("Success!", f"File {summary_filename} ready!\nLectures processed: {count}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


root = tk.Tk()
root.title("Udemy Subtitles to NotebookLM")
root.geometry("450x250")

tk.Label(root, text="Setting up a course for NotebookLM", font=("Arial", 12, "bold"), pady=10).pack()

tk.Label(root, text="Enter the topic name (for file name):", font=("Arial", 10)).pack()
entry_prefix = tk.Entry(root, font=("Arial", 10), width=40)
entry_prefix.insert(0, "SQL Course Section")
entry_prefix.pack(pady=5)

tk.Button(root, text="Select a folder and start", command=start_conversion,
          bg="#28a745", fg="white", font=("Arial", 10, "bold"), padx=20, pady=10).pack(pady=20)

root.mainloop()
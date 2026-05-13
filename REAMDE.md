Subtitles Cleaner for NotebookLM
A Python-based GUI utility designed to clean .vtt subtitle files and format them for use with Google NotebookLM. It removes timecodes, headers, and metadata, creating a clean knowledge base for your personal AI tutor.

Features:
Clean VTT Content: Automatically removes WEBVTT tags and complex timecode patterns using RegEx.

Natural Sorting: Sorts lecture files numerically (e.g., Lecture 2 comes before Lecture 10).

NotebookLM Integration: Automatically injects a specialized System Instruction prompt into the final summary file.

GUI Interface: Simple and intuitive interface built with Tkinter.

Batch Processing: Processes entire folders and creates a single consolidated summary for easy upload.
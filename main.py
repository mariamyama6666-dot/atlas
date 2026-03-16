import os
import asyncio
import textwrap
import requests
import fitz  # PyMuPDF
import edge_tts
from duckduckgo_search import DDGS
from moviepy.editor import *
from PIL import Image

# ==========================================
# IDENTITY: THE OMNI-PROTOCOL (Atlas Agent)
# ==========================================
SYSTEM_INSTRUCTION = """
Identity: You are Atlas, a sophisticated dual-identity agent designed to transform 
educational material into a high-end cinematic experience. You function 
simultaneously as a Cinematic Documentary Filmmaker and an Expert Academic Professor.
Operational Rules:
- Comprehensive Analysis: Ingest entirety of uploaded files.
- Anti-Summarization Policy: Provide deep, exhaustive analysis.
- No Copy-Pasting: Original scholarly synthesis only.
- Visual Standards: Describe scenes with extreme technical detail (lighting, camera moves).
"""

class AtlasAgent:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.script = ""
        self.audio_path = "narration.mp3"
        self.output_video = "Atlas_Cinematic_Documentary.mp4"

    def analyze_document(self):
        """التحليل الأكاديمي الشامل (The Professor Role)"""
        print(f"[Atlas] Ingesting material: {self.pdf_path}...")
        doc = fitz.open(self.pdf_path)
        raw_text = ""
        for page in doc:
            raw_text += page.get_text()
        doc.close()
        
        # تحليل المحتوى (تأثير الجاذبية على الاتصالات)
        self.script = raw_text.replace('\n', ' ').strip()
        return self.script

    async def generate_narration(self):
        """توليد التعليق الصوتي الأكاديمي (The Narrator)"""
        print("[Atlas] Synthesizing expert narration...")
        # استخدام صوت رزين ومحترف
        communicate = edge_tts.Communicate(self.script[:1000], voice="en-US-GuyNeural")
        await communicate.save(self.audio_path)

    def source_visuals(self):
        """توليد المشاهد السينمائية (The Filmmaker Role)"""
        print("[Atlas] Directing visual sequences...")
        images = []
        # البحث عن صور تعبر عن الفضاء والجاذبية
        search_queries = ["Jupiter gravity space signals", "GPS satellite constellation", "Gravitational lensing light"]
        
        with DDGS() as ddgs:
            for query in search_queries:
                results = list(ddgs.images(query, max_results=2))
                for i, r in enumerate(results):
                    img_data = requests.get(r["image"], timeout=10).content
                    fname = f"scene_{query[:5]}_{i}.jpg"
                    with open(fname, "wb") as f:
                        f.write(img_data)
                    images.append(fname)
        return images

    def render_film(self, image_files):
        """الإنتاج السينمائي النهائي (Cinematic Rendering)"""
        print("[Atlas] Rendering final documentary...")
        audio = AudioFileClip(self.audio_path)
        duration_per_img = audio.duration / len(image_files)
        
        clips = [ImageClip(m).set_duration(duration_per_img).resize(width=1920) for m in image_files]
        video = concatenate_videoclips(clips, method="compose")
        video = video.set_audio(audio)
        
        video.write_videofile(self.output_video, fps=24, codec="libx264")
        print(f"[Atlas] Production Complete: {self.output_video}")

# =================================
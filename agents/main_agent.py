from agents.base_agent import BaseAgent
from modules.llm_manager import LLMManager
from modules.memory_manager import MemoryManager
from modules.task_sequencer import TaskSequencer
from modules.calendar_handler import CalendarHandler
from modules.system_monitor import SystemMonitor
from modules.multimedia_processor import MultimediaProcessor
from modules.self_reflection import SelfReflection
from modules.security_handler import SecurityHandler
from modules.file_manager import FileManager # جديد
from utils.helper_functions import read_file_content
from config import HELP_FILE, SUPPORTED_LANGUAGES, DEFAULT_SCAN_PATH
import datetime
import re

class MainAgent(BaseAgent):
    def __init__(self, language="ar"):
        super().__init__(name="MainAgent")
        self.llm_manager = LLMManager()
        self.memory_manager = MemoryManager()
        self.task_sequencer = TaskSequencer(self)
        self.calendar_handler = CalendarHandler()
        self.system_monitor = SystemMonitor()
        self.multimedia_processor = MultimediaProcessor()
        self.self_reflection = SelfReflection(self.llm_manager, self.memory_manager)
        self.security_handler = SecurityHandler()
        self.file_manager = FileManager() # جديد
        self.current_language = language
        self._load_help_content()

    def _load_help_content(self):
        """Loads help content from markdown file."""
        self.help_content = read_file_content(HELP_FILE)

    def set_language(self, lang):
        """Sets the current language for responses."""
        if lang in SUPPORTED_LANGUAGES:
            self.current_language = lang
            self.add_log(f"Language set to: {lang}")
            return f"تم تغيير اللغة إلى {lang}." if lang == "ar" else f"Language set to {lang}."
        else:
            return f"اللغة {lang} غير مدعومة." if self.current_language == "ar" else f"Language {lang} not supported."

    def _get_system_info_prompt(self):
        """Provides a prompt snippet for the LLM to understand available tools."""
        info = f"""
        You are a smart local agent. You have access to several tools.
        Current time: {self.get_current_time()}
        
        Available Tools:
        - Get System Summary: `get_system_summary()` - Returns CPU, RAM, and Disk usage.
        - Add Calendar Event: `add_event(date_str, time_str, description)` - e.g., `add_event("2025-08-01", "10:00", "Meeting")`
        - Get Events for Day: `get_events_for_day(date_str)` - e.g., `get_events_for_day("2025-08-01")`
        - Get Upcoming Events: `get_upcoming_events(days)` - e.g., `get_upcoming_events(7)`
        - Read PDF: `read_pdf(filepath)` - Reads text from a PDF file. Provide full path.
        - Analyze Image (OCR): `analyze_image_ocr(filepath)` - Extracts text from an image. Provide full path.
        - Plan and Execute: `plan_and_execute(objective)` - Breaks down an objective into steps and executes them.
        - Self-Reflect: `reflect_on_performance(last_interaction, feedback)` - Analyze performance.
        - Analyze Error: `analyze_error(error_message, context)` - Analyze an error.
        - Security Check: `security_check()` - Runs a comprehensive security check.
        - Integrity Check: `integrity_check()` - Checks integrity of project files.
        - Scan Suspicious Files: `scan_suspicious_files()` - Scans common directories for suspicious files.
        - Create Integrity Baseline: `create_integrity_baseline()` - Generates file checksums for later checks.
        - Find File: `find_file(filename, search_path)` - e.g., `find_file("report.pdf", "C:/Users/Documents")`
        - Organize Files: `organize_files(directory_path)` - e.g., `organize_files("C:/Users/Downloads")`
        - Compress Folder: `compress_folder(folder_path)` - e.g., `compress_folder("C:/Users/Photos")`
        - Decompress File: `decompress_file(file_path)` - e.g., `decompress_file("C:/Users/archive.zip")`
        - Get Help: `get_help()` - Displays internal help document.
        - Clear Memory: `clear_memory()` - Clears conversation history.
        - Set Language: `set_language(lang_code)` - e.g., `set_language('ar')` or `set_language('en')`.

        Respond directly in the specified language ({self.current_language}).
        If a user asks for information that requires using a tool, respond with the appropriate tool call.
        If you are unsure how to use a tool, ask for clarification or state you can't perform the action.
        """
        return info

    def get_current_time(self):
        """Returns the current date and time."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_help(self):
        """Returns the content of the help document."""
        return self.help_content

    def process_command(self, user_input):
        """Processes user input, using LLM and tools."""
        self.add_log(f"User Input: {user_input}")
        self.memory_manager.add_message("user", user_input)

        response = ""
        user_input_lower = user_input.lower()

        # ... (باقي الشروط السابقة) ...
        # قسم إدارة الملفات (جديد)
        if "ابحث عن ملف" in user_input_lower or "find file" in user_input_lower:
            match = re.search(r'(?:file|ملف)\s+([\'"]?)(.*?)\1(?:\s+(?:in|في)\s+([\'"]?)(.*?)\3)?', user_input)
            if match:
                filename = match.group(2)
                search_path = match.group(4) if match.group(4) else DEFAULT_SCAN_PATH
                response = self.file_manager.find_file(filename, search_path)
            else:
                response = "Please provide a filename to search for." if self.current_language == "en" else "الرجاء توفير اسم الملف للبحث عنه."
        elif "تنظيم الملفات" in user_input_lower or "organize files" in user_input_lower:
            path_match = re.search(r'(?:تنظيم الملفات|organize files)\s+([\'"]?)(.*?)\1', user_input)
            dir_path = path_match.group(2) if path_match else None
            response = self.file_manager.organize_files(dir_path)
        elif "ضغط مجلد" in user_input_lower or "compress folder" in user_input_lower:
            path_match = re.search(r'(?:ضغط مجلد|compress folder)\s+([\'"]?)(.*?)\1', user_input)
            if path_match:
                folder_path = path_match.group(2)
                response = self.file_manager.compress_folder(folder_path)
            else:
                response = "Please provide the folder path to compress." if self.current_language == "en" else "الرجاء توفير مسار المجلد للضغط."
        elif "فك ضغط ملف" in user_input_lower or "decompress file" in user_input_lower:
            path_match = re.search(r'(?:فك ضغط ملف|decompress file)\s+([\'"]?)(.*?)\1', user_input)
            if path_match:
                file_path = path_match.group(2)
                response = self.file_manager.decompress_file(file_path)
            else:
                response = "Please provide the path to the zip file." if self.current_language == "en" else "الرجاء توفير مسار ملف ZIP."
        elif "مراقبة النظام" in user_input_lower or "system summary" in user_input_lower:
            response = self.system_monitor.get_system_summary()
        elif "إضافة حدث" in user_input_lower or "add event" in user_input_lower:
            parts = user_input_lower.split()
            if len(parts) >= 5:
                try:
                    date_str = parts[parts.index("event") + 1 if "event" in parts else parts.index("حدث") + 1]
                    time_str = parts[parts.index("event") + 2 if "event" in parts else parts.index("حدث") + 2]
                    description_start_index = parts.index(time_str) + 1
                    description = " ".join(parts[description_start_index:])
                    response = self.calendar_handler.add_event(date_str, time_str, description)
                except (ValueError, IndexError):
                    response = "Please provide date (YYYY-MM-DD), time (HH:MM), and description for the event." if self.current_language == "en" else "الرجاء توفير التاريخ (YYYY-MM-DD)، الوقت (HH:MM)، والوصف للحدث."
            else:
                response = "Please provide date (YYYY-MM-DD), time (HH:MM), and description for the event." if self.current_language == "en" else "الرجاء توفير التاريخ (YYYY-MM-DD)، الوقت (HH:MM)، والوصف للحدث."
        elif "أحداث اليوم" in user_input_lower or "events for today" in user_input_lower:
            today_str = datetime.date.today().strftime("%Y-%m-%d")
            response = self.calendar_handler.get_events_for_day(today_str)
        elif "أحداث قادمة" in user_input_lower or "upcoming events" in user_input_lower:
            try:
                days_idx = user_input_lower.find("upcoming events")
                if days_idx == -1: days_idx = user_input_lower.find("أحداث قادمة")
                days_str = user_input_lower[days_idx:].split()
                days = 7
                for ds in days_str:
                    try:
                        d = int(ds)
                        days = d
                        break
                    except ValueError:
                        pass
                response = self.calendar_handler.get_upcoming_events(days=days)
            except Exception:
                response = self.calendar_handler.get_upcoming_events()
        elif "قراءة pdf" in user_input_lower or "read pdf" in user_input_lower:
            path_start_idx = user_input_lower.find("pdf ") + 4
            if path_start_idx > 3:
                filepath = user_input[path_start_idx:].strip()
                response = self.multimedia_processor.read_pdf(filepath)
            else:
                response = "Please provide the full path to the PDF file." if self.current_language == "en" else "الرجاء توفير المسار الكامل لملف PDF."
        elif "تحليل صورة" in user_input_lower or "analyze image" in user_input_lower or "ocr" in user_input_lower:
            path_start_idx = -1
            if "analyze image " in user_input_lower:
                path_start_idx = user_input_lower.find("analyze image ") + len("analyze image ")
            elif "تحليل صورة " in user_input_lower:
                path_start_idx = user_input_lower.find("تحليل صورة ") + len("تحليل صورة ")
            elif "ocr " in user_input_lower:
                path_start_idx = user_input_lower.find("ocr ") + len("ocr ")
            if path_start_idx > -1:
                filepath = user_input[path_start_idx:].strip()
                response = self.multimedia_processor.analyze_image_ocr(filepath)
            else:
                response = "Please provide the full path to the image file for OCR." if self.current_language == "en" else "الرجاء توفير المسار الكامل لملف الصورة لتحليل OCR."
        elif "ساعدني" in user_input_lower or "help me" in user_input_lower or "get help" in user_input_lower:
            response = self.get_help()
        elif "مسح الذاكرة" in user_input_lower or "clear memory" in user_input_lower:
            self.memory_manager.clear_memory()
            response = "Conversation memory cleared." if self.current_language == "en" else "تم مسح ذاكرة المحادثة."
        elif "تغيير اللغة" in user_input_lower or "set language" in user_input_lower:
            lang_code_idx = user_input_lower.find("language") + len("language") if "language" in user_input_lower else user_input_lower.find("اللغة") + len("اللغة")
            lang_code = user_input[lang_code_idx:].strip().split()[0] if user_input[lang_code_idx:].strip() else ""
            response = self.set_language(lang_code)
        elif "فكر" in user_input_lower and ("أدائي" in user_input_lower or "reflect on performance" in user_input_lower):
            feedback_start = user_input_lower.find("أدائي:") + len("أدائي:") if "أدائي:" in user_input_lower else user_input_lower.find("performance:") + len("performance:")
            feedback = user_input[feedback_start:].strip() if feedback_start > -1 else ""
            last_assistant_response = ""
            history = self.memory_manager.get_history()
            for msg in reversed(history):
                if msg["role"] == "assistant":
                    last_assistant_response = msg["content"]
                    break
            response = self.self_reflection.reflect_on_performance(last_assistant_response, feedback)
        elif "حل خطأ" in user_input_lower or "analyze error" in user_input_lower:
            error_msg_start = user_input_lower.find("خطأ:") + len("خطأ:") if "خطأ:" in user_input_lower else user_input_lower.find("error:") + len("error:")
            error_msg = user_input[error_msg_start:].strip() if error_msg_start > -1 else ""
            context_start = user_input_lower.find("السياق:") + len("السياق:") if "السياق:" in user_input_lower else user_input_lower.find("context:") + len("context:")
            context = user_input[context_start:].strip() if context_start > -1 else ""
            response = self.self_reflection.analyze_error(error_msg, context)
        elif "خطط ونفذ" in user_input_lower or "plan and execute" in user_input_lower:
            objective_start = user_input_lower.find("خطط ونفذ") + len("خطط ونفذ") if "خطط ونفذ" in user_input_lower else user_input_lower.find("plan and execute") + len("plan and execute")
            objective = user_input[objective_start:].strip()
            if objective:
                sequence_results = self.task_sequencer.plan_and_execute(objective)
                response = "Task sequence completed. Results:\n" + "\n".join(sequence_results) if self.current_language == "en" else "تم إكمال تسلسل المهام. النتائج:\n" + "\n".join(sequence_results)
            else:
                response = "Please provide an objective to plan and execute." if self.current_language == "en" else "الرجاء توفير هدف للتخطيط والتنفيذ."
        elif "فحص الأمان" in user_input_lower or "security check" in user_input_lower:
            response = self.security_handler.run_full_security_check()
        elif "فحص سلامة" in user_input_lower or "integrity check" in user_input_lower:
            response = self.security_handler.run_integrity_check()
        elif "فحص الملفات المشبوهة" in user_input_lower or "scan for suspicious files" in user_input_lower:
            response = self.security_handler.scan_for_suspicious_files()
        elif "إنشاء قاعدة سلامة" in user_input_lower or "create integrity baseline" in user_input_lower:
            response = self.security_handler.create_integrity_baseline()
        else:
            history_for_llm = self.memory_manager.get_history()
            system_message_content = self._get_system_info_prompt()
            llm_messages = [{"role": "system", "content": system_message_content}] + history_for_llm
            llm_messages.append({"role": "user", "content": user_input})
            self.add_log(f"Sending to LLM: {user_input}")
            response = self.llm_manager.generate_response(user_input, history_for_llm)

        self.add_log(f"Agent Response: {response}")
        self.memory_manager.add_message("assistant", response)
        return response
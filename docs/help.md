# Local Smart Agent User Guide

Welcome to the Local Smart Agent! I'm an AI agent that runs on your device without an internet connection. I can help you with various tasks.

# Available Commands:

* **System Monitor / system summary**: To get information about CPU, RAM, and hard disk space usage.
* Example: `system monitor` or `system summary`

* **Calendar**:
* **Add event `<YYYY-MM-DD>` `<HH:MM>` `<description>`**: To add a new event to the calendar.
* Example: `Add event 2025-08-05 10:00 Team Meeting`
* Example (English): `add event 2025-08-05 10:00 Team Meeting`
* **Events for today**: To display today's events.
* **Upcoming events [number of days]**: Displays upcoming events for a specified number of days (default: 7 days).
* Example: `Upcoming events 3` (events for the next three days)
* Example (English): `Upcoming events 10`

* **Multimedia processing**:
* **Read pdf `<full_filepath>`: Reads text content from a PDF file.
* Example: `Read pdf C:\Users\YourUser\Documents\report.pdf`
* **Analyze image OCR `<full_filepath>`: Extracts text from an image using Optical Character Recognition (OCR) technology. * Example: `Analyze an OCR image from /Users/YourUser/Pictures/invoice.png`

* **Task Sequence**:
* **Plan and execute: <objective>**: To break down a complex goal into actionable steps and execute them.
* Example: `Plan and execute: Find the capital of France and then list its population.`

* **Introspection**:
* **Reflect on my performance: <your_feedback>**: To analyze the agent's performance and make suggestions for improvement.
* Example: `Reflect on my performance: You didn't understand my last question well.`
* **Resolve error: <error_message> [context: <error_context>] / analyze error: <error_message> [context: <error_context>]**: To analyze a specific error message.
* Example: `Resolved Error: FileNotFoundError Context: When trying to read a file`

* **Security and Privacy Module**:
* **Security Check**: Performs a basic security check of the system and proxy files.
* **Scan for Suspicious Files**: Scans for suspicious executable files in the Downloads folder.
* **Integrity Check**: Ensures that project files have not been tampered with.

* **File Management Module (New)**:
* **Find File `<filename>` [in `<directory_path>`]**: Searches for a specific file.
* Example: `Find file report.pdf` or `Find file photo.jpg in C:\Users\Documents`
* **Organize Files**: Sorts files into folders based on their type (such as images and videos).
* **Compress folder `<directory_path>`: Compresses a folder into a ZIP file.
* **Decompress file `<file_path>`: Decompress a ZIP file.

* **Memory and language management**:
* **Clear memory**: Clears previous chat history.
* **Change language [ar/en] / set language [ar/en]**: Change the agent language.
* Example: `change language en`

* **Help**:
* **Help me / get help**: View this guide.

## Important notes:

* **Paths**: When specifying file paths (PDF, images), make sure to use the full and exact path to the file on your system (e.g., `C:\path\to\file.pdf` on Windows or `/path/to/file.png` on macOS/Linux). * **Ollama**: Ensure that Ollama is installed and running, and that you have the Mistral 7B model loaded.
* **Tesseract OCR**: If you're using the OCR function, ensure that Tesseract-OCR is installed and the correct path is set in the `config.py` file.

Enjoy using your local smart agent!   

                           _________________________________________ar________________________________________________
# دليل استخدام الوكيل الذكي المحلي

مرحباً بك في الوكيل الذكي المحلي! أنا وكيل ذكاء اصطناعي يعمل على جهازك دون الحاجة للاتصال بالإنترنت. يمكنني مساعدتك في مهام مختلفة.

## الأوامر المتاحة:

* **مراقبة النظام / system summary**: للحصول على معلومات حول استخدام وحدة المعالجة المركزية (CPU)، الذاكرة العشوائية (RAM)، ومساحة القرص الصلب.
    * مثال: `مراقبة النظام` أو `system summary`

* **التقويم**:
    * **إضافة حدث / add event `<YYYY-MM-DD>` `<HH:MM>` `<الوصف>`**: لإضافة حدث جديد إلى التقويم.
        * مثال: `إضافة حدث 2025-08-05 10:00 اجتماع الفريق`
        * مثال (English): `add event 2025-08-05 10:00 Team Meeting`
    * **أحداث اليوم / events for today**: لعرض أحداث اليوم.
    * **أحداث قادمة / upcoming events [عدد الأيام]**: لعرض الأحداث القادمة لعدد محدد من الأيام (الافتراضي: 7 أيام).
        * مثال: `أحداث قادمة 3` (أحداث الأيام الثلاثة القادمة)
        * مثال (English): `upcoming events 10`

* **معالجة الوسائط المتعددة**:
    * **قراءة pdf `<مسار_الملف_الكامل>` / read pdf `<full_filepath>`**: لقراءة محتوى نصي من ملف PDF.
        * مثال: `قراءة pdf C:\Users\YourUser\Documents\report.pdf`
    * **تحليل صورة OCR `<مسار_الملف_الكامل>` / analyze image OCR `<full_filepath>`**: لاستخراج النص من صورة باستخدام تقنية التعرف الضوئي على الحروف (OCR).
        * مثال: `تحليل صورة OCR /Users/YourUser/Pictures/invoice.png`

* **تسلسل المهام**:
    * **خطط ونفذ: <الهدف> / plan and execute: <objective>**: لتقسيم هدف معقد إلى خطوات قابلة للتنفيذ وتنفذها.
        * مثال: `خطط ونفذ: ابحث عن عاصمة فرنسا ثم اذكر عدد سكانها.`

* **التفكير الذاتي**:
    * **فكر في أدائي: <ملاحظاتك> / reflect on performance: <your_feedback>**: لتحليل أداء الوكيل وتقديم اقتراحات للتحسين.
        * مثال: `فكر في أدائي: لم تفهم سؤالي الأخير بشكل جيد.`
    * **حل خطأ: <رسالة_الخطأ> [السياق: <سياق_الخطأ>] / analyze error: <error_message> [context: <error_context>]**: لتحليل رسالة خطأ معينة.
        * مثال: `حل خطأ: FileNotFoundError السياق: عندما حاولت قراءة ملف.`

* **وحدة الأمان والخصوصية**:
    * **فحص الأمان / security check**: لإجراء فحص أمني أساسي للنظام وملفات الوكيل.
    * **فحص الملفات المشبوهة / scan for suspicious files**: للبحث عن ملفات تنفيذية مشبوهة في مجلد التنزيلات.
    * **فحص سلامة ملفات المشروع / integrity check**: للتأكد من عدم العبث بملفات المشروع.

* **وحدة إدارة الملفات (جديد)**:
    * **البحث عن ملف `<اسم_الملف>` [في `<مسار_المجلد>`] / find file `<filename>` [in `<directory_path>`]**: للبحث عن ملف معين.
        * مثال: `ابحث عن ملف report.pdf` أو `find file photo.jpg in C:\Users\Documents`
    * **تنظيم الملفات / organize files**: لفرز الملفات في مجلدات بناءً على نوعها (مثل الصور والفيديوهات).
    * **ضغط مجلد `<مسار_المجلد>` / compress folder `<directory_path>`**: لضغط مجلد في ملف ZIP.
    * **فك ضغط ملف `<مسار_الملف>` / decompress file `<file_path>`**: لفك ضغط ملف ZIP.

* **إدارة الذاكرة واللغة**:
    * **مسح الذاكرة / clear memory**: لمسح سجل المحادثات السابق.
    * **تغيير اللغة [ar/en] / set language [ar/en]**: لتغيير لغة الوكيل.
        * مثال: `تغيير اللغة en`

* **مساعدة**:
    * **ساعدني / help me / get help**: لعرض هذا الدليل.

## ملاحظات مهمة:

* **المسارات**: عند تحديد مسارات الملفات (PDF، صور)، تأكد من استخدام المسار الكامل والدقيق للملف على نظامك (مثل `C:\path\to\file.pdf` على Windows أو `/path/to/file.png` على macOS/Linux).
* **Ollama**: تأكد من أن Ollama مثبت ويعمل، وأن نموذج Mistral 7B محمل لديك.
* **Tesseract OCR**: إذا كنت تستخدم وظيفة OCR، فتأكد من تثبيت Tesseract-OCR وتكوين المسار الصحيح له في ملف `config.py`.

استمتع باستخدام الوكيل الذكي المحلي!

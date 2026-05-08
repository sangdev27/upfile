import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
import pyautogui
import threading
import pyperclip
import sys
import html
import re

class HTMLTypingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Sang Dev - Trình Gõ HTML Chuẩn")
        self.root.geometry("850x650")
        self.root.resizable(True, True)
        
        # Theme
        self.root.configure(bg="#0a0a0a")
        
        # Variables
        self.text_to_type = ""
        self.typing_speed = 0.015  # Tốc độ ổn định
        self.is_typing = False
        self.is_paused = False
        
        # Colors
        self.bg_color = "#0a0a0a"
        self.card_bg = "#1a1a1a"
        self.accent_color = "#00ccff"
        self.primary_color = "#ff3366"
        self.text_color = "#ffffff"
        self.secondary_text = "#888888"
        
        self.check_libraries()
        self.setup_ui()
        
    def check_libraries(self):
        """Kiểm tra thư viện"""
        missing_libs = []
        
        try:
            import pyautogui
        except ImportError:
            missing_libs.append("pyautogui")
            
        try:
            import pyperclip
        except ImportError:
            missing_libs.append("pyperclip")
            
        if missing_libs:
            libs_str = ", ".join(missing_libs)
            messagebox.showwarning("Thiếu thư viện", 
                                  f"Cần cài đặt: {libs_str}\n\n"
                                  "pip install {libs_str}")
            self.root.destroy()
            sys.exit()
    
    def decode_html_entities(self, text):
        """Decode HTML entities với xử lý đặc biệt"""
        try:
            # Danh sách HTML entities thường gặp
            html_entities = {
                '&lt;': '<',
                '&gt;': '>',
                '&amp;': '&',
                '&quot;': '"',
                '&#39;': "'",
                '&nbsp;': ' ',
                '&copy;': '©',
                '&reg;': '®',
                '&trade;': '™',
                '&euro;': '€',
                '&pound;': '£',
                '&yen;': '¥',
                '&cent;': '¢',
                '&sect;': '§',
                '&para;': '¶',
            }
            
            # Thêm numeric entities
            for i in range(32, 256):
                html_entities[f'&#{i};'] = chr(i)
                html_entities[f'&#x{hex(i)[2:]};'] = chr(i)
            
            # Replace từng entity
            for entity, char in html_entities.items():
                text = text.replace(entity, char)
            
            # Dùng html.unescape cho các entity khác
            text = html.unescape(text)
            
            return text
        except Exception as e:
            print(f"Lỗi decode HTML: {e}")
            return text
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill=tk.X, padx=25, pady=(20, 15))
        
        logo_frame = tk.Frame(header_frame, bg=self.bg_color)
        logo_frame.pack(side=tk.LEFT)
        
        logo_label = tk.Label(logo_frame, 
                             text="🌐</> SANG DEV HTML", 
                             font=("Consolas", 26, "bold"), 
                             fg=self.primary_color, 
                             bg=self.bg_color)
        logo_label.pack()
        
        subtitle_label = tk.Label(logo_frame, 
                                 text="Trình Gõ HTML Entities Chuẩn", 
                                 font=("Segoe UI", 11), 
                                 fg=self.secondary_text, 
                                 bg=self.bg_color)
        subtitle_label.pack(pady=(5, 0))
        
        # HTML Info
        html_info = tk.Label(header_frame, 
                           text="📋 HỖ TRỢ:\n&lt; &gt; &amp; &quot; &#39;\nvà 100+ entities khác", 
                           font=("Segoe UI", 9), 
                           fg=self.accent_color, 
                           bg=self.bg_color,
                           justify=tk.RIGHT)
        html_info.pack(side=tk.RIGHT)
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 20))
        
        main_card = tk.Frame(main_container, bg=self.card_bg, relief=tk.FLAT, bd=1)
        main_card.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Text input
        left_column = tk.Frame(main_card, bg=self.card_bg)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        text_frame = tk.LabelFrame(left_column, text="📝 NHẬP VĂN BẢN/HTML", 
                                   font=("Segoe UI", 11, "bold"), 
                                   fg=self.text_color, bg=self.card_bg,
                                   relief=tk.FLAT, bd=1)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.text_input = tk.Text(text_frame, height=15, 
                                  font=("Consolas", 11), 
                                  wrap=tk.WORD, relief=tk.FLAT, 
                                  bg="#111111", fg=self.text_color,
                                  insertbackground=self.primary_color)
        self.text_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_scrollbar = tk.Scrollbar(text_frame, command=self.text_input.yview,
                                     bg=self.card_bg, troughcolor=self.accent_color)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_input.config(yscrollcommand=text_scrollbar.set)
        
        # Example HTML
        example_frame = tk.Frame(left_column, bg=self.card_bg)
        example_frame.pack(fill=tk.X, pady=(0, 10))
        
        example_btn = tk.Button(example_frame, text="📋 THÊM VÍ DỤ HTML", 
                               command=self.add_html_example,
                               bg="#333333", fg=self.accent_color,
                               font=("Segoe UI", 9), relief=tk.FLAT,
                               cursor="hand2")
        example_btn.pack(side=tk.LEFT)
        
        self.file_label = tk.Label(example_frame, text="Chưa chọn file", 
                                  font=("Segoe UI", 9), fg=self.secondary_text, 
                                  bg=self.card_bg)
        self.file_label.pack(side=tk.RIGHT)
        
        # Right column - Controls
        right_column = tk.Frame(main_card, bg=self.card_bg, width=320)
        right_column.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 15), pady=15)
        right_column.pack_propagate(False)
        
        # Control panel
        control_panel = tk.LabelFrame(right_column, text="⚙️ CÀI ĐẶT", 
                                     font=("Segoe UI", 11, "bold"), 
                                     fg=self.text_color, bg=self.card_bg,
                                     relief=tk.FLAT, bd=1)
        control_panel.pack(fill=tk.BOTH, expand=True)
        
        # File button
        file_button = tk.Button(control_panel, text="📁 CHỌN FILE .TXT/.HTML", 
                               command=self.load_text_file, 
                               bg=self.accent_color, fg="#000000",
                               font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                               activebackground="#33ddff", 
                               cursor="hand2", height=2)
        file_button.pack(fill=tk.X, padx=15, pady=(20, 10))
        self.file_button = file_button
        
        # HTML Decode options
        html_frame = tk.Frame(control_panel, bg=self.card_bg)
        html_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        html_label = tk.Label(html_frame, text="🌐 XỬ LÝ HTML:", 
                             font=("Segoe UI", 10), fg=self.text_color, 
                             bg=self.card_bg)
        html_label.pack(anchor=tk.W)
        
        self.decode_mode = tk.StringVar(value="auto")
        
        decode_auto = tk.Radiobutton(html_frame, text="AUTO: Tự động phát hiện & decode", 
                                    variable=self.decode_mode, value="auto",
                                    bg=self.card_bg, fg=self.text_color,
                                    selectcolor=self.card_bg,
                                    activebackground=self.card_bg,
                                    activeforeground=self.accent_color,
                                    font=("Segoe UI", 9))
        decode_auto.pack(anchor=tk.W, pady=(5, 0))
        
        decode_force = tk.Radiobutton(html_frame, text="FORCE: Luôn decode HTML entities", 
                                     variable=self.decode_mode, value="force",
                                     bg=self.card_bg, fg=self.text_color,
                                     selectcolor=self.card_bg,
                                     activebackground=self.card_bg,
                                     activeforeground=self.accent_color,
                                     font=("Segoe UI", 9))
        decode_force.pack(anchor=tk.W, pady=(5, 0))
        
        decode_none = tk.Radiobutton(html_frame, text="NONE: Giữ nguyên (không decode)", 
                                    variable=self.decode_mode, value="none",
                                    bg=self.card_bg, fg=self.text_color,
                                    selectcolor=self.card_bg,
                                    activebackground=self.card_bg,
                                    activeforeground=self.primary_color,
                                    font=("Segoe UI", 9))
        decode_none.pack(anchor=tk.W, pady=(5, 0))
        
        # Typing method
        method_frame = tk.Frame(control_panel, bg=self.card_bg)
        method_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        method_label = tk.Label(method_frame, text="🔧 PHƯƠNG PHÁP:", 
                               font=("Segoe UI", 10), fg=self.text_color, 
                               bg=self.card_bg)
        method_label.pack(anchor=tk.W)
        
        self.method_var = tk.StringVar(value="smart")
        
        method_smart = tk.Radiobutton(method_frame, text="SMART: Tự động chọn phương pháp", 
                                     variable=self.method_var, value="smart",
                                     bg=self.card_bg, fg=self.text_color,
                                     selectcolor=self.card_bg,
                                     activebackground=self.card_bg,
                                     activeforeground=self.accent_color,
                                     font=("Segoe UI", 9))
        method_smart.pack(anchor=tk.W, pady=(5, 0))
        
        method_clipboard = tk.Radiobutton(method_frame, text="CLIPBOARD: Copy-paste (chuẩn 100%)", 
                                         variable=self.method_var, value="clipboard",
                                         bg=self.card_bg, fg=self.text_color,
                                         selectcolor=self.card_bg,
                                         activebackground=self.card_bg,
                                         activeforeground=self.accent_color,
                                         font=("Segoe UI", 9))
        method_clipboard.pack(anchor=tk.W, pady=(5, 0))
        
        # Speed control
        speed_frame = tk.Frame(control_panel, bg=self.card_bg)
        speed_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        speed_label = tk.Label(speed_frame, text="⚡ TỐC ĐỘ (giây/ký tự):", 
                              font=("Segoe UI", 10), fg=self.text_color, 
                              bg=self.card_bg)
        speed_label.pack(anchor=tk.W)
        
        speed_input_frame = tk.Frame(speed_frame, bg=self.card_bg)
        speed_input_frame.pack(fill=tk.X, pady=(8, 0))
        
        # Scale
        self.speed_scale = tk.Scale(speed_input_frame, from_=0.005, to=0.1, 
                                   resolution=0.001, orient=tk.HORIZONTAL,
                                   length=200, command=self.update_speed_from_slider,
                                   bg=self.card_bg, fg=self.text_color,
                                   troughcolor=self.accent_color,
                                   highlightbackground=self.card_bg,
                                   sliderrelief=tk.FLAT,
                                   activebackground=self.primary_color,
                                   showvalue=0)
        self.speed_scale.set(0.015)
        self.speed_scale.pack(side=tk.LEFT)
        
        # Entry
        self.speed_var = tk.StringVar(value="0.015")
        speed_entry = tk.Entry(speed_input_frame, 
                              textvariable=self.speed_var,
                              width=8, font=("Consolas", 11),
                              bg="#111111", fg=self.primary_color,
                              relief=tk.FLAT, insertbackground=self.primary_color,
                              justify=tk.CENTER)
        speed_entry.pack(side=tk.LEFT, padx=(10, 0))
        speed_entry.bind("<Return>", self.update_speed_from_entry)
        speed_entry.bind("<FocusOut>", self.update_speed_from_entry)
        self.speed_entry = speed_entry
        
        speed_note = tk.Label(speed_frame, 
                             text="0.015s = ổn định nhất\n0.005s = nhanh (thử nghiệm)", 
                             font=("Segoe UI", 8), fg=self.secondary_text, 
                             bg=self.card_bg)
        speed_note.pack(anchor=tk.W, pady=(5, 0))
        
        # Countdown
        countdown_frame = tk.Frame(control_panel, bg=self.card_bg)
        countdown_frame.pack(fill=tk.X, padx=15, pady=(0, 20))
        
        countdown_label = tk.Label(countdown_frame, text="⏱️ ĐẾM NGƯỢC (giây):", 
                                  font=("Segoe UI", 10), fg=self.text_color, 
                                  bg=self.card_bg)
        countdown_label.pack(anchor=tk.W)
        
        self.countdown_var = tk.StringVar(value="2")
        countdown_entry = tk.Entry(countdown_frame, 
                                  textvariable=self.countdown_var,
                                  width=10, font=("Consolas", 11),
                                  bg="#111111", fg=self.accent_color,
                                  relief=tk.FLAT, insertbackground=self.accent_color,
                                  justify=tk.CENTER)
        countdown_entry.pack(fill=tk.X, pady=(8, 0))
        
        # Control buttons
        button_frame = tk.Frame(control_panel, bg=self.card_bg)
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 20))
        
        # Start button
        self.start_button = tk.Button(button_frame, text="🚀 BẮT ĐẦU GÕ", 
                                     command=self.start_typing, 
                                     bg=self.primary_color, fg="#000000",
                                     font=("Segoe UI", 12, "bold"), 
                                     relief=tk.FLAT, height=2,
                                     activebackground="#ff6699",
                                     cursor="hand2")
        self.start_button.pack(fill=tk.X, pady=(0, 10))
        
        # Pause button
        self.pause_button = tk.Button(button_frame, text="⏸️ TẠM DỪNG", 
                                     command=self.toggle_pause, 
                                     bg="#ff9900", fg="#000000",
                                     font=("Segoe UI", 11, "bold"), 
                                     relief=tk.FLAT, height=2,
                                     activebackground="#ffcc00",
                                     cursor="hand2")
        self.pause_button.pack(fill=tk.X, pady=(0, 10))
        self.pause_button.config(state=tk.DISABLED)
        
        # Stop button
        self.stop_button = tk.Button(button_frame, text="🛑 DỪNG HẲN", 
                                    command=self.stop_typing, 
                                    bg="#ff3333", fg="#000000",
                                    font=("Segoe UI", 11, "bold"), 
                                     relief=tk.FLAT, height=2,
                                     activebackground="#ff6666",
                                     cursor="hand2")
        self.stop_button.pack(fill=tk.X)
        self.stop_button.config(state=tk.DISABLED)
        
        # Status panel
        status_panel = tk.LabelFrame(right_column, text="📊 TRẠNG THÁI", 
                                    font=("Segoe UI", 11, "bold"), 
                                    fg=self.text_color, bg=self.card_bg,
                                    relief=tk.FLAT, bd=1)
        status_panel.pack(fill=tk.X, pady=(15, 0))
        
        self.status_label = tk.Label(status_panel, 
                                    text="✅ SẴN SÀNG\nNhập HTML/text → Chọn chế độ → BẮT ĐẦU", 
                                    font=("Segoe UI", 10), fg=self.text_color, 
                                    bg=self.card_bg, wraplength=280, 
                                    justify=tk.LEFT, padx=15, pady=15)
        self.status_label.pack()
        
        self.progress_label = tk.Label(status_panel, 
                                      text="Tiến độ: 0% | Chế độ: AUTO", 
                                      font=("Segoe UI", 9), fg=self.accent_color, 
                                      bg=self.card_bg)
        self.progress_label.pack(pady=(0, 15))
        
        # Preview panel
        preview_panel = tk.LabelFrame(left_column, text="👁️ XEM TRƯỚC (HTML → Text)", 
                                     font=("Segoe UI", 11, "bold"), 
                                     fg=self.text_color, bg=self.card_bg,
                                     relief=tk.FLAT, bd=1)
        preview_panel.pack(fill=tk.X, pady=(10, 0))
        
        self.preview_label = tk.Label(preview_panel, 
                                     text="Chưa có nội dung để xem trước\nNhập HTML entities để thử nghiệm", 
                                     font=("Segoe UI", 10), fg=self.secondary_text, 
                                     bg=self.card_bg, wraplength=450, 
                                     justify=tk.LEFT, padx=15, pady=15)
        self.preview_label.pack(anchor=tk.W)
        
        preview_btn = tk.Button(preview_panel, text="🔄 CẬP NHẬT XEM TRƯỚC", 
                               command=self.update_preview,
                               bg="#333333", fg=self.accent_color,
                               font=("Segoe UI", 9), relief=tk.FLAT,
                               cursor="hand2")
        preview_btn.pack(pady=(0, 15))
        
        # Footer
        footer_frame = tk.Frame(self.root, bg=self.bg_color)
        footer_frame.pack(fill=tk.X, padx=25, pady=(0, 15))
        
        html_examples = tk.Label(footer_frame, 
                                text="💡 Ví dụ HTML: &lt;div&gt; → <div> | &amp;copy; → © | &quot;text&quot; → \"text\" | &#39;apos&#39; → 'apos'", 
                                font=("Segoe UI", 9), fg=self.secondary_text, 
                                bg=self.bg_color, wraplength=800)
        html_examples.pack()
        
        copyright_label = tk.Label(footer_frame, 
                                  text="© 2024 Sang Dev - Xử lý HTML entities chuẩn", 
                                  font=("Segoe UI", 8), fg="#666666", 
                                  bg=self.bg_color)
        copyright_label.pack(pady=(5, 0))
        
        # Bind events
        self.text_input.bind("<KeyRelease>", self.on_text_change)
        
    def on_text_change(self, event=None):
        """Khi văn bản thay đổi"""
        text = self.text_input.get(1.0, tk.END).strip()
        char_count = len(text)
        
        # Kiểm tra có HTML entities không
        has_html = any(entity in text for entity in ['&lt;', '&gt;', '&amp;', '&quot;', '&#'])
        
        if has_html:
            decoded = self.decode_html_entities(text)
            self.preview_label.config(
                text=f"HTML Entities phát hiện:\n{text[:100]}...\n↓\n{decoded[:100]}...",
                fg=self.accent_color
            )
    
    def add_html_example(self):
        """Thêm ví dụ HTML"""
        example = '''<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>HTML Entities Test</h1>
    <p>&lt;div&gt; tags: &lt;p&gt;paragraph&lt;/p&gt;&lt;/div&gt;</p>
    <p>Special chars: &amp; (and), &quot;quotes&quot;, &#39;apostrophe&#39;</p>
    <p>Copyright: &copy; 2024, Registered: &reg;, Trade: &trade;</p>
    <p>Currency: &euro;100, &pound;50, &yen;1000</p>
    <p>Spaces: Hello&nbsp;&nbsp;&nbsp;World</p>
</body>
</html>'''
        
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(1.0, example)
        self.update_preview()
    
    def update_preview(self):
        """Cập nhật xem trước"""
        text = self.text_input.get(1.0, tk.END).strip()
        decoded = self.decode_html_entities(text)
        
        if len(text) > 200:
            preview_text = f"Input: {text[:200]}...\n\nOutput: {decoded[:200]}..."
        else:
            preview_text = f"Input: {text}\n\nOutput: {decoded}"
        
        self.preview_label.config(text=preview_text, fg=self.text_color)
    
    def update_speed_from_slider(self, value):
        """Cập nhật tốc độ từ slider"""
        try:
            speed = float(value)
            self.typing_speed = speed
            self.speed_var.set(f"{speed:.3f}")
        except:
            pass
    
    def update_speed_from_entry(self, event=None):
        """Cập nhật tốc độ từ entry"""
        try:
            speed = float(self.speed_var.get())
            if speed < 0.005:
                speed = 0.005
                self.speed_var.set("0.005")
            elif speed > 0.1:
                speed = 0.1
                self.speed_var.set("0.100")
            
            self.typing_speed = speed
            self.speed_scale.set(speed)
        except ValueError:
            messagebox.showerror("Lỗi", "Nhập số từ 0.005 đến 0.1")
            self.speed_var.set(f"{self.typing_speed:.3f}")
    
    def load_text_file(self):
        """Tải file"""
        file_path = filedialog.askopenfilename(
            title="Chọn file",
            filetypes=[("Text files", "*.txt"), ("HTML files", "*.html"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_input.delete(1.0, tk.END)
                    self.text_input.insert(1.0, content)
                    
                    filename = file_path.split('/')[-1]
                    if len(filename) > 20:
                        filename = filename[:17] + "..."
                    self.file_label.config(text=f"📄 {filename}")
                    self.update_preview()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
    
    def type_character_smart(self, char):
        """Gõ ký tự thông minh"""
        try:
            # ASCII printable characters
            if 32 <= ord(char) <= 126:
                pyautogui.write(char, interval=0)
                time.sleep(0.005)
            else:
                # Unicode characters - use clipboard
                pyperclip.copy(char)
                time.sleep(0.01)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.02)
        except:
            # Fallback
            try:
                pyautogui.write(char, interval=0)
            except:
                pass
    
    def type_character_clipboard(self, char):
        """Gõ ký tự bằng clipboard (chuẩn nhất)"""
        try:
            pyperclip.copy(char)
            time.sleep(0.015)  # Chờ copy
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.025)  # Chờ paste
        except:
            try:
                pyautogui.write(char, interval=0)
            except:
                pass
    
    def start_typing(self):
        """Bắt đầu gõ"""
        if self.is_typing:
            return
        
        raw_text = self.text_input.get(1.0, tk.END).strip()
        
        if not raw_text:
            messagebox.showwarning("Cảnh báo", "Nhập nội dung trước!")
            return
        
        # Xử lý HTML theo chế độ
        decode_mode = self.decode_mode.get()
        
        if decode_mode == "force":
            processed_text = self.decode_html_entities(raw_text)
            decode_status = "Đã decode HTML"
        elif decode_mode == "auto":
            # Tự động phát hiện HTML entities
            has_html = any(entity in raw_text for entity in ['&lt;', '&gt;', '&amp;', '&quot;', '&#'])
            if has_html:
                processed_text = self.decode_html_entities(raw_text)
                decode_status = "Auto-detect: Đã decode HTML"
            else:
                processed_text = raw_text
                decode_status = "Auto-detect: Không decode"
        else:  # none
            processed_text = raw_text
            decode_status = "Không decode HTML"
        
        self.text_to_type = processed_text
        
        try:
            countdown = int(self.countdown_var.get())
        except:
            countdown = 2
        
        # Update UI
        self.start_button.config(state=tk.DISABLED, bg="#555555", text="⏳ CHUẨN BỊ...")
        self.file_button.config(state=tk.DISABLED, bg="#555555")
        self.pause_button.config(state=tk.NORMAL, bg="#ff9900")
        self.stop_button.config(state=tk.NORMAL, bg="#ff3333")
        
        self.status_label.config(text=f"📋 {decode_status}\nKý tự: {len(raw_text)} → {len(processed_text)}")
        
        # Start in thread
        threading.Thread(target=self.countdown_and_type, args=(countdown,), daemon=True).start()
    
    def countdown_and_type(self, countdown):
        """Đếm ngược và gõ"""
        self.is_typing = True
        self.is_paused = False
        
        for i in range(countdown, 0, -1):
            if not self.is_typing:
                return
            self.root.after(0, lambda x=i: self.status_label.config(
                text=f"⏳ Đếm ngược: {x}s\nChuyển sang app khác!"
            ))
            time.sleep(1)
        
        if self.is_typing:
            method = self.method_var.get()
            method_name = "SMART" if method == "smart" else "CLIPBOARD"
            
            self.root.after(0, lambda: (
                self.status_label.config(
                    text=f"⚡ ĐANG GÕ ({method_name})...\nTốc độ: {self.typing_speed:.3f}s/ký tự"
                ),
                self.start_button.config(text="⚡ ĐANG GÕ...")
            ))
            
            time.sleep(0.5)
            self.type_text()
    
    def type_text(self):
        """Gõ văn bản"""
        try:
            total_chars = len(self.text_to_type)
            method = self.method_var.get()
            
            for i, char in enumerate(self.text_to_type):
                if not self.is_typing:
                    break
                
                while self.is_paused and self.is_typing:
                    time.sleep(0.01)
                
                if not self.is_typing:
                    break
                
                # Gõ ký tự
                if char == '\n':
                    pyautogui.press('enter')
                    time.sleep(0.03)
                elif char == '\t':
                    pyautogui.press('tab')
                    time.sleep(0.03)
                elif char == ' ':
                    pyautogui.press('space')
                    time.sleep(0.01)
                else:
                    if method == "smart":
                        self.type_character_smart(char)
                    else:
                        self.type_character_clipboard(char)
                
                # Delay
                if char not in ['\n', '\t', ' ']:
                    time.sleep(self.typing_speed)
                
                # Cập nhật tiến độ
                if (i + 1) % 10 == 0 or i + 1 == total_chars:
                    progress = ((i + 1) / total_chars) * 100
                    self.root.after(0, lambda p=progress, idx=i+1: (
                        self.progress_label.config(
                            text=f"Tiến độ: {p:.1f}% ({idx}/{total_chars})"
                        )
                    ))
            
            if self.is_typing:
                self.root.after(0, lambda: (
                    self.status_label.config(
                        text=f"✅ HOÀN THÀNH!\nĐã gõ {total_chars} ký tự\nHTML entities đã được xử lý"
                    ),
                    self.progress_label.config(text="Tiến độ: 100%")
                ))
                
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(
                text=f"❌ LỖI: {str(e)}"
            ))
        finally:
            self.finish_typing()
    
    def toggle_pause(self):
        """Tạm dừng"""
        if self.is_typing:
            self.is_paused = not self.is_paused
            
            if self.is_paused:
                self.pause_button.config(text="▶️ TIẾP TỤC", bg=self.accent_color)
                self.status_label.config(text="⏸️ ĐÃ TẠM DỪNG\nNhấn TIẾP TỤC để tiếp tục")
            else:
                self.pause_button.config(text="⏸️ TẠM DỪNG", bg="#ff9900")
                self.status_label.config(text="⚡ ĐANG TIẾP TỤC GÕ...")
    
    def stop_typing(self):
        """Dừng"""
        self.is_typing = False
        self.is_paused = False
        self.root.after(0, lambda: self.status_label.config(
            text="🛑 ĐÃ DỪNG\nNhấn BẮT ĐẦU để gõ lại"
        ))
        self.finish_typing()
    
    def finish_typing(self):
        """Kết thúc"""
        self.is_typing = False
        self.is_paused = False
        self.start_button.config(state=tk.NORMAL, bg=self.primary_color, text="🚀 BẮT ĐẦU GÕ")
        self.file_button.config(state=tk.NORMAL, bg=self.accent_color)
        self.pause_button.config(state=tk.DISABLED, bg="#555555", text="⏸️ TẠM DỪNG")
        self.stop_button.config(state=tk.DISABLED, bg="#555555")
    
    def on_closing(self):
        """Đóng app"""
        self.stop_typing()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = HTMLTypingSimulator(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    print("=== Sang Dev - HTML Typing Simulator ===")
    print("Hỗ trợ: &lt; &gt; &amp; &quot; &#39; etc.")
    print("Cài đặt: pip install pyautogui pyperclip")
    main()
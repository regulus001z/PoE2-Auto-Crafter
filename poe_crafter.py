import customtkinter as ctk
import pyautogui
import pyperclip
import threading
import time
import re
import keyboard

# --- VERSION CONTROL ---
APP_VERSION = "v1.27 (Exe)"
APP_TITLE = f"PoE 2 Auto Crafter {APP_VERSION}"

# Theme Setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PoEBotText(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title(APP_TITLE)
        self.geometry("500x720")
        self.resizable(False, False)
        
        # Variables
        self.chaos_pos = None
        self.item_pos = None
        self.is_running = False

        # --- UI LAYOUT (คงเดิมตามที่คุณขอ) ---
        
        # 1. Header Section
        self.frame_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header.pack(pady=(20, 10))
        
        self.lbl_title = ctk.CTkLabel(self.frame_header, text="RNG Chaos Roll by Yuki.xyz", font=("Roboto", 28, "bold"))
        self.lbl_title.pack()
        
        self.lbl_subtitle = ctk.CTkLabel(self.frame_header, text="Press 'X' to STOP", text_color="orange", font=("Arial", 14))
        self.lbl_subtitle.pack()

        # 2. Coordinates Section (Grid Layout)
        self.frame_coords = ctk.CTkFrame(self)
        self.frame_coords.pack(pady=10, padx=20, fill="x")
        self.frame_coords.grid_columnconfigure((0, 1), weight=1)

        # Chaos Button & Label
        self.btn_set_chaos = ctk.CTkButton(self.frame_coords, text="1. Set Chaos", command=self.set_chaos_action, 
                                         font=("Arial", 14, "bold"), height=40, fg_color="#D4AF37", hover_color="#B8860B", text_color="black")
        self.btn_set_chaos.grid(row=0, column=0, padx=10, pady=(15, 5), sticky="ew")
        
        self.lbl_chaos_status = ctk.CTkLabel(self.frame_coords, text="Not Set", text_color="red", font=("Arial", 12))
        self.lbl_chaos_status.grid(row=1, column=0, padx=10, pady=(0, 15))

        # Item Button & Label
        self.btn_set_item = ctk.CTkButton(self.frame_coords, text="2. Set Item", command=self.set_item_action, 
                                        font=("Arial", 14, "bold"), height=40, fg_color="#4682B4", hover_color="#36648B")
        self.btn_set_item.grid(row=0, column=1, padx=10, pady=(15, 5), sticky="ew")
        
        self.lbl_item_status = ctk.CTkLabel(self.frame_coords, text="Not Set", text_color="red", font=("Arial", 12))
        self.lbl_item_status.grid(row=1, column=1, padx=10, pady=(0, 15))

        # 3. Input Section
        self.lbl_instruct = ctk.CTkLabel(self, text="Paste mods here (poe2db supported).", text_color="silver", font=("Arial", 12))
        self.lbl_instruct.pack(pady=(10, 5))
        
        self.textbox = ctk.CTkTextbox(self, width=460, height=220, font=("Consolas", 14), border_width=2, corner_radius=10)
        self.textbox.pack(pady=5, padx=20)
        
        # Default Text (ค่าเดิม)
        default_text = """"""
        self.textbox.insert("0.0", default_text)

        # 4. Status & Control Section
        self.frame_controls = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_controls.pack(pady=20, padx=20, fill="x")

        self.lbl_log = ctk.CTkLabel(self.frame_controls, text="Status: Ready", font=("Arial", 16, "bold"))
        self.lbl_log.pack(pady=(0, 15))

        self.btn_start = ctk.CTkButton(self.frame_controls, text="START CRAFTING", command=self.start_bot,
                                     font=("Arial", 18, "bold"), height=50, fg_color="#2E8B57", hover_color="#228B22")
        self.btn_start.pack(fill="x", pady=5)

        self.btn_stop = ctk.CTkButton(self.frame_controls, text="STOP (Press X)", command=self.stop_bot,
                                    font=("Arial", 14, "bold"), height=40, fg_color="#CD5C5C", hover_color="#8B0000", state="disabled")
        self.btn_stop.pack(fill="x", pady=5)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Hotkey listener
        self.check_hotkey()

    def check_hotkey(self):
        if self.is_running and keyboard.is_pressed('x'):
            self.stop_bot()
        self.after(20, self.check_hotkey)

    def set_chaos_action(self):
        self.lbl_chaos_status.configure(text="Hover Currency... (2s)", text_color="orange")
        self.update()
        time.sleep(2)
        self.chaos_pos = pyautogui.position()
        self.lbl_chaos_status.configure(text=f"OK {self.chaos_pos}", text_color="#00FF00")

    def set_item_action(self):
        self.lbl_item_status.configure(text="Hover Item... (2s)", text_color="orange")
        self.update()
        time.sleep(2)
        self.item_pos = pyautogui.position()
        self.lbl_item_status.configure(text=f"OK {self.item_pos}", text_color="#00FF00")

    def parse_user_requirements(self, user_text):
        requirements = []
        clean_text = user_text.replace('–', '-').replace('—', '-')
        lines = clean_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or not re.search(r'\d', line): continue

            try:
                token_pattern = r'\(?(\d+)(?:-\d+)?\)?'
                min_values = []
                tokens = re.findall(token_pattern, line)
                if not tokens: continue
                for t in tokens: min_values.append(int(t))
                
                parts = re.split(r'\(?\d+(?:-\d+)?\)?', line)
                regex_pattern = ""
                for i, part in enumerate(parts):
                    regex_pattern += re.escape(part)
                    if i < len(parts) - 1:
                        regex_pattern += r"([\d,]+)"
                
                regex_pattern = regex_pattern.replace(r'\ ', r'\s+')
                requirements.append({"pattern": regex_pattern, "min_values": min_values, "original_text": line})
            except: pass
        return requirements

    def check_item_match(self, item_data, requirements):
        clean_data = item_data.replace(',', '')
        for req in requirements:
            match = re.search(req["pattern"], clean_data)
            if match:
                game_values = [int(v) for v in match.groups()]
                if len(game_values) == len(req["min_values"]):
                    all_pass = True
                    for g_val, m_val in zip(game_values, req["min_values"]):
                        if g_val < m_val:
                            all_pass = False
                            break
                    if all_pass: return True
        return False

    def start_bot(self):
        if not self.chaos_pos or not self.item_pos:
            self.lbl_log.configure(text="Error: Coordinates not set!", text_color="#FF4500")
            return
        
        user_text = self.textbox.get("0.0", "end")
        self.requirements = self.parse_user_requirements(user_text)
        
        if not self.requirements:
            self.lbl_log.configure(text="Error: No valid mods!", text_color="#FF4500")
            return

        self.is_running = True
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.lbl_log.configure(text="Running... (Exe Replica)", text_color="cyan")
        
        threading.Thread(target=self.run_process).start()

    def stop_bot(self):
        if not self.is_running: return
        self.is_running = False
        self.lbl_log.configure(text="STOPPED.", text_color="white")
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        
        # Force Release Shift (Hardware level)
        keyboard.release('shift')

    def force_stop(self):
        self.stop_bot()

    # --- LOGIC: Exe Replica (Continuous Hold) ---
    def run_process(self):
        # 1. Pickup Currency
        self.lbl_log.configure(text="Picking up Currency...", text_color="orange")
        pyautogui.moveTo(self.chaos_pos)
        time.sleep(0.2)
        pyautogui.rightClick()
        time.sleep(0.3)

        # 2. Move to Item
        pyautogui.moveTo(self.item_pos)
        time.sleep(0.2)

        self.lbl_log.configure(text=">>> ROLLING (Exe Logic) <<<", text_color="#00FF00")

        # 3. Hold Shift ONCE (Like the .exe does)
        # ใช้ keyboard.press แทน pyautogui เพื่อความแน่นเหมือน .exe
        keyboard.press('shift')
        time.sleep(0.2) 

        while self.is_running:
            if keyboard.is_pressed('x'): self.stop_bot(); break

            # === CLICK ===
            # คลิกแบบไม่ต้องปล่อยปุ่ม Shift (เพราะเรากดค้างไว้ระดับ Hardware แล้ว)
            pyautogui.click()
            
            # Wait for Server (Exe มี delay นิดหน่อยกันหลุด)
            time.sleep(0.06)

            if keyboard.is_pressed('x'): self.stop_bot(); break

            # === COPY ===
            # Exe จะเคลียร์ clipboard ก่อนเสมอ
            pyperclip.copy("") 
            pyautogui.hotkey('ctrl', 'c')
            
            # Wait Clipboard
            data = ""
            for _ in range(8): 
                if keyboard.is_pressed('x'): self.stop_bot(); break
                data = pyperclip.paste()
                if data: break
                time.sleep(0.01)

            # === CHECK ===
            if self.check_item_match(data, self.requirements):
                self.lbl_log.configure(text="CRAFT SUCCESS!", text_color="#00FF00")
                keyboard.release('shift')
                self.stop_bot()
                break
            
            # Loop delay (Exe มีความหน่วงนิดเดียวเพื่อให้ CPU ไม่พีค)
            time.sleep(0.02)

    def on_close(self):
        self.is_running = False
        keyboard.release('shift')
        self.destroy()

if __name__ == "__main__":
    app = PoEBotText()
    app.mainloop()
from logging import root
import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
import sys
from PIL import Image
import json
from groq import Groq
import re





ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 






class Application(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("ExeFlow - Python to EXE Converter")
        self.geometry("1200x600")
        self.resizable(False, False)
        self.iconbitmap("PythonScriptCompiler/assets/logo.ico")

        self.py_file = None
        self.images_dir = None
        self.audio_dir = None
        self.icon_path = None
        self.frame_corner_radius = 25
        self.application_font = "Mona Sans"

        self.client = Groq(api_key="Your Groq API key goes here")
        self.model = "llama-3.1-8b-instant"
        

        # self.grid_rowconfigure(0, minsize=400)
        # self.grid_rowconfigure(1, minsize = 650)
        self.main_scroll = ctk.CTkScrollableFrame(
            self,
            width=700,
            height=520,
            corner_radius = self.frame_corner_radius
        )
        self.main_scroll.grid(row = 0, column = 0,padx=10, pady=20)

        self.ai_chat_scroll = ctk.CTkScrollableFrame(self, width = 350, height = 520, corner_radius= self.frame_corner_radius)
        self.ai_chat_scroll.grid(row = 0, column = 1,padx = 20, pady = 20)

        # self.bottom_overlay = ctk.CTkImage(light_image= Image.open("PythonScriptCompiler/assets/bottom.png"), dark_image= Image.open("PythonScriptCompiler/assets/bottom.png"), size = (self.winfo_screenwidth(), 100))
        # self.bottom_overlay_lable = ctk.CTkLabel(master = self,image = self.bottom_overlay, text = ' ')
        # self.bottom_overlay_lable.place(x = 0, y = 100)
        # self.bottom_overlay_lable.lift()
        # self.bottom_overlay_lable.configure(
        #     fg_color="red"
        # )

        #self.winfo_screenheight() 
        # for i in range(20):
        #     ctk.CTkButton(scroll, text=f"Btn {i}").pack(side="left", padx=10)
        
        #--------Image Importing-------

        icon_length = 20
        logo_lenght = 24

        logo = ctk.CTkImage(light_image=Image.open("PythonScriptCompiler/assets/logo.png"),dark_image=Image.open("PythonScriptCompiler/assets/logo.png"), size=(logo_lenght, logo_lenght))  
        console_icon = ctk.CTkImage(light_image = Image.open("PythonScriptCompiler/assets/console_icon.png"), dark_image=Image.open("PythonScriptCompiler/assets/console_icon.png"), size = (icon_length,icon_length))
        file_name_icon = ctk.CTkImage(light_image = Image.open("PythonScriptCompiler/assets/file_name_icon.png"), dark_image=Image.open("PythonScriptCompiler/assets/file_name_icon.png"), size = (icon_length,icon_length))
        folder_icon = ctk.CTkImage(light_image = Image.open("PythonScriptCompiler/assets/folder_icon.png"), dark_image=Image.open("PythonScriptCompiler/assets/folder_icon.png"), size = (icon_length,icon_length))
        image_icon = ctk.CTkImage(light_image = Image.open("PythonScriptCompiler/assets/image_icon.png"), dark_image=Image.open("PythonScriptCompiler/assets/image_icon.png"), size = (icon_length,icon_length))
        pyfile_icon = ctk.CTkImage(light_image = Image.open("PythonScriptCompiler/assets/pyfile_icon.png"), dark_image=Image.open("PythonScriptCompiler/assets/pyfile_icon.png"), size = (icon_length,icon_length))
        audio_icon = ctk.CTkImage(light_image = Image.open("PythonScriptCompiler/assets/audio_icon.png"), dark_image=Image.open("PythonScriptCompiler/assets/audio_icon.png"), size = (icon_length,icon_length))
        user_icon = ctk.CTkImage(light_image = Image.open("PythonScriptCompiler/assets/user_icon.png"), dark_image=Image.open("PythonScriptCompiler/assets/user_icon.png"), size = (15,20))
        ai_icon = ctk.CTkImage(light_image = Image.open("PythonScriptCompiler/assets/ai_icon.png"), dark_image=Image.open("PythonScriptCompiler/assets/ai_icon.png"), size = (icon_length,icon_length))
        settings_icon = ctk.CTkImage(light_image = Image.open("PythonScriptCompiler/assets/settings_icon.png"), dark_image=Image.open("PythonScriptCompiler/assets/settings_icon.png"), size = (icon_length,icon_length))
        error_icon = ctk.CTkImage(light_image = Image.open("PythonScriptCompiler/assets/error_icon.png"), dark_image=Image.open("PythonScriptCompiler/assets/error_icon.png"), size = (icon_length,icon_length))
        ai_fix_icon = ctk.CTkImage(light_image = Image.open("PythonScriptCompiler/assets/ai_fix_icon.png"), dark_image=Image.open("PythonScriptCompiler/assets/ai_fix_icon.png"), size = (icon_length,icon_length))
        

        

        ######## AI SECTION #########

        self.ai_name = ctk.CTkLabel(self.ai_chat_scroll, text="  FLOW AI",image = logo, compound="left", font=(self.application_font, 25, "bold"), bg_color="#2b2b2b")
        self.ai_name.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.ai_name.lift()

        self.command_lable = ctk.CTkLabel(self.ai_chat_scroll, text = "  User Command:",image = user_icon, compound = "left", font = (self.application_font, 15) )
        self.command_lable.grid(row = 3, column =0, padx = 5, pady = 5, sticky = "w")

        self.ai_chat_scroll.grid_columnconfigure(0, minsize= 300)


        # self.settings_button = ctk.CTkButton(self.ai_chat_scroll, text="",image = settings_icon, compound = "left", width=10, height=40, fg_color="#1f1f1f", hover_color="#303030", corner_radius = 45)
        # self.settings_button.grid(row=0, column=0, padx=0, pady=10, sticky = "e")

        #AI COMMAND TEXTBOX
        self.ai_textbox = ctk.CTkTextbox(self.ai_chat_scroll, width=310, height=270, corner_radius=self.frame_corner_radius )
        self.ai_textbox.grid(row=4, column=0, padx=3, pady=5)

        self.ai_apply_btn = ctk.CTkButton( self.ai_chat_scroll, text="Generate Settings", command=self.process_ai_input, width=200, height=40, fg_color="#2b2b2b",border_color="#1f6aa5",border_width=3, hover_color="#515151", corner_radius = 45)
        self.ai_apply_btn.grid(row=6, column=0, pady=10)

        self.ans_processing_progressbar = ctk.CTkProgressBar(
            self.ai_chat_scroll,
            width=250,
            mode="indeterminate"
        )
        self.ans_processing_progressbar.grid(row=5, column=0, padx=47, pady=5, sticky="w")
        self.ans_processing_progressbar.stop()
        self.ans_processing_progressbar.grid_remove()  # hidden initially

        ########## AI ANSWERING ########

        self.ai_answer_textbox_lable = ctk.CTkLabel(self.ai_chat_scroll, text = "  AI Answer:",image = ai_icon, compound = "left", font = (self.application_font, 15) )  
        self.ai_answer_textbox_lable.grid(row = 7, column =0, padx = 5, pady = 5, sticky = "w")

        self.ai_chat_scroll.grid_columnconfigure(7, minsize= 300)

        self.ai_answer_textbox = ctk.CTkTextbox(self.ai_chat_scroll, width=310, height=200, corner_radius=self.frame_corner_radius)
        self.ai_answer_textbox.grid(row=8, column=0, padx=3, pady=5)

        ########## BUILDING ERRORS ########

        self.error_textbox_lable = ctk.CTkLabel(self.ai_chat_scroll, text = "  Building Errors:",image = error_icon, compound = "left", font = (self.application_font, 15) )
        self.error_textbox_lable.grid(row = 11, column =0, padx = 5, pady = 5, sticky = "w")

        self.ai_chat_scroll.grid_columnconfigure(12, minsize= 300)

        self.error_textbox = ctk.CTkTextbox( self.ai_chat_scroll,text_color = "#dd6c65", width=310, height=200, corner_radius=self.frame_corner_radius)
        self.error_textbox.grid(row=13, column=0, padx=3, pady=5)

        ########## AI FIXES ########

        self.ai_fix_textbox_lable = ctk.CTkLabel(self.ai_chat_scroll, text = "  AI Fixes:",image = ai_fix_icon, compound = "left", font = (self.application_font, 15) )
        self.ai_fix_textbox_lable.grid(row = 14, column =0, padx = 5, pady = 5, sticky = "w")

        self.ai_chat_scroll.grid_columnconfigure(15, minsize= 300)

        self.ai_fix_textbox = ctk.CTkTextbox(self.ai_chat_scroll, width=310, height=200, corner_radius=self.frame_corner_radius, text_color="#8fbf79")
        self.ai_fix_textbox.grid(row=16, column=0, padx=3, pady=5)

        

        
        


        

        #-------------  MAIN FRAME  -----------------

        self.app_name = ctk.CTkLabel(self.main_scroll, text="  EXE FLOW",image = logo, compound="left",
                        font=(self.application_font, 25, "bold"), bg_color="#2b2b2b")
        self.app_name.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        self.welcome_label = ctk.CTkLabel(self.main_scroll, text="Welcome Back!", font=(self.application_font, 40, "bold"), bg_color="#2b2b2b")
        self.welcome_label.grid(row=1, column=1, pady=10, padx=10, sticky="n")




        self.main_scroll.grid_rowconfigure(4, minsize=50)

        self.file_data_label = ctk.CTkLabel(self.main_scroll, text="File Data",
                                    font=(self.application_font, 20), bg_color="#2b2b2b")
        self.file_data_label.grid(row=5, column =1, pady=2, padx=10, sticky="sw")

        self.file_data_desc_label = ctk.CTkLabel(self.main_scroll, text="Upload the files",
                                            font=(self.application_font, 12), bg_color="#2b2b2b", text_color="#7E89AC")
        self.file_data_desc_label.grid(row=6, column = 1, pady=0, padx=10, sticky="w")

        ######## Upload Section ########

        self.mf_upload_scroll = ctk.CTkScrollableFrame(self.main_scroll, width=600, height=400, fg_color="#252525", corner_radius = self.frame_corner_radius, scrollbar_button_color="#252525", scrollbar_button_hover_color="#252525")
        self.mf_upload_scroll.grid(row=7, column=1, pady=10, padx=10, sticky="w")

        self.file_name_label = ctk.CTkLabel(self.mf_upload_scroll, text="  File Name",image=file_name_icon,compound = 'left' ,font=(self.application_font, 20))
        self.file_name_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.file_name_entry = ctk.CTkEntry(self.mf_upload_scroll, width=300, placeholder_text="Enter file name")
        self.file_name_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        self.mf_upload_scroll.grid_rowconfigure(1, minsize=30)

        self.main_pyf_label = ctk.CTkLabel(self.mf_upload_scroll, text="  Python File",image=pyfile_icon,compound = 'left' , font=(self.application_font, 20))
        self.main_pyf_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        self.main_pyf_entry = ctk.CTkEntry(self.mf_upload_scroll, width=300, placeholder_text="Select your .py file")
        self.main_pyf_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        self.select_pyf_button = ctk.CTkButton(self.mf_upload_scroll, text="Browse", width=80, command=self.select_py)
        self.select_pyf_button.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        self.app_icon_label = ctk.CTkLabel(self.mf_upload_scroll, text="  App Icon",image=image_icon,compound = 'left' , font=(self.application_font, 20))
        self.app_icon_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")
        
        self.app_icon_entry = ctk.CTkEntry(self.mf_upload_scroll, width=300, placeholder_text="Select your icon file ")
        self.app_icon_entry.grid(row=4, column=1, pady=10, padx=10, sticky="w")

        self.select_icon_button = ctk.CTkButton(self.mf_upload_scroll, text="Browse", width=80, command=self.select_icon)
        self.select_icon_button.grid(row=5, column=1, pady=10, padx=10, sticky="w")
        

        ######## Upload Section End ########

        

        self.main_scroll.grid_rowconfigure(8, minsize=50)

        self.addition_items_label = ctk.CTkLabel(self.main_scroll, text="Additional Items", font=(self.application_font, 20), bg_color="#2b2b2b")
        self.addition_items_label.grid(row=9, column =1, pady=2, padx=10, sticky="sw")
    
        self.addition_items_desc_label = ctk.CTkLabel(self.main_scroll, text="Upload the Additional Items", font=(self.application_font, 12), bg_color="#2b2b2b",text_color="#7E89AC")
        self.addition_items_desc_label.grid(row=10, column = 1, pady=0, padx=10, sticky="w")

        ######## Additional Items Section ########

        self.mf_additional_scroll = ctk.CTkScrollableFrame(self.main_scroll, width=600, height=200, fg_color="#252525", corner_radius = self.frame_corner_radius, scrollbar_button_color="#252525", scrollbar_button_hover_color="#252525")
        self.mf_additional_scroll.grid(row=11, column=1, pady=10, padx=10, sticky="w")

        self.images_folder_label = ctk.CTkLabel(self.mf_additional_scroll, text="  Images Folder",image=folder_icon,compound = 'left' ,  font=(self.application_font, 20))
        self.images_folder_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.images_folder_entry = ctk.CTkEntry(self.mf_additional_scroll, width=286, placeholder_text="Select your images folder")
        self.images_folder_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")
        
        self.select_images_button = ctk.CTkButton(self.mf_additional_scroll, text="Browse", width=80, command=self.select_images)
        self.select_images_button.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        self.audio_folder_label = ctk.CTkLabel(self.mf_additional_scroll, text="  Audio Folder",image=folder_icon,compound = 'left' , font=(self.application_font, 20))
        self.audio_folder_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        self.audio_folder_entry = ctk.CTkEntry(self.mf_additional_scroll, width=286, placeholder_text="Select your audio folder")
        self.audio_folder_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")
        
        self.select_audio_button = ctk.CTkButton(self.mf_additional_scroll, text="Browse", width=80, command=self.select_audio)
        self.select_audio_button.grid(row=3, column=1, pady=10, padx=10, sticky="w")
        ######## Additional Items Section End ########

        self.additional_settings_label = ctk.CTkLabel(self.main_scroll, text="Additional Settings", font=(self.application_font, 20), bg_color="#2b2b2b")
        self.additional_settings_label.grid(row=13, column =1, pady=2, padx=10, sticky="sw")

        self.additional_settings_desc_label = ctk.CTkLabel(self.main_scroll, text="Configure the settings", font=(self.application_font, 12), bg_color="#2b2b2b",text_color="#7E89AC")
        self.additional_settings_desc_label.grid(row=14, column = 1, pady=0, padx=10, sticky="w")
        
        self.main_scroll.grid_rowconfigure(12, minsize = 50)
        
        ######## Additional Settings Section ########
        
        self.additional_settings_scroll = ctk.CTkScrollableFrame(self.main_scroll, width=600, height=400, fg_color="#252525", corner_radius = self.frame_corner_radius, scrollbar_button_color="#252525", scrollbar_button_hover_color="#252525")   
        self.additional_settings_scroll.grid(row=15, column=1, pady=10, padx=10, sticky="w")

        def disable_scrollable_frame_scroll(scroll_frame):
            def _block(event):
                return "break"

            scroll_frame.bind("<MouseWheel>", _block)
            scroll_frame._parent_canvas.bind("<MouseWheel>", _block)

        self.onefile_var = ctk.BooleanVar(value=True)
        self.noconsole_var = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(self.additional_settings_scroll, text="One File", variable=self.onefile_var).grid(row=0, column=0, pady=10, padx=10, sticky="w")
        ctk.CTkCheckBox(self.additional_settings_scroll, text="No Console", variable=self.noconsole_var).grid(row=1, column=0, pady=10, padx=10, sticky="w")    

        self.build_dist_folder_label = ctk.CTkLabel(self.additional_settings_scroll, text="  Build Dist Folder",image=folder_icon,compound = 'left' , font=(self.application_font, 20))
        self.build_dist_folder_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        self.build_dist_folder_entry = ctk.CTkEntry(self.additional_settings_scroll, width=286, placeholder_text="Select your build dist folder")
        self.build_dist_folder_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        self.select_build_dist_button = ctk.CTkButton(self.additional_settings_scroll, text="Browse", width=80, command=self.select_folder)
        self.select_build_dist_button.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        self.splash_image_label = ctk.CTkLabel(self.additional_settings_scroll, text="  Splash Image",image=image_icon,compound = 'left' , font=(self.application_font, 20))
        self.splash_image_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")

        self.splash_image_discription_label = ctk.CTkLabel(self.additional_settings_scroll,anchor="w",justify="left", text="It only appears while the\napplication is loading", font=(self.application_font, 12), bg_color="#252525",text_color="#7E89AC")
        self.splash_image_discription_label.grid(row=5, column=0, pady=10, padx=10, sticky="nw")

        self.splash_image_entry = ctk.CTkEntry(self.additional_settings_scroll, width=286, placeholder_text="Select your splash image")
        self.splash_image_entry.grid(row=4, column=1, pady=10, padx=10, sticky="w")

        self.select_splash_image_button = ctk.CTkButton(self.additional_settings_scroll, text="Browse", width=80, command=self.select_splash_image)
        self.select_splash_image_button.grid(row=5, column=1, pady=10, padx=10, sticky="w")

        self.additional_commands_label = ctk.CTkLabel(self.additional_settings_scroll, text="  Additional Commands",image=console_icon,compound = 'left' , font=(self.application_font, 20))
        self.additional_commands_label.grid(row=6, column=0, pady=10, padx=10, sticky="w")
        
        self.additional_commands_discription_label = ctk.CTkLabel(self.additional_settings_scroll, text="Add any additional PyInstaller commands", font=(self.application_font, 12), bg_color="#252525",text_color="#7E89AC")
        self.additional_commands_discription_label.grid(row=7, column=0, pady=0, padx=10, sticky="nw")
        
        self.additional_commands_entry = ctk.CTkEntry(self.additional_settings_scroll, width=286, placeholder_text="e.g., --clean --log-level=DEBUG")
        self.additional_commands_entry.grid(row=6, column=1, pady=10, padx=10, sticky="w")


        #Hidden Imports[Commented for now]

        # self.hidden_imports_label = ctk.CTkLabel(self.additional_settings_scroll, text="Hidden Imports", font=(self.application_font, 20))
        # self.hidden_imports_label.grid(row=2, column=0, pady=10, padx=10, sticky="sw")

        # self.hidden_imports_discription_label = ctk.CTkLabel(self.additional_settings_scroll, text="Name the modules to be hidden", font=(self.application_font, 12), bg_color="#252525",text_color="#7E89AC")
        # self.hidden_imports_discription_label.grid(row=3, column=0, pady=0, padx=10, sticky="nw")

        # self.hidden_imports_entry = ctk.CTkEntry(self.additional_settings_scroll, width=400, placeholder_text="e.g., module1,module2,...")
        # self.hidden_imports_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        
        ######## Additional Settings Section End ########

        self.build_btn = ctk.CTkButton(self.main_scroll, text="Build EXE", command=self.start_build, width=200, height=40, fg_color="#2b2b2b",border_color="#fbfcfd",border_width=3, hover_color="#515151", corner_radius = 45)
        self.build_btn.grid(row=16, column=1, pady=20, padx=10, sticky="n")

        self.main_scroll.grid_columnconfigure(0, weight=1)

        self.log_command_label = ctk.CTkLabel(self.main_scroll, text="Build Logs",font=(self.application_font, 20), bg_color="#2b2b2b")
        self.log_command_label.grid(row=17, column =1, pady=2, padx=10, sticky="sw")

        self.console_log_box = ctk.CTkTextbox(
                self.main_scroll,
                width=610,
                height=260,
                corner_radius = self.frame_corner_radius,
                # text_color="#8fbf79"
                text_color="#FFFFFF"
                )

        
        self.console_log_box.grid(
                row=18,
                column=1,
                padx=20,
                pady=10,
                sticky="nsew"
                )
        
        self.build_progress = ctk.CTkProgressBar(self.main_scroll, width=580)
        self.build_progress.grid(row=19, column=1, pady=(5, 10))
        self.build_progress.set(0)

        
        self.main_scroll.grid_rowconfigure(20, minsize=20)

        self.final_command_label = ctk.CTkLabel(self.main_scroll, text="Final Command",font=(self.application_font, 20), bg_color="#2b2b2b")
        self.final_command_label.grid(row=21, column =1, pady=2, padx=10, sticky="sw")

        self.final_command_log_box = ctk.CTkTextbox(self.main_scroll, width=610, height=80, corner_radius = self.frame_corner_radius)
        self.final_command_log_box.grid(row=22, column=1, pady=10, padx=10)

            
        



    # ---------------- FUNCTIONS ----------------



    # ---------------- MAIN FUNCTIONS ----------------
    def select_py(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if path:
            self.py_file = path
            self.main_pyf_entry.delete(0, "end")
            self.main_pyf_entry.insert(0, path)

    def select_images(self):
        folder = filedialog.askdirectory()
        if folder:
            self.images_dir = folder
            self.images_folder_entry.delete(0, "end")
            self.images_folder_entry.insert(0, folder)

    def select_audio(self):
        folder = filedialog.askdirectory()
        if folder:
            self.audio_dir = folder
            self.audio_folder_entry.delete(0, "end")
            self.audio_folder_entry.insert(0, folder)
    
    def select_splash_image(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg"),
                ("All Files", "*.*")
            ]
        )
        if path:
            self.splash_image_entry.delete(0, "end")
            self.splash_image_entry.insert(0, path)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.build_dist_folder_entry.delete(0, "end")
            self.build_dist_folder_entry.insert(0, folder)

    def convert_to_ico(self, image_path):
        ico_path = os.path.splitext(image_path)[0] + ".ico"
        img = Image.open(image_path)
        img.save(ico_path, format="ICO", sizes=[(256, 256)])
        return ico_path
    
    def update_progress_from_output(self, line):
        line = line.lower()

        if "analyzing" in line:
            self.build_progress.set(0.2)
        elif "building exe" in line:
            self.build_progress.set(0.5)
        elif "collecting" in line:
            self.build_progress.set(0.7)
        elif "writing exe" in line or "copying" in line:
            self.build_progress.set(0.9)
    

    def refresh_app(event=None):
        
        subprocess.Popen(["python", "main.py"])
        app.after(3000, app.destroy()) # Wait for 3 second before closing

    def select_icon(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Image/Icon Files", "*.ico *.png *.jpg *.jpeg"),
                ("All Files", "*.*")
            ]
        )

        if not path:
            return

        ext = os.path.splitext(path)[1].lower()

        if ext != ".ico":
            try:
                path = self.convert_to_ico(path)
            except Exception as e:
                messagebox.showerror("Icon Error", f"Failed to convert icon:\n{e}")
                return

        self.icon_path = path
        self.app_icon_entry.delete(0, "end")
        self.app_icon_entry.insert(0, path)

    def start_build(self):
        if not self.py_file:
            messagebox.showerror("Error", "Select a Python file")
            return

        self.build_btn.configure(state="disabled")
        self.console_log_box.delete("1.0", "end")

        self.build_progress.configure(mode="indeterminate")
        self.build_progress.start()

        threading.Thread(target=self.run_pyinstaller, daemon=True).start()

    # ----------- AI FUNCTIONALITY -----------

    def process_ai_input(self):
        prompt = self.ai_textbox.get("1.0", "end").strip()
        if not prompt:
            messagebox.showerror("Error", "Enter instructions")
            return

        self.start_ai_loading()

        def task():
            try:
                # SETTINGS MODE
                if self.is_settings_intent(prompt):
                    data = self.ask_ai(prompt)

                    def apply_settings():
                        if "py_file" in data:
                            self.main_pyf_entry.delete(0, "end")
                            self.main_pyf_entry.insert(0, data["py_file"])

                        if "images_dir" in data:
                            self.images_folder_entry.delete(0, "end")
                            self.images_folder_entry.insert(0, data["images_dir"])

                        if "audio_dir" in data:
                            self.audio_folder_entry.delete(0, "end")
                            self.audio_folder_entry.insert(0, data["audio_dir"])

                        if "icon_path" in data:
                            self.app_icon_entry.delete(0, "end")
                            self.app_icon_entry.insert(0, data["icon_path"])

                        if "onefile" in data:
                            self.onefile_var.set(bool(data["onefile"]))

                        if "noconsole" in data:
                            self.noconsole_var.set(bool(data["noconsole"]))

                        if "extra_args" in data:
                            self.additional_commands_entry.delete(0, "end")
                            self.additional_commands_entry.insert(
                                0, " ".join(data["extra_args"])
                            )

                        if "name_file" in data:
                            self.file_name_entry.delete(0, "end")
                            self.file_name_entry.insert(0, data["name_file"])

                        if "build_dist" in data:
                            self.build_dist_folder_entry.delete(0, "end")
                            self.build_dist_folder_entry.insert(0, data["build_dist"])

                        if "splash_image" in data:
                            self.splash_image_entry.delete(0, "end")
                            self.splash_image_entry.insert(0, data["splash_image"])

                        self.write_textbox(self.ai_answer_textbox, "Done.")

                    self.after(0, apply_settings)

                # CHAT MODE
                else:
                    answer = self.ask_ai_chat(prompt)
                    self.after(0, lambda: self.write_textbox(self.ai_answer_textbox, answer))

            except Exception as e:
                self.after(0, lambda: messagebox.showerror("AI Error", str(e)))

            finally:
                self.after(0, self.stop_ai_loading)
                self.after(0, lambda: self.ai_textbox.delete("1.0", "end"))

        threading.Thread(target=task, daemon=True).start()
    
    #checks if the text contains any of the keywords(is user intend to change any settings)
    def is_settings_intent(self, text):
        keywords = [
            "set", "change", "enable", "disable", "add", "remove",
            "use", "build", "convert", "make exe", "onefile",
            "noconsole", "icon", "splash", "pyinstaller"
        ]
        text = text.lower()
        return any(k in text for k in keywords)
    
    # asks the api for the answer
    def ask_ai_chat(self, user_prompt):
        system_prompt = (
            "You are a helpful assistant for a Python EXE builder app.And creator of this as is Sanath\n"
            "Answer clearly and briefly.\n"
            "No JSON. No markdown."
        )

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4,
            max_tokens=200
        )

        return completion.choices[0].message.content.strip()
    
    def ask_ai(self, user_prompt):
        system_prompt = (
            "You convert user instructions into JSON.\n"
            "Allowed keys:\n"
            "py_file, images_dir, audio_dir, icon_path,\n"
            "build_dist, onefile, noconsole, splash_image, extra_args, name_file\n\n"
            "Return ONLY valid JSON. No explanation."
        )

        completion = self.client.chat.completions.create(
            model="self.model",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )

        raw = completion.choices[0].message.content.strip()

        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError("AI did not return valid JSON")

        return json.loads(match.group())

    def ask_ai_answer(self, user_text):
        completion = self.client.chat.completions.create(
            model="self.model",
            messages=[
                {"role": "system", "content": "Answer clearly and briefly."},
                {"role": "user", "content": user_text}
            ],
            temperature=0.4,
            max_tokens=200
        )
        return completion.choices[0].message.content.strip()


    def compress_error(self, err_text, max_lines=6):
        lines = err_text.strip().splitlines()
        return "\n".join(lines[-max_lines:])
    
    

    def ask_ai_error_fix(self, error_log):
        system_prompt = (
            "You fix Python build/compile errors.\n"
            "Reply with a short clear solution.\n"
            "No explanations, no code blocks."
        )

        compressed = self.compress_error(error_log)

        completion = self.client.chat.completions.create(
            model="self.model",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": compressed}
            ],
            temperature=0.1,
            max_tokens=120
        )

        return completion.choices[0].message.content.strip()
    
    
    

    # AI SECONDARY FUNCTIONALITY
    
    
    _typing_job = None

    def write_textbox(self, textbox, text, delay=25):
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")

        cursor = "▌"

        def type_char(i=0):
            textbox.delete("end-2c", "end")  # remove old cursor

            if i < len(text):
                textbox.insert("end", text[i] + cursor)
                textbox.see("end")
                textbox.after(delay, type_char, i + 1)
            else:
                textbox.insert("end", "")     # remove cursor
                textbox.configure(state="disabled")

        textbox.insert("end", cursor)
        type_char()

    
    
    def start_ai_loading(self):
        self.ans_processing_progressbar.grid()
        self.ans_processing_progressbar.start()

        self.ai_apply_btn.configure(
            state="disabled",
            fg_color= "#515151"
        )

    def stop_ai_loading(self):
        self.ans_processing_progressbar.stop()
        self.ans_processing_progressbar.grid_remove()

        self.ai_apply_btn.configure(
            state="normal",
            fg_color= "#2b2b2b"
        )
    
    def type_text(self, textbox, text, delay=15):
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")

        def write(i=0):
            if i < len(text):
                textbox.insert("end", text[i])
                textbox.see("end")
                textbox.after(delay, write, i + 1)
            else:
                textbox.configure(state="disabled")

        write()


    

#-------------------- BUILDING EXE FUNCTIONALITY --------------------

    

    def run_pyinstaller(self):
        cmd = [sys.executable, "-m", "PyInstaller"]
        self.build_progress.set(0)

        # One FIle opition
        if self.onefile_var.get():
            cmd.append("--onefile")
        
        # No Console option
        if self.noconsole_var.get():
            cmd.append("--noconsole")
        # App Name
        app_name = self.file_name_entry.get().strip()
        if app_name:
            cmd += ["--name", app_name]
        # Icon Path
        if self.icon_path:
            cmd += ["--icon", self.icon_path]

        # Main Python File
        cmd.append(self.py_file)

        # Images folder (ONLY if user selected it)
        if self.images_dir and os.path.exists(self.images_dir):
            images_path = os.path.abspath(self.images_dir)
            cmd += ["--add-data", f"{images_path};images"]
        
        # Audio folder (ONLY if user selected it)
        if self.audio_dir and os.path.exists(self.audio_dir):
            audio_path = os.path.abspath(self.audio_dir)
            cmd += ["--add-data", f"{audio_path};audio"]

        # Build Dist Folder
        build_dist_folder = self.build_dist_folder_entry.get().strip()
        if build_dist_folder:
            cmd += ["--distpath", build_dist_folder]
        
        # Final Command Display
        self.final_command_log_box.delete("1.0", "end")
        self.final_command_log_box.insert("1.0", " ".join(cmd))

        #Distination folder
        dist_folder = self.build_dist_folder_entry.get().strip()
        if dist_folder:
            cmd += ["--distpath", dist_folder]

        # Splash Image
        splash_image = self.splash_image_entry.get().strip()
        if splash_image:
            cmd += ["--splash", splash_image]

        # Additional Commands
        additional_commands = self.additional_commands_entry.get().strip()
        if additional_commands:
            cmd += additional_commands.split()

        # Hidden Imports
        # hidden_imports = self.hidden_imports_entry.get().strip()
        # if hidden_imports:
        #     for module in hidden_imports.split(","):
        #         module = module.strip()
        #         if module:
        #             cmd += ["--hidden-import", module]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            self.console_log_box.insert("end", line)
            self.console_log_box.see("end")
            self.update_progress_from_output(line)



        process.wait()

        self.build_progress.stop()
        self.build_progress.configure(mode="determinate")



        self.build_btn.configure(state="normal")

        self.build_progress.set(1.0)

        if process.returncode == 0:
            messagebox.showinfo("Success", "EXE created in /dist folder")
        else:
            messagebox.showerror("Failed", "Build failed. Check logs.")

        # Audio folder (ONLY if user selected it)
        if self.audio_dir and os.path.exists(self.audio_dir):
            cmd += ["--add-data", f"{self.audio_dir};audio"]

        # Images folder (ONLY if user selected it)
        if self.images_dir and os.path.exists(self.images_dir):
            cmd += ["--add-data", f"{self.images_dir};images"]

        try:
            self.run_build()   # your existing compile function

        except Exception as e:
            error_text = str(e)

            # Show raw error
            self.write_textbox(self.error_textbox, error_text)

            try:
                ai_fix = self.ask_ai_error_fix(error_text)
                self.write_textbox(self.ai_fix_textbox, ai_fix)
            except Exception:
                self.write_textbox(
                    self.ai_fix_textbox,
                    "AI could not generate a fix. Check error above."
                )

        


        

        


if __name__ == "__main__":
    app = Application()
    app.bind_all("<Control-r>", lambda e: app.refresh_app())

    app.mainloop()












    
    
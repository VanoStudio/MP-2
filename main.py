import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FullscreenResponsiveApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ==== WINDOW UTAMA ====
        self.title("MP-2")
        self.state("zoomed")  # fullscreen tapi tetap ada title bar
        self.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.resizable(False, False)
        self.bind("<Configure>", self.force_fullscreen)

        # ==== SCALING ====
        screen_w, screen_h = self.winfo_screenwidth(), self.winfo_screenheight()
        base_w, base_h = 1920, 1080
        scale = min(screen_w / base_w, screen_h / base_h)

        def scaled(v): return int(v * scale)

        # ==== FRAME UTAMA ====
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self, corner_radius=20)
        main_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=scaled(40), pady=scaled(40))
        main_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # ==== TITLE BAR ====
        title_frame = ctk.CTkFrame(main_frame, fg_color="#4476cd", corner_radius=15)
        title_frame.grid(row=0, column=0, pady=(scaled(40), scaled(20)), sticky="n")
        title_frame.grid_propagate(False)
        title_frame.configure(width=scaled(600), height=scaled(120))

        title_label = ctk.CTkLabel(
            title_frame,
            text="WELCOME TO MP-2",
            font=("Arial", scaled(36), "bold"),
            text_color="#ffffff"
        )
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        # ==== LOGIN FRAME ====
        login_frame = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="#2e2e2e")
        login_frame.grid(row=2, column=0, pady=(scaled(20), scaled(60)))
        login_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        login_frame.grid_columnconfigure(0, weight=1)

        # ==== ENTRY + BUTTON ====
        entry_font = ("Arial", scaled(20))
        entry_width = scaled(400)
        entry_height = scaled(70)

        # Username Entry
        entry_username = ctk.CTkEntry(
            login_frame,
            placeholder_text="Username",
            font=entry_font,
            width=entry_width,
            height=entry_height
        )
        entry_username.grid(row=0, column=0, pady=scaled(15))

        # ==== PASSWORD + EYE ====
        password_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        password_frame.grid(row=1, column=0, pady=scaled(15))

        entry_password = ctk.CTkEntry(
            password_frame,
            placeholder_text="Password",
            font=entry_font,
            show="*",
            width=entry_width - scaled(60),
            height=entry_height
        )
        entry_password.pack(side="left", padx=(0, scaled(10)))

        # toggle eye button
        self.password_visible = False

        def toggle_password():
            self.password_visible = not self.password_visible
            if self.password_visible:
                entry_password.configure(show="")
                eye_button.configure(text="🙈")
            else:
                entry_password.configure(show="*")
                eye_button.configure(text="👁")

        eye_button = ctk.CTkButton(
            password_frame,
            text="👁",
            width=scaled(50),
            height=entry_height,
            font=("Arial", scaled(20)),
            fg_color="#2e2e2e",
            hover_color="#3a3a3a",
            command=toggle_password
        )
        eye_button.pack(side="left")

        # ==== FADE TRANSITION HELPER ====
        # helper to animate a fade that only covers the login_frame using an overlay
        def fade_elements_transition(swap_fn, steps=10, delay=25):
            # create an overlay Toplevel positioned exactly over login_frame
            try:
                self.update_idletasks()
                x = login_frame.winfo_rootx()
                y = login_frame.winfo_rooty()
                w = login_frame.winfo_width()
                h = login_frame.winfo_height()

                overlay = tk.Toplevel(self)
                overlay.overrideredirect(True)
                overlay.attributes("-topmost", True)
                # try to set initial alpha; if not supported, fallback to direct swap
                try:
                    overlay.attributes("-alpha", 0.0)
                except Exception:
                    overlay.destroy()
                    swap_fn()
                    return

                # position and color the overlay to match the login_frame background
                try:
                    bg = login_frame.cget("fg_color")
                except Exception:
                    bg = "#2e2e2e"

                overlay.geometry(f"{w}x{h}+{x}+{y}")
                overlay.configure(bg=bg)

                def fade_up(i=0):
                    a = min(1.0, i / steps)
                    overlay.attributes("-alpha", a)
                    if i < steps:
                        overlay.after(delay, lambda: fade_up(i + 1))
                    else:
                        # fully covered; perform swap, then fade down
                        swap_fn()
                        overlay.after(delay, lambda: fade_down(steps))

                def fade_down(i=steps):
                    a = max(0.0, i / steps)
                    overlay.attributes("-alpha", a)
                    if i > 0:
                        overlay.after(delay, lambda: fade_down(i - 1))
                    else:
                        try:
                            overlay.destroy()
                        except Exception:
                            pass

                fade_up(0)
            except Exception:
                # if anything fails, just perform the swap immediately
                swap_fn()

        # ==== BUTTONS ====
        login_google_btn = ctk.CTkButton(
            login_frame,
            text="Login dengan Google",
            fg_color="#DB4437",
            hover_color="#C33D2F",
            font=("Arial", scaled(18), "bold"),
            height=scaled(70),
            width=entry_width
        )
        login_google_btn.grid(row=2, column=0, pady=scaled(15))

        login_btn = ctk.CTkButton(
            login_frame,
            text="Login",
            fg_color="#4CAF50",
            hover_color="#45A049",
            font=("Arial", scaled(18), "bold"),
            height=scaled(70),
            width=entry_width
        )
        login_btn.grid(row=3, column=0, pady=scaled(15))

                # ==== LABEL REGISTER (klikable) ====
        def open_register():
            # perform the register UI swap inside a fade transition
            def swap_to_register():
                # sembunyikan semua elemen login
                for widget in login_frame.winfo_children():
                    widget.grid_forget()

                register_title = ctk.CTkLabel(
                    login_frame, 
                    text="Buat Akun Baru",
                    font=("Arial", scaled(28), "bold"),
                    text_color="#FFFFFF"
                )
                register_title.grid(row=0, column=0, pady=(scaled(20), scaled(30)))

                entry_reg_user = ctk.CTkEntry(login_frame, placeholder_text="Username", width=scaled(400), height=scaled(70))
                entry_reg_email = ctk.CTkEntry(login_frame, placeholder_text="Email", width=scaled(400), height=scaled(70))
                entry_reg_pass = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=scaled(400), height=scaled(70))

                entry_reg_user.grid(row=1, column=0, pady=scaled(10))
                entry_reg_email.grid(row=2, column=0, pady=scaled(10))
                entry_reg_pass.grid(row=3, column=0, pady=scaled(10))

                back_to_login = ctk.CTkButton(
                    login_frame, text="Kembali ke Login",
                    fg_color="#555555", hover_color="#666666",
                    width=scaled(400), height=scaled(70),
                    command=show_login
                )
                back_to_login.grid(row=4, column=0, pady=scaled(20))

            fade_elements_transition(swap_to_register)

        def show_login():
            # swap back to the login UI inside a fade transition
            def swap_to_login():
                # hapus elemen register dan tampilkan ulang elemen login
                for widget in login_frame.winfo_children():
                    widget.grid_forget()

                # panggil ulang entry login & tombol yang sudah ada
                entry_username.grid(row=0, column=0, pady=scaled(15))

                # Tampilkan kembali frame password dengan entry dan tombol eye
                password_frame.grid(row=1, column=0, pady=scaled(15))
                # ensure packed children exist inside the password_frame
                entry_password.pack(side="left", padx=(0, scaled(10)))
                eye_button.pack(side="left")

                # Tampilkan kembali tombol-tombol
                login_google_btn.grid(row=2, column=0, pady=scaled(15))
                login_btn.grid(row=3, column=0, pady=scaled(15))
                register_label.grid(row=4, column=0, pady=scaled(15))

            fade_elements_transition(swap_to_login)

        def on_hover(e):
            register_label.configure(text_color="#4A90E2")  # warna biru pas hover

        def off_hover(e):
            
            register_label.configure(text_color="#AAAAAA")  # kembali ke abu pas keluar hover
            
        register_label = ctk.CTkLabel(
            login_frame,
            text="Belum punya akun? Daftar di sini",
            font=("Arial", scaled(16)),
            text_color="#AAAAAA"
        )
        register_label.grid(row=4, column=0, pady=scaled(15))
        
        # === Event Binding ===
        register_label.bind("<Button-1>", lambda e: open_register())
        register_label.bind("<Enter>", on_hover)
        register_label.bind("<Leave>", off_hover)

        # ==== FOOTER ====
        footer = ctk.CTkLabel(
            main_frame,
            text="© 2025 Vann Project | SMK Cyber Media",
            font=("Arial", scaled(14)),
            text_color="#888888"
        )
        footer.grid(row=4, column=0, pady=(scaled(10), scaled(20)))

    def force_fullscreen(self, event=None):
        if self.state() != "zoomed":
            self.state("zoomed")

    def quit_app(self):
        self.destroy()

if __name__ == "__main__":
    app = FullscreenResponsiveApp()
    app.mainloop()

# -*- coding: utf-8 -*-
import psutil, platform, wx, subprocess, os, re

class LexusSpecAnalyzer(wx.Frame):
    def __init__(self):
        super(LexusSpecAnalyzer, self).__init__(None, title="Lexus Spec Analyzer v1.0", size=(750, 700))
        self.init_ui()
        self.Centre()
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer_tick, self.timer)
        self.progress = 0

    def init_ui(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#0d0d0d")
        v_layout = wx.BoxSizer(wx.VERTICAL)
        
        title = wx.StaticText(panel, label="LEXUS SPEC ANALYZER - HARDWARE AUDIT")
        title.SetForegroundColour("#00fbff")
        title.SetFont(wx.Font(14, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        v_layout.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        
        self.log = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE)
        self.log.SetBackgroundColour("#1a1a1a")
        self.log.SetForegroundColour("#00ff41")
        self.log.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        v_layout.Add(self.log, 1, wx.EXPAND | wx.ALL, 20)

        self.gauge = wx.Gauge(panel, range=100, size=(600, 15))
        self.gauge.Hide() 
        v_layout.Add(self.gauge, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        self.btn = wx.Button(panel, label="🚀 INICIAR ESCANEO DE HARDWARE", size=(350, 45))
        self.btn.SetBackgroundColour("#00fbff")
        self.btn.Bind(wx.EVT_BUTTON, self.on_start_click)
        v_layout.Add(self.btn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)
        
        panel.SetSizer(v_layout)

    def on_start_click(self, event):
        self.btn.Disable()
        self.log.SetValue("🕵️ AUDITANDO COMPONENTES...\n\nLexus-Team está extrayendo información técnica del sistema...")
        self.gauge.Show()
        self.gauge.SetValue(0)
        self.progress = 0
        self.Layout()
        self.timer.Start(30)

    def on_timer_tick(self, event):
        self.progress += 5
        self.gauge.SetValue(self.progress)
        if self.progress >= 100:
            self.timer.Stop()
            self.run_final_analysis()

    def get_detailed_cpu(self):
        try:
            # Obtenemos Nombre, Velocidad Máxima y Núcleos de forma nativa
            cmd = "wmic cpu get name, maxclockspeed, numberofcores /format:list"
            output = subprocess.check_output(cmd, shell=True, creationflags=0x08000000).decode('utf-8')
            data = {}
            for line in output.splitlines():
                if '=' in line:
                    k, v = line.split('=')
                    data[k.strip()] = v.strip()
            
            name = data.get('Name', 'Procesador Desconocido')
            cores = data.get('NumberOfCores', '0')
            speed = float(data.get('MaxClockSpeed', 0)) / 1000 # Convertir MHz a GHz
            return f"{name} @ {speed:.2f} GHz ({cores} Núcleos)"
        except: return platform.processor()

    def get_gpu_info(self):
        try:
            output = subprocess.check_output("wmic path win32_VideoController get name", 
                                            shell=True, creationflags=0x08000000).decode('utf-8')
            lines = [l.strip() for l in output.split('\n') if l.strip() and 'Name' not in l]
            return lines[0] if lines else "Gráficos Integrados"
        except: return "No detectada"

    def run_final_analysis(self):
        cpu_full = self.get_detailed_cpu()
        cores = psutil.cpu_count(logical=False)
        ram_gb = round(psutil.virtual_memory().total / (1024**3))
        gpu_name = self.get_gpu_info()
        
        gpu_up = gpu_name.upper()
        is_gaming_gpu = any(x in gpu_up for x in ["GTX", "RTX", "RX ", "NVIDIA", "RADEON", "VEGA"])
        
        score = 0
        if ram_gb >= 12: score += 2
        if cores >= 6: score += 2
        if is_gaming_gpu: score += 3

        msg =  f"{'='*60}\n ✅ AUDITORÍA COMPLETADA - LEXUS-TEAM\n{'='*60}\n\n"
        msg += f" 💻 CPU: {cpu_full}\n 🧠 NÚCLEOS FÍSICOS: {cores}\n 📊 RAM: {ram_gb} GB\n 🎮 GPU: {gpu_name}\n\n"

        if score >= 6:
            diag = "🏆 NIVEL: ENTUSIASTA / GAMING PRO\n"
            diag += " 🕹️ EMULACIÓN: Switch (4K), PS3, Xbox 360, Wii U y RCPS3.\n"
            diag += " 🖥️ JUEGOS NATIVOS: Cyberpunk 2077, Warzone, RDR2, Elden Ring."
        elif score >= 3:
            diag = "⚔️ NIVEL: GAMA MEDIA / GAMER ESTÁNDAR\n"
            diag += " 🕹️ EMULACIÓN: PS2 (4x Res), Wii, GameCube, 3DS, Citra y CEMU.\n"
            diag += " 🖥️ JUEGOS NATIVOS: GTA V, Fortnite, Valorant, Forza Horizon 4."
        else:
            diag = "📁 NIVEL: BÁSICO / RETRO GAMING\n"
            diag += " 🕹️ EMULACIÓN: PS1, N64, Dreamcast, DS, GBA, SNES, NES, Genesis, MAME (Arcade).\n"
            diag += " 🖥️ JUEGOS NATIVOS: Roblox, Minecraft, Cuphead, Stardew Valley, Terraria, LoL (Low)."

        msg += f" 🚩 DIAGNÓSTICO OBJETIVO: {diag}\n\n{'='*60}\n"
        msg += " 💡 ¿QUIERES OPTIMIZAR ESTA POTENCIA?\n"
        msg += " Nexus Architect está diseñado para exprimir tu hardware:\n"
        msg += " https://github.com/Lexus-Team/Nexus-Architect-Ultimate\n"
        msg += f"{'='*60}"

        self.log.SetValue(msg)
        self.gauge.Hide()
        self.btn.Enable()
        self.Layout()

if __name__ == "__main__":
    app = wx.App(redirect=False)
    LexusSpecAnalyzer().Show()
    app.MainLoop()
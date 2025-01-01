import tkinter as tk
from tkinter import ttk, messagebox
import math
import json

class WeatherCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Calculator")
        self.root.geometry("600x500")
        
        # Constants
        self.PI = 3.1415926535
        self.weather_types = ["Rain", "Sun", "Cloud", "Fog", "Wind"]
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input variables
        self.n_var = tk.StringVar()
        self.dc_var = tk.StringVar()
        self.dg_var = tk.StringVar()
        self.ld_var = tk.StringVar()
        self.weather_var = tk.StringVar(value=self.weather_types[0])
        
        # Create input fields
        ttk.Label(main_frame, text="Enter N value:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(main_frame, textvariable=self.n_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(main_frame, text="Enter DC value:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(main_frame, textvariable=self.dc_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(main_frame, text="Enter DG value:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(main_frame, textvariable=self.dg_var).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(main_frame, text="Enter LD value:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(main_frame, textvariable=self.ld_var).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(main_frame, text="Select Weather:").grid(row=4, column=0, padx=5, pady=5)
        weather_combo = ttk.Combobox(main_frame, textvariable=self.weather_var, values=self.weather_types)
        weather_combo.grid(row=4, column=1, padx=5, pady=5)
        
        # Create calculate button
        ttk.Button(main_frame, text="Calculate", command=self.calculate).grid(row=5, column=0, columnspan=2, pady=20)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.result_text = tk.Text(results_frame, height=10, width=50)
        self.result_text.grid(row=0, column=0, padx=5, pady=5)

    def amicable(self, n, ld):
        s1 = sum(j for j in range(1, n // 2 + 1) if n % j == 0)
        s2 = sum(j for j in range(1, ld // 2 + 1) if ld % j == 0)
        return s1 == ld and s2 == n

    def case_wind(self, n, dc, dg, ld):
        nbc = dc * dc
        nbg = (dg * dg * self.PI) / 4
        bc = n // nbc
        nd = n - bc * nbc
        bg = int(nd / nbg)
        nd = nd - bg * nbg
        max_bc = bc
        tld = bc + bg
        
        if tld > ld:
            if bc > ld:
                bc = ld
                bg = 0
                nd = n - bc * nbc
            else:
                bc = max_bc
                bg = ld - bc
                nd = n - bc * nbc - bg * nbg
        
        return bc, bg, nd

    def case_rain(self, n, dc, dg, ld):
        nbc = dc * dc
        nbg = (dg * dg * self.PI) / 4
        nd = n
        
        if n >= 0:
            bc = int(nd / nbc)
            nd = nd - bc * nbc
            bg = int(nd / nbg)
            nd = nd - bg * nbg
        
        temp = bc + bg
        if temp > ld:
            temp = ld
            
        if temp % 2 == 0:
            temp = temp // 2
        else:
            temp = int((temp + 1) / 1.5)
            
        bc = temp
        bg = temp
        nd = n - bc * nbc - bg * nbg
        
        bct = int(nd / nbc)
        bgt = int(nd / nbg)
        
        ndbc = nd - (bc + bct) * nbc - bg * nbg
        ndbg = nd - (bg + bgt) * nbg - bc * nbc
        
        if ndbc < ndbg:
            bc = bc + bct
        else:
            bg = bg + bgt
            
        nd = n - bc * nbc - bg * nbg
        
        while nd < 0:
            bc -= 1
            bg -= 1
            nd = n - bc * nbc - bg * nbg
            
        return bc, bg, nd

    def case_fog(self, n, dc, dg, ld):
        return dc, dg, n

    def case_cloud(self, n, dc, dg, ld):
        if self.amicable(n, ld):
            return 0, 0, n
        
        nbc = dc * dc
        nbg = (dg * dg * self.PI) / 4
        bg = int(n / nbg)
        nd = n - bg * nbg
        bc = int(nd / nbc)
        nd = nd - bc * nbc
        max_bg = bg
        tld = bc + bg
        
        if tld > ld:
            if bg > ld:
                bg = ld
                bc = 0
                nd = n - bg * nbg
            else:
                bg = max_bg
                bc = ld - bg
                nd = n - bc * nbc - bg * nbg
                
        return bc, bg, nd

    def case_sun(self, n, dc, dg, ld):
        g = dc % 6
        h = ld % 5
        
        # Calculate percentage increase and new ld based on g and h values
        percentages = {
            (0, 0): (5, 5), (0, 1): (20, 20), (0, 2): (15, 15),
            (0, 3): (12, 12), (0, 4): (10, 10), (1, 0): (7, 7),
            # ... (similar pattern for other combinations)
        }
        
        percentage, ld_reduction = percentages.get((g, h), (7, 7))  # Default values
        nt = n + ((n * percentage) / 100)
        ldm = ld - ld_reduction
        
        ws = (dc + dg) % 3
        
        if ws == 0:  # rain
            return self.case_rain(int(nt), dc, dg, ldm)
        elif ws == 1:  # wind
            return self.case_wind(int(nt), dc, dg, ldm)
        else:  # cloud
            return self.case_cloud(int(nt), dc, dg, ldm)

    def calculate(self):
        try:
            # Get input values
            n = int(self.n_var.get())
            dc = int(self.dc_var.get())
            dg = int(self.dg_var.get())
            ld = int(self.ld_var.get())
            weather = self.weather_var.get()
            
            # Validate input
            if n > 1000 or ld < 1 or ld > 300:
                self.show_results(-1, -1, n)
                return
                
            if weather not in self.weather_types:
                self.show_results(-1, -1, n)
                return
            
            # Process based on weather
            if weather == "Wind":
                bc, bg, nd = self.case_wind(n, dc, dg, ld)
            elif weather == "Rain":
                bc, bg, nd = self.case_rain(n, dc, dg, ld)
            elif weather == "Sun":
                bc, bg, nd = self.case_sun(n, dc, dg, ld)
            elif weather == "Fog":
                bc, bg, nd = self.case_fog(n, dc, dg, ld)
            else:  # Cloud
                bc, bg, nd = self.case_cloud(n, dc, dg, ld)
            
            self.show_results(bc, bg, nd)
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numeric values")
            
    def show_results(self, bc, bg, nd):
        self.result_text.delete(1.0, tk.END)
        if bc + bg < 0:
            self.result_text.insert(tk.END, f"-1 -1 {nd}")
        else:
            self.result_text.insert(tk.END, f"BC: {bc}\nBG: {bg}\nND: {nd:.3f}")

if __name__ == "__main__":
    root = tk.Window()
    app = WeatherCalculator(root)
    root.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pdf_parser import extract_prices
from excel_handler import read_products, write_prices
from matcher import match_products_to_prices

class PriceFillerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chemical Price Filler Pro")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.pdf_path = None
        self.excel_path = None
        
        # Main Frame
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(main_frame, text="Chemical Price Filler", 
                        font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=(0, 20))
        
        # PDF Section
        pdf_frame = tk.LabelFrame(main_frame, text="PDF Price List", 
                                 font=("Arial", 10, "bold"), bg="#f0f0f0", padx=15, pady=15)
        pdf_frame.pack(fill="x", pady=10)
        
        pdf_btn_frame = tk.Frame(pdf_frame, bg="#f0f0f0")
        pdf_btn_frame.pack(fill="x")
        
        tk.Button(pdf_btn_frame, text="📄 Browse PDF", command=self.browse_pdf, 
                 bg="#4CAF50", fg="white", font=("Arial", 10), width=15, 
                 relief="flat", cursor="hand2").pack(side="left")
        
        self.pdf_label = tk.Label(pdf_btn_frame, text="No file selected", 
                                 fg="gray", bg="#f0f0f0", font=("Arial", 9))
        self.pdf_label.pack(side="left", padx=15)
        
        # Excel Section
        excel_frame = tk.LabelFrame(main_frame, text="Excel File", 
                                   font=("Arial", 10, "bold"), bg="#f0f0f0", padx=15, pady=15)
        excel_frame.pack(fill="x", pady=10)
        
        excel_btn_frame = tk.Frame(excel_frame, bg="#f0f0f0")
        excel_btn_frame.pack(fill="x")
        
        tk.Button(excel_btn_frame, text="📊 Browse Excel", command=self.browse_excel, 
                 bg="#2196F3", fg="white", font=("Arial", 10), width=15, 
                 relief="flat", cursor="hand2").pack(side="left")
        
        self.excel_label = tk.Label(excel_btn_frame, text="No file selected", 
                                   fg="gray", bg="#f0f0f0", font=("Arial", 9))
        self.excel_label.pack(side="left", padx=15)
        
        # Price Mode Section
        mode_frame = tk.LabelFrame(main_frame, text="Price Selection Mode", 
                                  font=("Arial", 10, "bold"), bg="#f0f0f0", padx=15, pady=15)
        mode_frame.pack(fill="x", pady=10)
        
        self.price_mode = tk.StringVar(value="min")
        
        radio_frame = tk.Frame(mode_frame, bg="#f0f0f0")
        radio_frame.pack()
        
        tk.Radiobutton(radio_frame, text="⬇ Minimum Price", variable=self.price_mode, 
                      value="min", bg="#f0f0f0", font=("Arial", 10), 
                      cursor="hand2").pack(side="left", padx=20)
        tk.Radiobutton(radio_frame, text="⬆ Maximum Price", variable=self.price_mode, 
                      value="max", bg="#f0f0f0", font=("Arial", 10), 
                      cursor="hand2").pack(side="left", padx=20)
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill="x", pady=10)
        
        # Process Button
        tk.Button(main_frame, text="🚀 Fill Prices", command=self.process, 
                 bg="#FF5722", fg="white", font=("Arial", 14, "bold"), 
                 height=2, relief="flat", cursor="hand2").pack(fill="x", pady=10)
        
        # Status
        self.status_label = tk.Label(main_frame, text="Ready to process", 
                                    fg="#666", bg="#f0f0f0", font=("Arial", 9))
        self.status_label.pack(pady=5)
    
    def browse_pdf(self):
        self.pdf_path = filedialog.askopenfilename(
            title="Select PDF Price List",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if self.pdf_path:
            filename = self.pdf_path.split('/')[-1]
            self.pdf_label.config(text=f"✓ {filename}", fg="green")
            self.update_status()
    
    def browse_excel(self):
        self.excel_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if self.excel_path:
            filename = self.excel_path.split('/')[-1]
            self.excel_label.config(text=f"✓ {filename}", fg="green")
            self.update_status()
    
    def update_status(self):
        if self.pdf_path and self.excel_path:
            self.status_label.config(text="✓ Ready to fill prices", fg="green")
    
    def process(self):
        if not self.pdf_path or not self.excel_path:
            messagebox.showwarning("Missing Files", 
                                 "Please select both PDF and Excel files")
            return
        
        try:
            # Start progress
            self.progress.start(10)
            self.status_label.config(text="⏳ Extracting prices from PDF...", fg="blue")
            self.root.update()
            
            # Extract prices
            price_data = extract_prices(self.pdf_path)
            
            self.status_label.config(text="⏳ Reading products from Excel...", fg="blue")
            self.root.update()
            
            # Read products
            products = read_products(self.excel_path)
            
            self.status_label.config(text="⏳ Matching products...", fg="blue")
            self.root.update()
            
            # Match
            matched_prices, unmatched = match_products_to_prices(products, price_data)
            
            self.status_label.config(text="⏳ Writing prices to Excel...", fg="blue")
            self.root.update()
            
            # Write prices
            write_prices(self.excel_path, matched_prices, self.price_mode.get())
            
            # Stop progress
            self.progress.stop()
            
            # Show results
            result_msg = f"✅ Process Complete!\n\n"
            result_msg += f"Total Products: {len(products)}\n"
            result_msg += f"Matched: {len(matched_prices)}\n"
            result_msg += f"Unmatched: {len(unmatched)}\n"
            
            if unmatched:
                result_msg += f"\n⚠ Unmatched products:\n"
                result_msg += "\n".join([f"  • {p}" for p in unmatched[:10]])
                if len(unmatched) > 10:
                    result_msg += f"\n  ... and {len(unmatched) - 10} more"
            
            messagebox.showinfo("Success", result_msg)
            self.status_label.config(text="✓ Completed successfully!", fg="green")
            
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")
            self.status_label.config(text="✗ Error occurred", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = PriceFillerApp(root)
    root.mainloop()

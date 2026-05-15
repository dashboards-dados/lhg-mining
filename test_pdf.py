from fpdf import FPDF
import tempfile
import os

pdf = FPDF()
pdf.add_page()
pdf.set_font('Helvetica', 'B', 16)
pdf.cell(0, 10, 'Teste', new_x='LMARGIN', new_y='NEXT')
out = bytes(pdf.output())

# Write to file directly
with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
    pdf.output(tmp.name)
    with open(tmp.name, 'rb') as f:
        out2 = f.read()
    os.unlink(tmp.name)

print(len(out), len(out2))
print(out == out2)

{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "47783ef1-f9e4-4311-ad1f-525976714c68",
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "9704f9f2-60f7-4b43-a5b8-a0155b51ae09",
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "\n",
    "tax_rules = {\n",
    "    \"standard_deduction_old\": 50000,\n",
    "    \"standard_deduction_new\": 75000,\n",
    "\n",
    "    \"slabs_old\": [\n",
    "        { \"limit\": 250000, \"rate\": 0 },\n",
    "        { \"limit\": 500000, \"rate\": 0.05 },\n",
    "        { \"limit\": 1000000, \"rate\": 0.20 },\n",
    "        { \"limit\": 999999999, \"rate\": 0.30 }\n",
    "    ],\n",
    "\n",
    "    \"slabs_new\": [\n",
    "        { \"limit\": 300000, \"rate\": 0 },\n",
    "        { \"limit\": 700000, \"rate\": 0.05 },\n",
    "        { \"limit\": 1000000, \"rate\": 0.10 },\n",
    "        { \"limit\": 1200000, \"rate\": 0.15 },\n",
    "        { \"limit\": 1500000, \"rate\": 0.20 },\n",
    "        { \"limit\": 999999999, \"rate\": 0.30 }\n",
    "    ],\n",
    "\n",
    "    \"rebate_87A_old\": {\n",
    "        \"income_limit\": 500000,\n",
    "        \"rebate_amount\": 12500\n",
    "    },\n",
    "\n",
    "    \"rebate_87A_new\": {\n",
    "        \"income_limit\": 700000,\n",
    "        \"rebate_amount\": 25000\n",
    "    },\n",
    "\n",
    "    \"deductions\": {\n",
    "        \"80C\": {\n",
    "            \"limit\": 150000,\n",
    "            \"description\": \"Life insurance premiums, ELSS, PPF, EPF, home loan principal, tuition fees, etc.\"\n",
    "        },\n",
    "        \"80D\": {\n",
    "            \"limit\": 25000,\n",
    "            \"description\": \"Health insurance premium for self and family (₹50,000 for senior citizens)\"\n",
    "        },\n",
    "        \"80G\": {\n",
    "            \"limit\": \"unlimited\",\n",
    "            \"description\": \"Donations to registered charities (simplified to 100% deduction in prototype)\"\n",
    "        },\n",
    "        \"HRA\": {\n",
    "            \"limit\": \"dynamic\",\n",
    "            \"description\": \"House Rent Allowance — based on rent paid and basic salary (not implemented in prototype)\"\n",
    "        }\n",
    "    }\n",
    "}\n",
    "\n",
    "with open(\"tax_rules.json\", \"w\") as f:\n",
    "    json.dump(tax_rules, f, indent=4)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "3bfa5625-0619-4055-a36f-1216c3f191a7",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "150000\n"
     ]
    }
   ],
   "source": [
    "with open(\"tax_rules.json\") as f:\n",
    "    rules = json.load(f)\n",
    "\n",
    "print(rules[\"deductions\"][\"80C\"][\"limit\"])  # ✅ Output: 150000\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "eb3aedc9-27ee-482a-be21-7de1d5166ffd",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting fpdf\n",
      "  Downloading fpdf-1.7.2.tar.gz (39 kB)\n",
      "  Preparing metadata (setup.py): started\n",
      "  Preparing metadata (setup.py): finished with status 'done'\n",
      "Building wheels for collected packages: fpdf\n",
      "  Building wheel for fpdf (setup.py): started\n",
      "  Building wheel for fpdf (setup.py): finished with status 'done'\n",
      "  Created wheel for fpdf: filename=fpdf-1.7.2-py2.py3-none-any.whl size=40713 sha256=74f5ab2b27420ce4e32e22d9b8a9021c83ea177dc317d432fe553e9e170b0514\n",
      "  Stored in directory: c:\\users\\himan\\appdata\\local\\pip\\cache\\wheels\\6e\\62\\11\\dc73d78e40a218ad52e7451f30166e94491be013a7850b5d75\n",
      "Successfully built fpdf\n",
      "Installing collected packages: fpdf\n",
      "Successfully installed fpdf-1.7.2\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "pip install fpdf\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "07d68ccc-1a48-4e46-9bd4-1d54f257c80a",
   "metadata": {},
   "outputs": [],
   "source": [
    "from fpdf import FPDF\n",
    "\n",
    "def generate_tax_summary_pdf(\n",
    "    filename,\n",
    "    total_income,\n",
    "    total_deductions,\n",
    "    taxable_income,\n",
    "    tax_payable\n",
    "):\n",
    "    pdf = FPDF()\n",
    "    pdf.add_page()\n",
    "\n",
    "    # Title\n",
    "    pdf.set_font(\"Arial\", 'B', 16)\n",
    "    pdf.cell(0, 10, \"Tax Summary Report\", ln=True, align=\"C\")\n",
    "\n",
    "    pdf.ln(10)\n",
    "\n",
    "    # Content font\n",
    "    pdf.set_font(\"Arial\", size=12)\n",
    "\n",
    "    pdf.cell(0, 10, f\"Total Income: ₹{total_income:,}\", ln=True)\n",
    "    pdf.cell(0, 10, f\"Total Deductions: ₹{total_deductions:,}\", ln=True)\n",
    "    pdf.cell(0, 10, f\"Taxable Income: ₹{taxable_income:,}\", ln=True)\n",
    "    pdf.cell(0, 10, f\"Income Tax Payable: ₹{tax_payable:,}\", ln=True)\n",
    "\n",
    "    pdf.ln(20)\n",
    "    pdf.set_font(\"Arial\", 'I', 10)\n",
    "    pdf.cell(0, 10, \"Generated by TaxTime - AI Tax Assistant\", ln=True, align=\"C\")\n",
    "\n",
    "    pdf.output(filename)\n",
    "    print(f\"PDF generated: {filename}\")\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    # Example usage\n",
    "    generate_tax_summary_pdf(\n",
    "        filename=\"Tax_Summary_Report.pdf\",\n",
    "        total_income=1200000,\n",
    "        total_deductions=155000,\n",
    "        taxable_income=1045000,\n",
    "        tax_payable=87250\n",
    "    )\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

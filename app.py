from flask import Flask, request, jsonify, send_file, render_template
from tax_backend import parse_income_input, load_tax_rules, apply_deductions, calculate_tax, generate_tax_summary_pdf

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def homepage():
    return render_template("taxindex.html")

@app.route("/api/tax-summary", methods=["POST"])
def tax_summary():
    data = request.get_json()
    user_input = data.get("text", "")

    parsed = parse_income_input(user_input)
    total_income = sum([
        parsed["salary_income"],
        parsed["freelance_income"],
        parsed["crypto_income"],
        parsed["other_income"]
    ])

    deductions = {
        "80C": 0,
        "donation": parsed["donation"]
    }

    rules = load_tax_rules()
    taxable_income, total_deduction = apply_deductions(total_income, deductions, rules)
    tax_payable = int(calculate_tax(taxable_income, rules))

    filename = "Tax_Summary_Report.pdf"
    generate_tax_summary_pdf(filename, total_income, total_deduction, taxable_income, tax_payable)

    return jsonify({
        "total_income": total_income,
        "total_deductions": total_deduction,
        "taxable_income": taxable_income,
        "tax_payable": tax_payable,
        "pdf": "/download"
    })

@app.route("/download")
def download_pdf():
    return send_file("Tax_Summary_Report.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

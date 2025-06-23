document.getElementById("taxForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const input = document.getElementById("incomeText").value;
  const resultBox = document.getElementById("result");

  console.log("📝 Input submitted:", input);

  resultBox.innerHTML = "⏳ Generating summary...";

  try {
    const res = await fetch("/api/tax-summary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input })
    });

    const data = await res.json();
    console.log("✅ Response received:", data);

    resultBox.innerHTML = `
      <p><strong>Total Income:</strong> ₹${data.total_income.toLocaleString()}</p>
      <p><strong>Total Deductions:</strong> ₹${data.total_deductions.toLocaleString()}</p>
      <p><strong>Taxable Income:</strong> ₹${data.taxable_income.toLocaleString()}</p>
      <p><strong>Tax Payable:</strong> ₹${data.tax_payable.toLocaleString()}</p>
      <a href="${data.pdf}" class="inline-block mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">📄 Download PDF</a>
    `;
  } catch (error) {
    resultBox.innerHTML = "❌ Failed to generate summary.";
    console.error("🚫 Error occurred:", error);
  }
});

document.getElementById("taxForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const input = document.getElementById("incomeText").value;
    const resultBox = document.getElementById("result");

    // Show loading state
    resultBox.innerHTML = `
        <div class="flex items-center justify-center space-x-3 py-6">
            <div class="loading-spinner rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600"></div>
            <span class="text-gray-700">Calculating your tax summary...</span>
        </div>
    `;

    try {
        const res = await fetch("/api/tax-summary", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: input })
        });

        if (!res.ok) throw new Error(await res.text());
        
        const data = await res.json();
        
        // Format results with Indian number formatting
        const formatINR = (num) => new Intl.NumberFormat('en-IN').format(num);
        
        resultBox.innerHTML = `
            <div class="space-y-4">
                <div class="result-item">
                    <span class="result-label">Total Income:</span>
                    <span class="result-value">₹${formatINR(data.total_income)}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Total Deductions:</span>
                    <span class="result-value">₹${formatINR(data.total_deductions)}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Taxable Income:</span>
                    <span class="result-value">₹${formatINR(data.taxable_income)}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Tax Payable:</span>
                    <span class="result-value tax-payable">₹${formatINR(data.tax_payable)}</span>
                </div>
                <div class="pt-4">
                    <a href="${data.pdf}" class="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition">
                        <i class="fas fa-file-pdf mr-2"></i> Download PDF Summary
                    </a>
                </div>
            </div>
        `;
    } catch (error) {
        console.error("Error:", error);
        resultBox.innerHTML = `
            <div class="bg-red-50 text-red-600 p-4 rounded-lg">
                <i class="fas fa-exclamation-circle mr-2"></i>
                Error generating summary: ${error.message}
            </div>
        `;
    }
});

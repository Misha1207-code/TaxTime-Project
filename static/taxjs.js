document.getElementById("taxForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const input = document.getElementById("incomeText").value;
    const resultBox = document.getElementById("result");

    resultBox.innerHTML = `
        <div class="flex items-center justify-center space-x-3 py-6">
            <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600"></div>
            <span class="text-gray-700">Generating your tax summary...</span>
        </div>
    `;

    try {
        const res = await fetch("/api/tax-summary", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: input })
        });

        const data = await res.json();
        
        resultBox.innerHTML = `
            <div class="space-y-4" data-aos="fade-up">
                <div class="flex justify-between items-center border-b pb-2">
                    <span class="font-medium">Total Income:</span>
                    <span class="font-bold">₹${data.total_income.toLocaleString('en-IN')}</span>
                </div>
                <div class="flex justify-between items-center border-b pb-2">
                    <span class="font-medium">Total Deductions:</span>
                    <span class="font-bold">₹${data.total_deductions.toLocaleString('en-IN')}</span>
                </div>
                <div class="flex justify-between items-center border-b pb-2">
                    <span class="font-medium">Taxable Income:</span>
                    <span class="font-bold">₹${data.taxable_income.toLocaleString('en-IN')}</span>
                </div>
                <div class="flex justify-between items-center border-b pb-2">
                    <span class="font-medium">Tax Payable:</span>
                    <span class="font-bold text-red-600">₹${data.tax_payable.toLocaleString('en-IN')}</span>
                </div>
                <div class="pt-4">
                    <a href="${data.pdf}" class="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition">
                        <i class="fas fa-file-pdf mr-2"></i> Download PDF Summary
                    </a>
                </div>
            </div>
        `;
    } catch (error) {
        resultBox.innerHTML = `
            <div class="bg-red-50 text-red-600 p-4 rounded-lg">
                <i class="fas fa-exclamation-circle mr-2"></i>
                Failed to generate summary. Please try again.
            </div>
        `;
        console.error("Error:", error);
    }
});
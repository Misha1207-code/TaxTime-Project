// Navbar Scroll Effect
window.addEventListener('scroll', () => {
  const header = document.querySelector('header');
  header.classList.toggle('scrolled', window.scrollY > 50);
});

// Ripple Effect for Buttons
document.querySelectorAll('.btn-ripple').forEach(btn => {
  btn.addEventListener('click', function(e) {
    const ripple = document.createElement('span');
    ripple.classList.add('ripple-effect');
    
    const rect = this.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = `${size}px`;
    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;
    
    this.appendChild(ripple);
    
    setTimeout(() => {
      ripple.remove();
    }, 600);
  });
});

// Form Submission with Confetti
document.getElementById("taxForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  const input = document.getElementById("incomeText").value;
  const resultBox = document.getElementById("result");

  console.log("📝 Input submitted:", input);

  // Show loading state
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
    console.log("✅ Response received:", data);

    // Show result with animation
    resultBox.innerHTML = `
      <div class="space-y-4" data-aos="fade-up">
        <div class="flex justify-between items-center border-b pb-2">
          <span class="font-medium">Total Income:</span>
          <span class="font-bold">₹${data.total_income.toLocaleString()}</span>
        </div>
        <div class="flex justify-between items-center border-b pb-2">
          <span class="font-medium">Total Deductions:</span>
          <span class="font-bold">₹${data.total_deductions.toLocaleString()}</span>
        </div>
        <div class="flex justify-between items-center border-b pb-2">
          <span class="font-medium">Taxable Income:</span>
          <span class="font-bold">₹${data.taxable_income.toLocaleString()}</span>
        </div>
        <div class="flex justify-between items-center border-b pb-2">
          <span class="font-medium">Tax Payable:</span>
          <span class="font-bold text-red-600">₹${data.tax_payable.toLocaleString()}</span>
        </div>
        <div class="pt-4">
          <a href="${data.pdf}" class="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition">
            <i class="fas fa-file-pdf mr-2"></i> Download PDF Summary
          </a>
        </div>
      </div>
    `;

    // Trigger confetti celebration
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 }
    });

  } catch (error) {
    resultBox.innerHTML = `
      <div class="bg-red-50 text-red-600 p-4 rounded-lg">
        <i class="fas fa-exclamation-circle mr-2"></i>
        Failed to generate summary. Please try again.
      </div>
    `;
    console.error("🚫 Error occurred:", error);
  }
});

// Initialize AOS after dynamic content loads
document.addEventListener('DOMContentLoaded', () => {
  AOS.refresh();
});

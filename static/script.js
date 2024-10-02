document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('voting-form');

    if (form) {
        const sliders = form.querySelectorAll('input[type="range"]');

        sliders.forEach(slider => {
            const outputElement = document.createElement('span');
            slider.parentNode.insertBefore(outputElement, slider.nextSibling);

            function updateSlider() {
                const value = parseInt(slider.value);
                const convertedValue = value - 6; // Convert 1-11 to -5 to 5 scale
                const percent = ((value - 1) / 10) * 100;
                slider.style.background = `linear-gradient(to right, #4CAF50 0%, #4CAF50 ${percent}%, #ddd ${percent}%, #ddd 100%)`;
            }

            slider.addEventListener('input', updateSlider);
            updateSlider();
        });
    } else {
        console.log('Voting form not found on this page');
    }

    // New code for handling report generation progress
    const generateReportBtn = document.getElementById('generate-report-btn');
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const reportContainer = document.getElementById('report');

    if (generateReportBtn) {
        generateReportBtn.addEventListener('click', function(e) {
            e.preventDefault();
            generateReport();
        });
    }

    function generateReport() {
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';
        progressText.textContent = 'Initializing report generation...';
        reportContainer.innerHTML = ''; // Clear any previous report content

        const eventSource = new EventSource('/generate_report');

        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.status === 'complete') {
                eventSource.close();
                progressBar.style.width = '100%';
                progressText.textContent = 'Report generation complete!';
                // Display the generated report
                reportContainer.innerHTML = data.report;
                // Scroll to the report
                reportContainer.scrollIntoView({ behavior: 'smooth' });
            } else {
                const progress = Math.min(99, Math.round(data.progress));
                progressBar.style.width = progress + '%';
                progressText.textContent = `${data.status} (${progress}%)`;
            }
        };

        eventSource.onerror = function(error) {
            console.error('Error:', error);
            eventSource.close();
            progressText.textContent = 'An error occurred while generating the report.';
            reportContainer.innerHTML = '<p class="text-red-600">An error occurred while generating the report. Please try again later.</p>';
        };
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('voting-form');

    if (form) {
        const sliders = form.querySelectorAll('input[type="range"]');

        sliders.forEach(slider => {
            const outputElement = document.createElement('span');
            //outputElement.classList.add('slider-value');
            slider.parentNode.insertBefore(outputElement, slider.nextSibling);

            function updateSlider() {
                const value = parseInt(slider.value);
                const convertedValue = value - 6; // Convert 1-11 to -5 to 5 scale
                const percent = ((value - 1) / 10) * 100;
                slider.style.background = `linear-gradient(to right, #4CAF50 0%, #4CAF50 ${percent}%, #ddd ${percent}%, #ddd 100%)`;
                //outputElement.textContent = convertedValue;
            }

            slider.addEventListener('input', updateSlider);
            // Trigger the input event to set the initial background and value
            updateSlider();
        });
    } else {
        console.log('Voting form not found on this page');
    }
});
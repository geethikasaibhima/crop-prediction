/**
 * Smart Crop Prediction System - Client Script
 * Provides:
 * - Diagnostic connectivity confirmation
 * - Real-time input validation
 * - Instant one-click presets
 * - Safe loading state on submission
 */

console.log("🌱 [Smart Crop] JavaScript is connected and active.");

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('cropForm');
  const submitBtn = document.getElementById('predictBtn');
  const btnSpinner = document.getElementById('btnSpinner');
  const btnText = document.getElementById('btnText');
  const alertContainer = document.getElementById('clientAlert');

  // Realistic sample presets for non-technical users
  const presets = {
    rice: { N: 90, P: 42, K: 43, temperature: 20.9, humidity: 82.0, ph: 6.5, rainfall: 202.9 },
    maize: { N: 71, P: 54, K: 20, temperature: 22.6, humidity: 65.1, ph: 5.7, rainfall: 82.4 },
    cotton: { N: 118, P: 48, K: 22, temperature: 25.1, humidity: 80.3, ph: 6.9, rainfall: 71.3 },
    chickpea: { N: 39, P: 68, K: 79, temperature: 18.9, humidity: 16.9, ph: 7.3, rainfall: 80.1 },
    coffee: { N: 101, P: 29, K: 32, temperature: 26.5, humidity: 58.9, ph: 6.8, rainfall: 158.1 },
    banana: { N: 100, P: 75, K: 50, temperature: 27.3, humidity: 80.3, ph: 5.9, rainfall: 104.9 },
    apple: { N: 24, P: 128, K: 196, temperature: 22.8, humidity: 92.3, ph: 5.9, rainfall: 110.8 }
  };

  // Attach Preset Buttons
  document.querySelectorAll('.preset-chip').forEach(chip => {
    chip.addEventListener('click', (e) => {
      e.preventDefault();
      const cropKey = chip.getAttribute('data-crop');
      const data = presets[cropKey];
      if (data) {
        Object.keys(data).forEach(field => {
          const input = document.getElementById(field);
          if (input) {
            input.value = data[field];
            input.classList.remove('is-invalid');
            const errSpan = document.getElementById(`${field}-error`);
            if (errSpan) errSpan.style.display = 'none';
          }
        });

        if (alertContainer) {
          alertContainer.style.display = 'none';
        }
      }
    });
  });

  // Client-side Validation Logic
  function validateForm() {
    let isValid = true;
    let firstInvalidInput = null;

    const validationRules = [
      { id: 'N', name: 'Nitrogen (N)', min: 0, max: 300 },
      { id: 'P', name: 'Phosphorus (P)', min: 0, max: 300 },
      { id: 'K', name: 'Potassium (K)', min: 0, max: 300 },
      { id: 'temperature', name: 'Temperature', min: -10, max: 60 },
      { id: 'humidity', name: 'Humidity', min: 0, max: 100 },
      { id: 'ph', name: 'Soil pH', min: 0, max: 14 },
      { id: 'rainfall', name: 'Rainfall', min: 0, max: 1000 }
    ];

    validationRules.forEach(rule => {
      const input = document.getElementById(rule.id);
      const errorMsg = document.getElementById(`${rule.id}-error`);
      if (!input) return;

      const valStr = input.value.trim();
      let error = null;

      if (valStr === '') {
        error = `Please enter a valid ${rule.name} value.`;
      } else {
        const val = Number(valStr);
        if (isNaN(val)) {
          error = `${rule.name} must be a number (e.g. 50 or 23.5).`;
        } else if (val < rule.min) {
          if (rule.min === 0) {
            error = `${rule.name} cannot be negative.`;
          } else {
            error = `${rule.name} must be at least ${rule.min}.`;
          }
        } else if (val > rule.max) {
          error = `${rule.name} cannot exceed ${rule.max}.`;
        }
      }

      if (error) {
        isValid = false;
        input.classList.add('is-invalid');
        if (errorMsg) {
          errorMsg.textContent = error;
          errorMsg.style.display = 'block';
        }
        if (!firstInvalidInput) firstInvalidInput = input;
      } else {
        input.classList.remove('is-invalid');
        if (errorMsg) {
          errorMsg.textContent = '';
          errorMsg.style.display = 'none';
        }
      }
    });

    if (!isValid && firstInvalidInput) {
      firstInvalidInput.focus();
    }

    return isValid;
  }

  // Handle Form Submission
  if (form) {
    form.addEventListener('submit', (e) => {
      if (!validateForm()) {
        e.preventDefault();
        return false;
      }

      // Show user visual feedback
      if (btnSpinner) btnSpinner.classList.remove('d-none');
      if (btnText) btnText.textContent = '🌾 Analyzing Soil & Predicting Suitable Crop...';

      // Disable button asynchronously to prevent cancelling browser submit
      if (submitBtn) {
        setTimeout(() => {
          submitBtn.disabled = true;
        }, 10);
      }
    });

    // Real-time input error clearing
    form.querySelectorAll('input').forEach(input => {
      input.addEventListener('input', () => {
        input.classList.remove('is-invalid');
        const errorMsg = document.getElementById(`${input.id}-error`);
        if (errorMsg) errorMsg.style.display = 'none';
      });
    });
  }
});

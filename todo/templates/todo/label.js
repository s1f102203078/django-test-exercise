document.addEventListener('DOMContentLoaded', function() {
  const colorOptions = document.querySelectorAll('.color-option');
  const selectedColorDisplay = document.getElementById('selectedColorDisplay');
  let selectedColor = null;

  colorOptions.forEach(button => {
    button.addEventListener('click', function() {
      colorOptions.forEach(btn => btn.classList.remove('selected'));

      this.classList.add('selected');

      selectedColor = this.dataset.color;
      selectedColorDisplay.textContent = selectedColor;

    });
  });

  if (colorOptions.length > 0) {
    colorOptions[0].click();
  }
});
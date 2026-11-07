document.addEventListener('DOMContentLoaded', () => {
    const quantityControls = document.querySelectorAll(
        '.cart-quantity-control'
    );

    quantityControls.forEach(control => {
        const input = control.querySelector('.cart-quantity-input');
        const decreaseBtn = control.querySelector(
            '[data-action="decrease"]'
        );
        const increaseBtn = control.querySelector(
            '[data-action="increase"]'
        );

        if (!input || !decreaseBtn || !increaseBtn) return;

        const form = control.closest('.cart-quantity-form');

        const min = Number(input.min) || 1;
        const max = Number(input.max);

        // Validate manually entered quantity
        function validateQuantity() {
            const quantity = input.valueAsNumber;

            // Clear previous validation message
            input.setCustomValidity('');

            if (input.value.trim() === '' || !Number.isInteger(quantity)) {
                input.setCustomValidity('Please enter a whole number.');
            } else if (quantity < min) {
                input.setCustomValidity(
                    `Quantity must be at least ${min}.`
                );
            } else if (Number.isFinite(max) && quantity > max) {
                input.setCustomValidity(
                    `Only ${max} units are available.`
                );
            }
        }

        // Adjust quantity using the + and - buttons
        function setQuantity(value) {
            let quantity = Number.isFinite(value) ? Math.floor(value) : min;

            quantity = Math.max(min, quantity);

            if (Number.isFinite(max) && max >= min) {
                quantity = Math.min(quantity, max);
            }

            input.value = quantity;
            validateQuantity();
        }

        decreaseBtn.addEventListener('click', () => {
            const current = input.valueAsNumber;
            setQuantity((Number.isFinite(current) ? current : min) - 1);
        });

        increaseBtn.addEventListener('click', () => {
            const current = input.valueAsNumber;
            setQuantity((Number.isFinite(current) ? current : min) + 1);
        });

        // Validate input without silently changing its value
        input.addEventListener('input', () => {
            // Remove an old success message when the user edits quantity
            document.querySelectorAll('.flash-success').forEach(alert => {
                alert.remove();
            });

            validateQuantity();
        });

        // Prevent invalid form submission
        if (form) {
            form.addEventListener('submit', event => {
                validateQuantity();

                if (!form.checkValidity()) {
                    event.preventDefault();
                    form.reportValidity();
                }
            });
        }
    });
});
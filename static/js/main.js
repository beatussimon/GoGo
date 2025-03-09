document.addEventListener('DOMContentLoaded', () => {
    // Confetti on M-Pesa success
    const payButtons = document.querySelectorAll('.pay-btn');
    payButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (e.target.form.checkValidity()) {
                setTimeout(() => {
                    const canvas = document.createElement('canvas');
                    canvas.className = 'fixed inset-0 pointer-events-none z-30';
                    document.body.appendChild(canvas);
                    const ctx = canvas.getContext('2d');
                    canvas.width = window.innerWidth;
                    canvas.height = window.innerHeight;
                    for (let i = 0; i < 100; i++) {
                        ctx.fillStyle = ['#00A859', '#FFC107', '#FFFFFF'][Math.floor(Math.random() * 3)];
                        const x = Math.random() * canvas.width;
                        const y = Math.random() * canvas.height;
                        ctx.beginPath();
                        ctx.arc(x, y, 3, 0, Math.PI * 2);
                        ctx.fill();
                    }
                    setTimeout(() => canvas.remove(), 1500);
                }, 500);
            }
        });
    });

    // Staggered animations
    document.querySelectorAll('.trip-card, .post, .message').forEach((el, i) => {
        setTimeout(() => el.style.opacity = '1', i * 150);
    });
});
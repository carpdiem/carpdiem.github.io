document.addEventListener('DOMContentLoaded', () => {
    let tapCount = 0;
    let lastTap = 0;
    const TRIPLE_TAP_DELAY = 500; // Milliseconds

    document.body.addEventListener('touchend', () => {
        const now = new Date().getTime();
        const timeSinceLastTap = now - lastTap;

        if (timeSinceLastTap < TRIPLE_TAP_DELAY && timeSinceLastTap > 0) {
            tapCount++;
        } else {
            tapCount = 1;
        }

        lastTap = now;

        if (tapCount === 3) {
            window.location.reload();
        }
    });
});

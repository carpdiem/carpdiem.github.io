document.addEventListener('DOMContentLoaded', () => {
    let tapCount = 0;
    let lastTapTime = 0;
    let lastTapPosition = { x: 0, y: 0 };
    const TRIPLE_TAP_DELAY = 300; // Milliseconds
    const TAP_RADIUS = 75; // Pixels

    document.body.addEventListener('touchend', (event) => {
        const now = new Date().getTime();
        const touch = event.changedTouches[0];
        const currentTapPosition = { x: touch.clientX, y: touch.clientY };

        const timeSinceLastTap = now - lastTapTime;
        const dx = currentTapPosition.x - lastTapPosition.x;
        const dy = currentTapPosition.y - lastTapPosition.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (timeSinceLastTap < TRIPLE_TAP_DELAY && distance < TAP_RADIUS) {
            tapCount++;
        } else {
            tapCount = 1;
        }

        lastTapTime = now;
        lastTapPosition = currentTapPosition;

        if (tapCount === 3) {
            window.location.reload();
        }
    });
});

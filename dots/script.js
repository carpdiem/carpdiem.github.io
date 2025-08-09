document.addEventListener('DOMContentLoaded', () => {
    // 1. SETUP
    const canvas = document.getElementById('dotsCanvas');
    const ctx = canvas.getContext('2d');

    // Set canvas size to fill the window
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    const { width, height } = canvas.getBoundingClientRect();

    // Adjust for device pixel ratio for a sharp canvas
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.scale(dpr, dpr);

    // 2. CONFIGURATION
    const DOT_DIAMETER_MM = 8;
    const DPI = 96 * (window.devicePixelRatio || 1); // Approximate device DPI
    const DOT_DIAMETER_INCHES = DOT_DIAMETER_MM / 25.4;
    const dotRadius = (DOT_DIAMETER_INCHES * DPI) / (2 * dpr); // Final dot radius in logical pixels

    // Dynamically determine dot count based on screen area
    const DOT_DENSITY_FACTOR = 60000; // Lower number = more dots per area
    const screenArea = width * height;
    const targetDotCount = Math.floor(screenArea / DOT_DENSITY_FACTOR);

    // Generate a random number of dots centered around the target
    const getDotCount = () => {
        const min = Math.max(1, Math.floor(targetDotCount * 0.5));
        const max = Math.ceil(targetDotCount * 1.5);
        const r1 = Math.floor(Math.random() * (max - min + 1)) + min;
        const r2 = Math.floor(Math.random() * (max - min + 1)) + min;
        return Math.floor((r1 + r2) / 2);
    };

    const numDots = getDotCount();
    const dots = [];
    const MAX_ATTEMPTS = 100; // Prevents infinite loops on crowded screens

    // 3. LOGIC: Non-overlapping placement
    for (let i = 0; i < numDots; i++) {
        let attempts = 0;
        while (attempts < MAX_ATTEMPTS) {
            // Define a margin to keep dots from the edge (1 diameter buffer + dot radius)
            const margin = (dotRadius * 2) + dotRadius;
            const safeAreaWidth = width - 2 * margin;
            const safeAreaHeight = height - 2 * margin;

            const newDot = {
                x: Math.random() * safeAreaWidth + margin,
                y: Math.random() * safeAreaHeight + margin,
                radius: dotRadius
            };

            let hasOverlap = false;
            for (const existingDot of dots) {
                const dx = newDot.x - existingDot.x;
                const dy = newDot.y - existingDot.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < newDot.radius + existingDot.radius + 5) { // Add small buffer
                    hasOverlap = true;
                    break;
                }
            }

            if (!hasOverlap) {
                dots.push(newDot);
                break;
            }
            attempts++;
        }
    }

    // 4. DRAWING
    ctx.fillStyle = '#111111';
    dots.forEach(dot => {
        ctx.beginPath();
        ctx.arc(dot.x, dot.y, dot.radius, 0, Math.PI * 2);
        ctx.fill();
    });
});
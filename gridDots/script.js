document.addEventListener('DOMContentLoaded', () => {
    // 1. SETUP (Identical to dots.js)
    const canvas = document.getElementById('dotsCanvas');
    const ctx = canvas.getContext('2d');
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    const { width, height } = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.scale(dpr, dpr);

    // 2. CONFIGURATION (Adapted for grid logic)
    const DOT_DIAMETER_MM = 8;
    const DPI = 96 * (window.devicePixelRatio || 1);
    const DOT_DIAMETER_INCHES = DOT_DIAMETER_MM / 25.4;
    const dotRadius = (DOT_DIAMETER_INCHES * DPI) / (2 * dpr);

    // Set max grid dimension based on screen size
    const isMobile = width < 768;
    const MAX_GRID_DIM = isMobile ? 5 : 12;

    // 3. LOGIC: Grid Calculation
    // Define a margin to keep dots from the edge
    const margin = (dotRadius * 2) + dotRadius;
    const safeAreaWidth = width - 2 * margin;
    const safeAreaHeight = height - 2 * margin;

    // Randomize the internal spacing of the grid for more variability
    const spacingMultiplierX = 1.5 + Math.random() * 2.5; // Spacing is 1.5x to 4x dot diameter
    const spacingMultiplierY = 1.5 + Math.random() * 2.5;
    const xSpacing = dotRadius * 2 * spacingMultiplierX;
    const ySpacing = dotRadius * 2 * spacingMultiplierY;

    // Determine max possible grid dimensions based on spacing
    const max_x_count = Math.min(MAX_GRID_DIM, Math.floor(safeAreaWidth / xSpacing) + 1);
    const max_y_count = Math.min(MAX_GRID_DIM, Math.floor(safeAreaHeight / ySpacing) + 1);

    // Choose random grid dimensions
    const x_count = Math.floor(Math.random() * (max_x_count - 2 + 1)) + 2;
    const y_count = Math.floor(Math.random() * (max_y_count - 2 + 1)) + 2;

    // Calculate the total size of the grid block
    const gridWidth = (x_count - 1) * xSpacing;
    const gridHeight = (y_count - 1) * ySpacing;

    // Randomly position the entire grid block within the safe area
    const offsetX = margin + Math.random() * (safeAreaWidth - gridWidth);
    const offsetY = margin + Math.random() * (safeAreaHeight - gridHeight);

    // 4. DRAWING
    ctx.fillStyle = '#111111';
    for (let y = 0; y < y_count; y++) {
        for (let x = 0; x < x_count; x++) {
            const dotX = offsetX + x * xSpacing;
            const dotY = offsetY + y * ySpacing;
            ctx.beginPath();
            ctx.arc(dotX, dotY, dotRadius, 0, Math.PI * 2);
            ctx.fill();
        }
    }
});

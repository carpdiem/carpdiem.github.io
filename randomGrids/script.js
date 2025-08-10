document.addEventListener('DOMContentLoaded', () => {
    // 1. SETUP
    const canvas = document.getElementById('dotsCanvas');
    const ctx = canvas.getContext('2d');
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    const { width, height } = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.scale(dpr, dpr);

    // 2. CONFIGURATION
    const DOT_DIAMETER_MM = 8;
    const DPI = 96 * (window.devicePixelRatio || 1);
    const DOT_DIAMETER_INCHES = DOT_DIAMETER_MM / 25.4;
    const dotRadius = (DOT_DIAMETER_INCHES * DPI) / (2 * dpr);
    const isMobile = width < 768;
    const MAX_GRID_DIM = isMobile ? 5 : 12;

    // 3. LOGIC
    // Define a margin to keep dots from the edge
    const margin = (dotRadius * 2) + dotRadius;
    const safeAreaWidth = width - 2 * margin;
    const safeAreaHeight = height - 2 * margin;

    // Randomize the internal spacing (vector magnitudes)
    const xSpacing = dotRadius * 2 * (1.5 + Math.random() * 2.5);
    const ySpacing = dotRadius * 2 * (1.5 + Math.random() * 2.5);

    // Generate two random basis vectors
    const angle1 = Math.random() * 2 * Math.PI;
    const v_x = { x: Math.cos(angle1) * xSpacing, y: Math.sin(angle1) * xSpacing };

    const skewDirection = Math.random() > 0.5 ? 1 : -1;
    const skewAngle = (Math.PI / 4 + Math.random() * Math.PI / 2) * skewDirection; // 45 to 135 deg, either direction
    const angle2 = angle1 + skewAngle;
    const v_y = { x: Math.cos(angle2) * ySpacing, y: Math.sin(angle2) * ySpacing };

    // Start with a candidate grid size and iteratively check if it fits.
    let x_count = Math.floor(Math.random() * MAX_GRID_DIM) + 1;
    let y_count = Math.floor(Math.random() * MAX_GRID_DIM) + 1;
    let dotPositions, minX, minY, maxX, maxY, boundingBoxWidth, boundingBoxHeight;

    while (x_count > 0 && y_count > 0) {
        // Prevent 1x1 grids
        if (x_count === 1 && y_count === 1) {
            if (Math.random() > 0.5) x_count++; else y_count++;
            if (x_count > MAX_GRID_DIM) x_count = MAX_GRID_DIM;
            if (y_count > MAX_GRID_DIM) y_count = MAX_GRID_DIM;
        }

        // Calculate all dot positions relative to (0,0) and find the bounding box
        dotPositions = [];
        minX = Infinity; minY = Infinity; maxX = -Infinity; maxY = -Infinity;
        for (let j = 0; j < y_count; j++) {
            for (let i = 0; i < x_count; i++) {
                const pos = { x: i * v_x.x + j * v_y.x, y: i * v_x.y + j * v_y.y };
                dotPositions.push(pos);
                if (pos.x < minX) minX = pos.x;
                if (pos.x > maxX) maxX = pos.x;
                if (pos.y < minY) minY = pos.y;
                if (pos.y > maxY) maxY = pos.y;
            }
        }

        boundingBoxWidth = maxX - minX;
        boundingBoxHeight = maxY - minY;

        if ((boundingBoxWidth + dotRadius * 2) <= safeAreaWidth && (boundingBoxHeight + dotRadius * 2) <= safeAreaHeight) {
            break; // This grid fits, so we're done.
        }

        // If it doesn't fit, shrink the grid and try again.
        if (boundingBoxWidth > safeAreaWidth) x_count--;
        if (boundingBoxHeight > safeAreaHeight) y_count--;
    }

    // Calculate the final placement offset
    const offsetX = margin - minX + Math.random() * (safeAreaWidth - boundingBoxWidth);
    const offsetY = margin - minY + Math.random() * (safeAreaHeight - boundingBoxHeight);

    // 4. DRAWING
    ctx.fillStyle = '#111111';
    dotPositions.forEach(pos => {
        ctx.beginPath();
        ctx.arc(pos.x + offsetX, pos.y + offsetY, dotRadius, 0, Math.PI * 2);
        ctx.fill();
    });
});

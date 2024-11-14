const canvas = document.getElementById('latticeCanvas');
const ctx = canvas.getContext('2d');
const gridSize = 20;
const treasurePoint = { x: 5, y: 8 };

function drawGrid(vector1, vector2) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the lattice points
    ctx.fillStyle = '#4b0082';
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    for (let i = -15; i <= 15; i++) {
        for (let j = -15; j <= 15; j++) {
            const x = centerX + (i * vector1.x + j * vector2.x) * gridSize;
            const y = centerY - (i * vector1.y + j * vector2.y) * gridSize;
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, 2 * Math.PI);
            ctx.fill();
        }
    }

    // Draw the treasure point as a target
    ctx.fillStyle = '#ffcc00';
    const treasureScreenX = centerX + treasurePoint.x * gridSize;
    const treasureScreenY = centerY - treasurePoint.y * gridSize;
    ctx.beginPath();
    ctx.arc(treasureScreenX, treasureScreenY, 8, 0, 2 * Math.PI);
    ctx.fill();
    ctx.strokeStyle = '#ffa500';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw the basis vectors
    ctx.strokeStyle = '#ff33cc';
    ctx.lineWidth = 2;

    // Vector 1
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX + vector1.x * gridSize, centerY - vector1.y * gridSize);
    ctx.stroke();
    ctx.fillText(`Vektor 1 (${vector1.x}, ${vector1.y})`, centerX + vector1.x * gridSize + 5, centerY - vector1.y * gridSize - 5);

    // Vector 2
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX + vector2.x * gridSize, centerY - vector2.y * gridSize);
    ctx.stroke();
    ctx.fillText(`Vektor 2 (${vector2.x}, ${vector2.y})`, centerX + vector2.x * gridSize + 5, centerY - vector2.y * gridSize - 5);
}

document.getElementById('updateGrid').addEventListener('click', () => {
    const vector1 = {
        x: parseInt(document.getElementById('vector1x').value, 10),
        y: parseInt(document.getElementById('vector1y').value, 10)
    };
    const vector2 = {
        x: parseInt(document.getElementById('vector2x').value, 10),
        y: parseInt(document.getElementById('vector2y').value, 10)
    };

    drawGrid(vector1, vector2);

    // Send data to the server for validation
    fetch('/validate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ vector1, vector2 })
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = data.message;
        messageDiv.style.color = data.success ? 'green' : 'red';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Initial draw
drawGrid({ x: 2, y: 1 }, { x: 1, y: 3 });


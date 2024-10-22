document.getElementById('createRuleBtn').addEventListener('click', async () => {
    const ruleInput = document.getElementById('ruleInput').value;
    try {
        const response = await fetch('/create_rule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rule_string: ruleInput })
        });
        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }
        const result = await response.json();
        document.getElementById('output').innerText = JSON.stringify(result);
    } catch (error) {
        document.getElementById('output').innerText = `Create Rule Failed: ${error.message}`;
    }
});

document.getElementById('combineRulesBtn').addEventListener('click', async () => {
    const ruleIdsInput = document.getElementById('ruleIdsInput').value;
    const ruleIds = ruleIdsInput.split(',').map(id => id.trim());
    try {
        const response = await fetch('/combine_rules', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rule_ids: ruleIds })
        });
        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }
        const result = await response.json();
        document.getElementById('output').innerText = JSON.stringify(result);
    } catch (error) {
        document.getElementById('output').innerText = `Combine Rules Failed: ${error.message}`;
    }
});

document.getElementById('evaluateRuleBtn').addEventListener('click', async () => {
    const ruleId = document.getElementById('ruleIdInput').value;
    const dataInput = document.getElementById('dataInput').value;
    let data;
    try {
        data = JSON.parse(dataInput);
    } catch (error) {
        document.getElementById('output').innerText = `Invalid JSON: ${error.message}`;
        return;
    }
    
    try {
        const response = await fetch('/evaluate_rule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rule_id: ruleId, data: data })
        });
        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }
        const result = await response.json();
        document.getElementById('output').innerText = JSON.stringify(result);
    } catch (error) {
        document.getElementById('output').innerText = `Evaluate Rule Failed: ${error.message}`;
    }
});
const canvas = document.getElementById('gradientCanvas');
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;
        const points = [
      { x: 100, y: 300, color: 'rgba(148,238,144,0.8)', radius: 400, dx: 1, dy: 1.2 },
      { x: 300, y: 600, color: 'rgba(255,192,203, 0.5)', radius: 500, dx: 1, dy: 1.2 },
      { x: 800, y: 400, color: 'rgba(255, 255, 0, 0.5)', radius: 350, dx: -1, dy: -1 },
      { x: 400, y: 700, color: 'rgb(255,192,203,0.5)', radius: 450, dx: 1.5, dy: -0.8 }
    ];

    function drawGradient() {
      ctx.clearRect(0, 0, width, height);
      points.forEach(point => {
        const gradient = ctx.createRadialGradient(point.x, point.y, 0, point.x, point.y, point.radius);
        gradient.addColorStop(0, point.color);
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

        ctx.beginPath();
        ctx.arc(point.x, point.y, point.radius, 0, Math.PI * 2);
        ctx.fillStyle = gradient;
        ctx.fill();
      });
    }

    function updatePoints() {
      points.forEach(point => {
        point.x += point.dx;
        point.y += point.dy;

        if (point.x < 0 || point.x > width) point.dx *= -1;
        if (point.y < 0 || point.y > height) point.dy *= -1;
      });
    }

    function animate() {
      updatePoints();
      drawGradient();
      requestAnimationFrame(animate);
    }

    animate();
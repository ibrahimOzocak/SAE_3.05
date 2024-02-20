const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const shapes = [];
let selectedShape = null;

function addShape(type) {
  const x = 150;
  const y = 150;
  const size = document.getElementById('sizeSlider').value;
  const color = document.getElementById('colorPicker').value;

  ctx.fillStyle = color;

  if (type === 'circle') {
    ctx.beginPath();
    ctx.arc(x, y, size, 0, 2 * Math.PI);
    ctx.fill();
  } else if (type === 'square') {
    ctx.fillRect(x - size, y - size, size * 2, size * 2);
  } else if (type === 'rectangle') {
    ctx.fillRect(x - size, y - size, size * 3, size * 2);
  }

  shapes.push({ type, x, y, size, color });
}

function removeLastShape() {
  shapes.pop();
  selectedShape = null;
  redrawCanvas();
}

function addText() {
  const text = document.getElementById('textInput').value;
  const x = 150;
  const y = 150;

  ctx.fillStyle = 'black';
  ctx.font = '14px Arial';
  ctx.fillText(text, x, y);

  shapes.push({ type: 'text', x, y, text });
}

function handleMouseDown(event) {
  const mouseX = event.clientX - canvas.getBoundingClientRect().left;
  const mouseY = event.clientY - canvas.getBoundingClientRect().top;

  for (let i = shapes.length - 1; i >= 0; i--) {
    const shape = shapes[i];
    if (isPointInsideShape(mouseX, mouseY, shape)) {
      selectedShape = shape;
      return;
    }
  }

  selectedShape = null;
}

function handleMouseUp() {
  selectedShape = null;
}

function handleMouseMove(event) {
  if (selectedShape) {
    const mouseX = event.clientX - canvas.getBoundingClientRect().left;
    const mouseY = event.clientY - canvas.getBoundingClientRect().top;

    selectedShape.x = mouseX;
    selectedShape.y = mouseY;

    redrawCanvas();
  }
}

function isPointInsideShape(x, y, shape) {
  if (shape.type === 'circle') {
    const distance = Math.sqrt((x - shape.x) ** 2 + (y - shape.y) ** 2);
    return distance <= shape.size;
  } else if (shape.type === 'square' || shape.type === 'rectangle') {
    return x >= shape.x - shape.size && x <= shape.x - (-shape.size) &&
           y >= shape.y - shape.size && y <= shape.y - (-shape.size);
  } else if (shape.type === 'text') {
    const textWidth = ctx.measureText(shape.text).width;
    const textHeight = parseInt(ctx.font, 10);
    return x >= shape.x && x <= shape.x + textWidth &&
           y >= shape.y - textHeight && y <= shape.y;
  }

  return false;
}

function redrawCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (const shape of shapes) {
    ctx.fillStyle = shape.color || 'black';

    if (shape.type === 'circle') {
      ctx.beginPath();
      ctx.arc(shape.x, shape.y, shape.size, 0, 2 * Math.PI);
      ctx.fill();
    } else if (shape.type === 'square') {
      ctx.fillRect(shape.x - shape.size, shape.y - shape.size, shape.size * 2, shape.size * 2);
    } else if (shape.type === 'rectangle') {
      ctx.fillRect(shape.x - shape.size, shape.y - shape.size, shape.size * 3, shape.size * 2);
    } else if (shape.type === 'text') {
      ctx.fillStyle = 'black';
      ctx.font = '14px Arial';
      ctx.fillText(shape.text, shape.x, shape.y);
    }
  }
}

function downloadPDF() {
  const element = document.getElementById('dessin');
  html2pdf(element);
}

canvas.addEventListener('mousedown', handleMouseDown);
canvas.addEventListener('mouseup', handleMouseUp);
canvas.addEventListener('mousemove', handleMouseMove);
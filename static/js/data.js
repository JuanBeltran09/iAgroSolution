// Función para almacenar datos
const form = document.getElementById('data-form');
const dataList = document.getElementById('data-list');

form.addEventListener('submit', function(event) {
    event.preventDefault();

    const product = document.getElementById('product').value;
    const origin = document.getElementById('origin').value;
    const logistics = document.getElementById('logistics').value;
    const status = document.getElementById('status').value;

    const listItem = document.createElement('li');
    listItem.textContent = `Producto: ${product}, Origen: ${origin}, Movimiento: ${logistics}, Estado: ${status}`;
    
    dataList.appendChild(listItem);

    // Limpiar el formulario
    form.reset();
});

// Función para analizar datos
document.getElementById('analyze-button').addEventListener('click', function() {
    const analysisOutput = document.getElementById('analysis-output');
    const items = dataList.children;
    
    if (items.length === 0) {
        analysisOutput.textContent = "No hay datos para analizar.";
        return;
    }

    // Simulación de análisis
    let inTransit = 0;
    for (let i = 0; i < items.length; i++) {
        if (items[i].textContent.includes('En tránsito')) {
            inTransit++;
        }
    }

    analysisOutput.textContent = `Se encontraron ${inTransit} productos en tránsito.`;
});

// Función para predicción simple
document.getElementById('predict-button').addEventListener('click', function() {
    const predictionOutput = document.getElementById('prediction-output');
    const items = dataList.children;

    if (items.length === 0) {
        predictionOutput.textContent = "No hay datos para hacer una predicción.";
        return;
    }

    // Simulación de predicción simple
    const randomOutcome = Math.random() < 0.5 ? "Todo está en buen estado" : "Se han detectado posibles problemas de calidad.";
    
    predictionOutput.textContent = `Predicción: ${randomOutcome}`;
});

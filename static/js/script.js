document.getElementById("upload-form").onsubmit = async function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const response = await fetch("/predict", {
        method: "POST",
        body: formData,
    });

    const resultDiv = document.getElementById("result");
    if (response.ok) {
        const data = await response.json();
        resultDiv.innerHTML = `
            <h3>Prediction Result</h3>
            <p><strong>Crop:</strong> ${data.crop_name}</p>
            <p><strong>Disease:</strong> ${data.disease_name}</p>
            <p><strong>Solution:</strong> ${data.solution}</p>
        `;
    } else {
        resultDiv.innerHTML = `<p>Error: Unable to predict</p>`;
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#upload-form');
    const fileUpload = document.querySelector('#file-upload');
    const outputDiv = document.querySelector('#output-div');
    const downloadLink = document.querySelector('#download-link');

    form.addEventListener('submit', (event) => {
        event.preventDefault();

        const file = fileUpload.files[0];
        const formData = new FormData();
        formData.append('file', file);

        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const outputFilename = data.output_filename;
            downloadLink.href = outputFilename;
            downloadLink.style.display = 'block';
            outputDiv.style.display = 'block';
        })
        .catch(error => console.error(error));
    });
});
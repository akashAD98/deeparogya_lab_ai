// // static/script.js
// document.getElementById('uploadForm').addEventListener('submit', function(event) {
//     event.preventDefault();
//     const formData = new FormData(this);

//     fetch('/uploadfile/', {
//         method: 'POST',
//         body: formData,
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById('responseArea').innerText = 'File uploaded successfully. Here is the response: ' + JSON.stringify(data, null, 2);
//     })
//     .catch(error => {
//         document.getElementById('responseArea').innerText = 'Error processing your file.';
//     });
// });





// // static/script.js

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Disable the submit button and show loading message
    const submitButton = document.getElementById('submitBtn');
    submitButton.disabled = true;
    submitButton.innerText = 'Uploading...';

    // Show the loading message
    const loadingIndicator = document.getElementById('loading');
    loadingIndicator.style.display = 'block';

    // Hide response area and back button initially
    const responseArea = document.getElementById('responseArea');
    responseArea.innerHTML = '';
    document.getElementById('backButton').style.display = 'none';

    const formData = new FormData(this);

    fetch('/uploadfile/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Hide the loading indicator
        loadingIndicator.style.display = 'none';

        // Show the response
        responseArea.innerHTML = `<pre>File uploaded successfully. Here is the response: ${JSON.stringify(data, null, 2)}</pre>`;

        // Show the back button
        document.getElementById('backButton').style.display = 'inline-block';
    })
    .catch(error => {
        loadingIndicator.style.display = 'none';
        responseArea.innerHTML = 'Error processing your file. Please try again.';
    })
    .finally(() => {
        // Re-enable the submit button
        submitButton.disabled = false;
        submitButton.innerText = 'Upload';
    });
});

// Function to reset the form and go back to the initial state
function resetForm() {
    document.getElementById('uploadForm').reset(); // Clear the form input
    document.getElementById('responseArea').innerHTML = ''; // Clear the response area
    document.getElementById('backButton').style.display = 'none'; // Hide back button
}

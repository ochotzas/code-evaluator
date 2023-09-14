// Initialize CodeMirror
const codeEditor = CodeMirror.fromTextArea(document.getElementById("code"), {
    mode: "python",
    theme: "base16-light",
    lineNumbers: true,
    autofocus: true
});

// Add border radius to CodeMirror wrapper element
codeEditor.getWrapperElement().style.borderRadius = '8px';

// Define constants for elements
const form = document.getElementById('code-form');
const resultDiv = document.getElementById('result');
const evaluateBtn = document.getElementById('evaluate-btn');
const loader = document.getElementById('loader');
const expectedOutputTextarea = document.getElementById('expected-output');
const fileInput = document.getElementById('file-input');
const clearFileBtn = document.getElementById('clear-file-btn');

// Initialize expectedFileOutput variable
let expectedFileOutput = null;

// Function to load content from a file
const loadFileContent = (file) => {
    const reader = new FileReader();

    reader.onload = (event) => {
        expectedFileOutput = event.target.result;
        expectedOutputTextarea.value = ''; // Clear the manual input
        expectedOutputTextarea.setAttribute('disabled', 'true'); // Disable manual input
    };

    reader.readAsText(file);
};

// Event listener for file input
fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        loadFileContent(file);
    }
});

// Clear file input when the clear button is clicked
clearFileBtn.addEventListener('click', () => {
    fileInput.value = '';
    expectedOutputTextarea.removeAttribute('disabled'); // Enable manual input
    expectedOutputTextarea.value = ''; // Clear the text area
    expectedFileOutput = null; // Clear expectedFileOutput
});

// Function to parse and style the diff content
const parseAndStyleDiff = (diffContent) => {
    return diffContent
        .split('\n')
        .map((line) => {
            if (line.startsWith('---') || line.startsWith('+++') || line.startsWith('@@')) {
                return `<span class="header-line text-blue-500">${line}</span>`;
            } else if (line.startsWith('-')) {
                return `<span class="removed-line text-red-500">${line}</span>`;
            } else if (line.startsWith('+')) {
                return `<span class="added-line text-green-500">${line}</span>`;
            } else {
                return `<span>${line}</span>`;
            }
        })
        .join('<br>');
};

// Event listener for form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Remove previous response
    resultDiv.innerHTML = '';

    // Disable textareas and button, show loading indicator
    document.getElementById('code').setAttribute('disabled', 'true');
    expectedOutputTextarea.setAttribute('disabled', 'true');
    evaluateBtn.setAttribute('disabled', 'true');
    loader.classList.remove('hidden');

    const code = document.getElementById('code').value;
    const expectedOutput = expectedFileOutput || expectedOutputTextarea.value;

    try {
        const response = await fetch('http://localhost:8080/evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code,
                expected_output: expectedOutput,
            }),
        });

        const data = await response.json();

        // Enable textareas and button, hide loading indicator
        document.getElementById('code').removeAttribute('disabled');
        expectedOutputTextarea.removeAttribute('disabled');
        evaluateBtn.removeAttribute('disabled');
        loader.classList.add('hidden');
        fileInput.value = ''; // Clear file input
        expectedFileOutput = null; // Clear expectedFileOutput

        const actualOutput = data.actual_output ? `
                <div class="mt-4">
                    <p class="text-gray-700 font-medium">Actual Output:</p>
                    <div class="bg-gray-400 text-white rounded-lg p-2 font-sans max-h-24 overflow-y-auto">
                        <pre class="diff-content">${parseAndStyleDiff(data.actual_output)}</pre>
                    </div>
                </div>
            ` : '';

        const expectedOutputDiv = data.expected_output ? `
                <div class="mt-4">
                    <p class="text-gray-700 font-medium">Expected Output:</p>
                    <div class="bg-gray-400 text-white rounded-lg p-2 font-sans max-h-24 overflow-y-auto">
                        <pre class="diff-content">${parseAndStyleDiff(data.expected_output)}</pre>
                    </div>
                </div>
            ` : '';

        const diff = data.diff ? `
                <div class="mt-4 border rounded-lg p-2">
                    <p class="text-gray-700 font-medium">Difference:</p>
                    <div class="bg-gray-100 text-black rounded-lg p-2 font-mono max-h-24 overflow-y-auto">
                        <pre class="diff-content">${parseAndStyleDiff(data.diff)}</pre>
                    </div>
                </div>
            ` : '';

        const errorMessage = data.error_message ? `
                <div class="mt-4">
                    <p class="text-gray-700 font-medium">Error message:</p>
                    <div class="relative">
                        <span class="tooltiptext">${data.error_message}</span>
                    </div>
                </div>
            ` : '';

        // Display result
        const resultDivContent = `
                <div class="p-4 text-${data.success ? 'green' : 'red'}-800 rounded-lg">
                    <h2 class="text-lg font-bold">${data.success ? 'Success!' : 'Error'}</h2>
                    <p class="mt-2">${data.message}</p>
                    ${actualOutput !== '' ? actualOutput : ''}
                    ${expectedOutputDiv !== '' ? expectedOutputDiv : ''}
                    ${diff !== '' ? diff : ''}
                    ${errorMessage !== '' ? errorMessage : ''}
                </div>
            `;

        resultDiv.innerHTML = resultDivContent;
    } catch (error) {
        console.error(error);
    }
});
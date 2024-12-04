document.addEventListener('DOMContentLoaded', () => {
    const dynamicContent = document.getElementById('dynamicContent');
    const textInput = document.getElementById('text-to-encrypt');
    const passkeyInput = document.getElementById('passkey');

    const btnEncryptDecrypt = document.getElementById('btnEncryptDecrypt');
    const btnImageOptions = document.getElementById('btnImageOptions');
    const btnOption3 = document.getElementById('btnOption3');
    const btnOption4 = document.getElementById('btnOption4');

    const tabEncrypt = document.getElementById('tabEncrypt');
    const tabDecrypt = document.getElementById('tabDecrypt');

    let currentMode = 'encrypt'; // Default mode is Encrypt

    /**
     * Clear all dynamic content.
     */
    const clearDynamicContent = () => {
        dynamicContent.innerHTML = '';
    };

    /**
     * Switch between Encrypt and Decrypt modes.
     * @param {string} mode - 'encrypt' or 'decrypt'
     */
    const switchTab = (mode) => {
        currentMode = mode;

        // Toggle active tab styling
        tabEncrypt.classList.toggle('active', mode === 'encrypt');
        tabDecrypt.classList.toggle('active', mode === 'decrypt');

        // Update placeholder for text input
        textInput.placeholder = mode === 'encrypt'
            ? 'Enter text to Encrypt here...'
            : 'Enter text to Decrypt here...';

        // Reset text input visibility for Stegano-specific behavior
        textInput.style.display = 'block';

        clearDynamicContent(); // Clear dynamic content
    };

    // Attach event listeners for tab switching
    tabEncrypt.addEventListener('click', () => switchTab('encrypt'));
    tabDecrypt.addEventListener('click', () => switchTab('decrypt'));

    /**
     * Button 1: ASCII Encrypt/Decrypt
     */
    btnEncryptDecrypt.addEventListener('click', () => {
        clearDynamicContent();

        // Create results field
        const resultField = document.createElement('textarea');
        resultField.rows = 5;
        resultField.placeholder = `ASCII ${currentMode} results...`;
        resultField.readOnly = true;

        dynamicContent.appendChild(resultField);
    });

    /**
     * Button 2: Stegano Encrypt/Decrypt
     */
    btnImageOptions.addEventListener('click', () => {
        clearDynamicContent();

        if (currentMode === 'encrypt') {
            // Encrypt mode: Provide options for Upload or AI
            const select = document.createElement('select');
            const optionUpload = document.createElement('option');
            optionUpload.value = 'upload';
            optionUpload.textContent = 'Upload Image';
            const optionAI = document.createElement('option');
            optionAI.value = 'ai';
            optionAI.textContent = 'AI Generate Image';

            select.appendChild(optionUpload);
            select.appendChild(optionAI);

            const uploadButton = document.createElement('button');
            uploadButton.textContent = 'Browse Directory';
            uploadButton.style.display = 'none';

            const aiPrompt = document.createElement('textarea');
            aiPrompt.rows = 3;
            aiPrompt.placeholder = 'Enter AI prompt...';
            aiPrompt.style.display = 'none';

            const generateButton = document.createElement('button');
            generateButton.textContent = 'Generate';
            generateButton.style.display = 'none';

            // Show/hide options based on selection
            select.addEventListener('change', (e) => {
                const selected = e.target.value;
                uploadButton.style.display = selected === 'upload' ? 'block' : 'none';
                aiPrompt.style.display = selected === 'ai' ? 'block' : 'none';
                generateButton.style.display = selected === 'ai' ? 'block' : 'none';
            });

            // Append components to dynamic content
            dynamicContent.appendChild(select);
            dynamicContent.appendChild(uploadButton);
            dynamicContent.appendChild(aiPrompt);
            dynamicContent.appendChild(generateButton);

        } else {
            // Decrypt mode: Upload Encrypted Image
            textInput.style.display = 'none'; // Hide text field

            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = 'image/*';

            const processButton = document.createElement('button');
            processButton.textContent = 'Process';

            const resultField = document.createElement('textarea');
            resultField.rows = 5;
            resultField.placeholder = 'Decryption results...';
            resultField.readOnly = true;

            // Show Process button only after selecting a file
            fileInput.addEventListener('change', () => {
                if (fileInput.files.length > 0) {
                    processButton.style.display = 'block';
                }
            });

            // Append components to dynamic content
            dynamicContent.appendChild(fileInput);
            dynamicContent.appendChild(processButton);
            dynamicContent.appendChild(resultField);
        }
    });

    /**
     * Button 3: Song Encrypt/Decrypt
     */
    btnOption3.addEventListener('click', () => {
        clearDynamicContent();

        // Create results field
        const resultField = document.createElement('textarea');
        resultField.rows = 5;
        resultField.placeholder = `Song ${currentMode} results...`;
        resultField.readOnly = true;

        dynamicContent.appendChild(resultField);
    });

    /**
     * Button 4: Geo Encrypt/Decrypt
     */
    btnOption4.addEventListener('click', () => {
        clearDynamicContent();

        // Create results field
        const resultField = document.createElement('textarea');
        resultField.rows = 5;
        resultField.placeholder = `Geo ${currentMode} results...`;
        resultField.readOnly = true;

        dynamicContent.appendChild(resultField);
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const dynamicContent = document.getElementById('dynamicContent');
    const tabEncrypt = document.getElementById('tabEncrypt');
    const tabDecrypt = document.getElementById('tabDecrypt');

    const btnEncryptDecrypt = document.getElementById('btnEncryptDecrypt');
    const btnImageOptions = document.getElementById('btnImageOptions');
    const btnOption3 = document.getElementById('btnOption3');
    const btnGeo = document.getElementById('btnGeo');

    let currentMode = 'encrypt'; // Default mode is Encrypt

    /**
     * Clear all dynamic content.
     */
    const clearDynamicContent = () => {
        // @ts-ignore
        dynamicContent.innerHTML = '';
    };

    /**
     * Switch between Encrypt and Decrypt modes.
     * @param {string} mode - 'encrypt' or 'decrypt'
     */
    const switchTab = (mode) => {
        currentMode = mode;

        // Toggle active tab styling
        // @ts-ignore
        tabEncrypt.classList.toggle('active', mode === 'encrypt');
        // @ts-ignore
        tabDecrypt.classList.toggle('active', mode === 'decrypt');

        clearDynamicContent(); // Clear the dynamic content
    };

    // Attach event listeners for tab switching
    // @ts-ignore
    tabEncrypt.addEventListener('click', () => switchTab('encrypt'));
    // @ts-ignore
    tabDecrypt.addEventListener('click', () => switchTab('decrypt'));

    /**
     * Button 1: ASCII Encrypt/Decrypt
     */
    // @ts-ignore
    btnEncryptDecrypt.addEventListener('click', () => {
        clearDynamicContent();

        const messageField = document.createElement('textarea');
        messageField.rows = 3;
        messageField.placeholder = `Enter the message to ${currentMode}...`;

        const keyField = document.createElement('input');
        keyField.type = 'text';
        keyField.placeholder = 'Enter the key...';

        const processButton = document.createElement('button');
        processButton.textContent = currentMode === 'encrypt' ? 'Encrypt' : 'Decrypt';

        const resultField = document.createElement('textarea');
        resultField.rows = 10;
        resultField.readOnly = true;
        resultField.placeholder = `Result will appear here...`;

        // @ts-ignore
        dynamicContent.appendChild(messageField);
        // @ts-ignore
        dynamicContent.appendChild(keyField);
        // @ts-ignore
        dynamicContent.appendChild(processButton);
        // @ts-ignore
        dynamicContent.appendChild(resultField);

        processButton.addEventListener('click', async () => {
            const message = messageField.value.trim();
            const key = keyField.value.trim();

            if (!message || !key) {
                resultField.value = 'Please enter both a message and a key.';
                return;
            }

            try {
                const endpoint = currentMode === 'encrypt' ? '/encrypt' : '/decrypt';
                const payload = currentMode === 'encrypt'
                    ? { message, key }
                    : { ascii_art: message, key };

                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });

                const data = await response.json();

                if (response.ok) {
                    resultField.value = data.ascii_art || data.decrypted_message;
                } else {
                    resultField.value = `Error: ${data.error}`;
                }
            } catch (error) {
                resultField.value = 'An error occurred while processing your request.';
            }
        });
    });

    /**
     * Button 2: Stegano Encrypt/Decrypt
     */
    // @ts-ignore
    btnImageOptions.addEventListener('click', () => {
        clearDynamicContent();

        if (currentMode === 'encrypt') {
            const messageField = document.createElement('textarea');
            messageField.rows = 3;
            messageField.placeholder = 'Enter the text to encrypt...';

            const passkeyField = document.createElement('input');
            passkeyField.type = 'text';
            passkeyField.placeholder = 'Enter the passkey...';

            const selectOption = document.createElement('select');
            const optionUpload = document.createElement('option');
            optionUpload.value = 'upload';
            optionUpload.textContent = 'Upload Image';
            const optionAI = document.createElement('option');
            optionAI.value = 'ai';
            optionAI.textContent = 'Generate AI Image';
            selectOption.appendChild(optionUpload);
            selectOption.appendChild(optionAI);

            const uploadInput = document.createElement('input');
            uploadInput.type = 'file';
            uploadInput.accept = 'image/*';
            uploadInput.style.display = 'none';

            const promptField = document.createElement('textarea');
            promptField.rows = 3;
            promptField.placeholder = 'Enter a prompt for the AI to generate an image...';
            promptField.style.display = 'none';

            const generateButton = document.createElement('button');
            generateButton.textContent = 'Generate Image';
            generateButton.style.display = 'none';

            const encryptButton = document.createElement('button');
            encryptButton.textContent = 'Encrypt';

            selectOption.addEventListener('change', (e) => {
                // @ts-ignore
                const selected = e.target.value;
                uploadInput.style.display = selected === 'upload' ? 'block' : 'none';
                promptField.style.display = selected === 'ai' ? 'block' : 'none';
                generateButton.style.display = selected === 'ai' ? 'block' : 'none';
            });

            // @ts-ignore
            dynamicContent.appendChild(messageField);
            // @ts-ignore
            dynamicContent.appendChild(passkeyField);
            // @ts-ignore
            dynamicContent.appendChild(selectOption);
            // @ts-ignore
            dynamicContent.appendChild(uploadInput);
            // @ts-ignore
            dynamicContent.appendChild(promptField);
            // @ts-ignore
            dynamicContent.appendChild(generateButton);
            // @ts-ignore
            dynamicContent.appendChild(encryptButton);

            generateButton.addEventListener('click', async () => {
                const prompt = promptField.value.trim();
                if (!prompt) {
                    alert('Please enter a prompt for image generation.');
                    return;
                }
            
                // Show a loading indicator above the encrypt button
                const loadingIndicator = document.createElement('div');
                loadingIndicator.textContent = 'Generating image... Please wait.';
                loadingIndicator.classList.add('loading-indicator');
                // @ts-ignore
                dynamicContent.insertBefore(loadingIndicator, encryptButton);
            
                try {
                    const response = await fetch('/generate-ai-image', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ prompt }),
                    });
            
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = URL.createObjectURL(blob);
            
                        // Replace the loading indicator with the generated image
                        const imgPreview = document.createElement('img');
                        imgPreview.src = url;
                        imgPreview.alt = 'Generated Image Preview';
                        imgPreview.style.width = '200px';
                        imgPreview.classList.add('generated-image');
                        // @ts-ignore
                        dynamicContent.replaceChild(imgPreview, loadingIndicator);
            
                        // Add a save button if it doesn't already exist
                        // @ts-ignore
                        const saveButton = dynamicContent.querySelector('button.save-image');
                        if (!saveButton) {
                            const newSaveButton = document.createElement('button');
                            newSaveButton.textContent = 'Save Image';
                            newSaveButton.classList.add('save-image');
                            newSaveButton.addEventListener('click', () => {
                                const link = document.createElement('a');
                                link.href = url;
                                link.download = 'generated_image.png';
                                link.click();
                            });
                            // @ts-ignore
                            dynamicContent.insertBefore(newSaveButton, encryptButton.nextSibling);
                        }
                    } else {
                        const error = await response.json();
                        alert(`Error: ${error.error}`);
                        // @ts-ignore
                        dynamicContent.removeChild(loadingIndicator);
                    }
                } catch (error) {
                    alert('Error during image generation.');
                    // @ts-ignore
                    dynamicContent.removeChild(loadingIndicator);
                }
            });
            
            
            encryptButton.addEventListener('click', async () => {
                const message = messageField.value.trim();
                const imageFile = uploadInput.files?.[0];
                const prompt = promptField.value.trim();

                if (!message) {
                    alert('Please enter a message.');
                    return;
                }

                const formData = new FormData();
                formData.append('message', message);
                if (imageFile) {
                    formData.append('image', imageFile);
                } else if (prompt) {
                    formData.append('prompt', prompt);
                } else {
                    alert('Please upload an image or enter a prompt.');
                    return;
                }
            
                try {
                    const response = await fetch('/stegano/encrypt', {
                        method: 'POST',
                        body: formData,
                    });
            
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = URL.createObjectURL(blob);
            
                        // Display the encoded image
                        const imgPreview = document.createElement('img');
                        imgPreview.src = url;
                        imgPreview.alt = 'Encoded Image Preview';
                        imgPreview.style.width = '200px';
                        // @ts-ignore
                        dynamicContent.appendChild(imgPreview);
            
                        // Add a save button
                        const saveButton = document.createElement('button');
                        saveButton.textContent = 'Save Image';
                        saveButton.addEventListener('click', () => {
                            const link = document.createElement('a');
                            link.href = url;
                            link.download = 'encoded_image.png';
                            link.click();
                        });
                        // @ts-ignore
                        dynamicContent.appendChild(saveButton);
                    } else {
                        const error = await response.json();
                        alert(`Error: ${error.error}`);
                    }
                } catch (error) {
                    alert('An error occurred during encryption.');
                }
            });
            
        } else {
            const uploadInput = document.createElement('input');
            uploadInput.type = 'file';
            uploadInput.accept = 'image/*';

            const passkeyField = document.createElement('input');
            passkeyField.type = 'text';
            passkeyField.placeholder = 'Enter the passkey...';

            const decryptButton = document.createElement('button');
            decryptButton.textContent = 'Decrypt';

            const resultField = document.createElement('textarea');
            resultField.rows = 3;
            resultField.readOnly = true;
            resultField.placeholder = 'Decoded message will appear here...';

            // @ts-ignore
            dynamicContent.appendChild(uploadInput);
            // @ts-ignore
            dynamicContent.appendChild(passkeyField);
            // @ts-ignore
            dynamicContent.appendChild(decryptButton);
            // @ts-ignore
            dynamicContent.appendChild(resultField);

            decryptButton.addEventListener('click', async () => {
                const imageFile = uploadInput.files?.[0];
                const passkey = passkeyField.value.trim();

                if (!imageFile || !passkey) {
                    alert('Please upload an image and enter the passkey.');
                    return;
                }

                const formData = new FormData();
                formData.append('image', imageFile);
                formData.append('passkey', passkey);

                const response = await fetch('/stegano/decrypt', {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    const data = await response.json();
                    resultField.value = data.message;
                } else {
                    alert('Error during decryption.');
                }
            });
        }
    });

        /**
     * Button RSA
     */
        const btnRSA = document.getElementById('btnRSA');

        // @ts-ignore
        btnRSA.addEventListener('click', () => {
            clearDynamicContent();
        
            if (currentMode === 'encrypt') {
                // RSA Encryption UI
                const messageField = document.createElement('textarea');
                messageField.rows = 3;
                messageField.placeholder = 'Enter the message to encrypt...';
        
                const encryptButton = document.createElement('button');
                encryptButton.textContent = 'Encrypt';
        
                const resultField = document.createElement('textarea');
                resultField.rows = 10;
                resultField.readOnly = true;
                resultField.placeholder = 'Encrypted data and keys will appear here...';
        
                // @ts-ignore
                dynamicContent.appendChild(messageField);
                // @ts-ignore
                dynamicContent.appendChild(encryptButton);
                // @ts-ignore
                dynamicContent.appendChild(resultField);
        
                encryptButton.addEventListener('click', async () => {
                    const message = messageField.value.trim();
                    if (!message) {
                        resultField.value = 'Please enter a message.';
                        return;
                    }
        
                    try {
                        const response = await fetch('/rsa/encrypt', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ message }),
                        });
        
                        const data = await response.json();
        
                        if (response.ok) {
                            resultField.value = `Ciphertext: ${data.ciphertext}\n\nPublic Key:\n${data.public_key}\n\nPrivate Key:\n${data.private_key}`;
                        } else {
                            resultField.value = `Error: ${data.error}`;
                        }
                    } catch (error) {
                        resultField.value = 'An error occurred during encryption.';
                    }
                });
            } else {
                // RSA Decryption UI
                const ciphertextField = document.createElement('textarea');
                ciphertextField.rows = 3;
                ciphertextField.placeholder = 'Enter the ciphertext...';
        
                const privateKeyField = document.createElement('textarea');
                privateKeyField.rows = 5;
                privateKeyField.placeholder = 'Enter the private key...';
        
                const decryptButton = document.createElement('button');
                decryptButton.textContent = 'Decrypt';
        
                const resultField = document.createElement('textarea');
                resultField.rows = 10;
                resultField.readOnly = true;
                resultField.placeholder = 'Decrypted message will appear here...';
        
                // @ts-ignore
                dynamicContent.appendChild(ciphertextField);
                // @ts-ignore
                dynamicContent.appendChild(privateKeyField);
                // @ts-ignore
                dynamicContent.appendChild(decryptButton);
                // @ts-ignore
                dynamicContent.appendChild(resultField);
        
                decryptButton.addEventListener('click', async () => {
                    const ciphertext = ciphertextField.value.trim();
                    const privateKey = privateKeyField.value.trim();
        
                    if (!ciphertext || !privateKey) {
                        resultField.value = 'Please enter both ciphertext and private key.';
                        return;
                    }
        
                    try {
                        const response = await fetch('/rsa/decrypt', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ ciphertext, private_key: privateKey }),
                        });
        
                        const data = await response.json();
        
                        if (response.ok) {
                            resultField.value = `Decrypted Message: ${data.plaintext}`;
                        } else {
                            resultField.value = `Error: ${data.error}`;
                        }
                    } catch (error) {
                        resultField.value = 'An error occurred during decryption.';
                    }
                });
            }
        });
        


    /**
     * Button 3: Song Encrypt/Decrypt
     */
    // @ts-ignore
    btnOption3.addEventListener('click', () => {
        clearDynamicContent();

        const resultField = document.createElement('textarea');
        resultField.rows = 5;
        resultField.readOnly = true;
        resultField.placeholder = `Song ${currentMode} results...`;

        // @ts-ignore
        dynamicContent.appendChild(resultField);
    });

    /**
     * Button 4: Geo Encrypt/Decrypt
     */
    // @ts-ignore
    btnGeo.addEventListener('click', () => {
        clearDynamicContent();

        console.log('geo button clicked', currentMode)

        if(currentMode === 'encrypt') {

            const encryptButton = document.createElement('button');
            encryptButton.textContent = 'Encrypt';

            const resultField = document.createElement('textarea');
            resultField.rows = 10;
            resultField.readOnly = true;
            resultField.placeholder = 'Encrypted data and key will appear here...';

            dynamicContent?.appendChild(encryptButton)
            dynamicContent?.appendChild(resultField)

            encryptButton.addEventListener('click', async () => {
                try {
                    const response = await fetch('/geo/encrypt', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({  }),
                    });

                    console.log(response)
    
                    const data = await response.json();
    
                    if (response.ok) {
                        resultField.value = `Ciphertext: ${data.ciphertext}\n\nKey:\n${data.key}\n\nNonce: ${data.nonce}`;
                    } else {
                        resultField.value = `Error: ${data.error}`;
                    }
                }
                catch(error) {
                    resultField.value = `An error occurred during encryption. Exception: ${error}`;
                }
            });  
        }
        else 
        {
            const ciphertextField = document.createElement('textarea');
            ciphertextField.rows = 3;
            ciphertextField.placeholder = 'Enter the ciphertext...';
    
            const keyField = document.createElement('textarea');
            keyField.rows = 3;
            keyField.placeholder = 'Enter the key...';

            const nonceField = document.createElement('textarea');
            nonceField.rows = 3;
            nonceField.placeholder = 'Enter the nonce...';
    
            const decryptButton = document.createElement('button');
            decryptButton.textContent = 'Decrypt';
    
            const resultField = document.createElement('textarea');
            resultField.rows = 3;
            resultField.readOnly = true;
            resultField.placeholder = 'Decrypted message will appear here...';

            dynamicContent?.appendChild(ciphertextField);
            dynamicContent?.appendChild(keyField);
            dynamicContent?.appendChild(nonceField);
            dynamicContent?.appendChild(decryptButton)
            dynamicContent?.appendChild(resultField);

            decryptButton.addEventListener('click', async () => {
                const ciphertext = ciphertextField.value.trim();
                const key = keyField.value.trim();
                const nonce = nonceField.value.trim();
        
                if (!ciphertext || !key || !nonce) {
                    resultField.value = 'Please enter both ciphertext, key and nonce.';
                    return;
                }
        
                try {   
                    const response = await fetch('/geo/decrypt', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ ciphertext, key, nonce }),
                    });
        
                    const data = await response.json();
        
                    if (response.ok) {
                        resultField.value = `Decrypted Message: ${data.capital}`;
                    } else {
                        resultField.value = `Error: ${data.error}`;
                    }
                } catch (error) {
                    resultField.value = 'An error occurred during decryption.';
                }
            });  
        }

    });
});

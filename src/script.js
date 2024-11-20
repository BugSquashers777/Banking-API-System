// API URL
const apiUrl = "http://localhost:5000";  // Change to your API URL if needed

// Create Account
function createAccount() {
    const name = document.getElementById("create_name").value;
    const email = document.getElementById("create_email").value;

    fetch(`${apiUrl}/accounts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email })
    })
    .then(response => response.json())
    .then(data => {
        const responseDiv = document.getElementById("create_response");
        responseDiv.innerHTML = `Account created successfully! ID: ${data.account_id}, Balance: ${data.balance}`;
        responseDiv.className = 'response success';
    })
    .catch(err => {
        document.getElementById("create_response").innerHTML = "Error creating account: " + err.message;
        document.getElementById("create_response").className = 'response error';
    });
}

// Get Account Info
function getAccountInfo() {
    const accountId = document.getElementById("view_account_id").value;

    fetch(`${apiUrl}/accounts/${accountId}`)
        .then(response => response.json())
        .then(data => {
            if (data.email === undefined){
                document.getElementById("account_info_response").innerHTML = "Account not found or error occurred:"
            }else{
            const responseDiv = document.getElementById("account_info_response");
            responseDiv.innerHTML = `Name: ${data.name}<br>Email: ${data.email}<br>Balance: ${data.balance}`;
            responseDiv.className = 'response success';
            }
        })
        .catch(err => {
            document.getElementById("account_info_response").innerHTML = "Account not found or error occurred: " + err.message;
            document.getElementById("account_info_response").className = 'response error';
        });
}

// Process Deposit or Withdrawal
function processTransaction(action) {
    const accountId = document.getElementById("trans_account_id").value;
    const amount = parseFloat(document.getElementById("trans_amount").value);

    fetch(`${apiUrl}/transactions/${action}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ account_id: accountId, amount })
    })
    .then(response => response.json())
    .then(data => {
        if (data[1] === 200){
        const responseDiv = document.getElementById("transaction_response");
        responseDiv.innerHTML = `${action.charAt(0).toUpperCase() + action.slice(1)} successful! New Balance: ${data[0].balance}`;
        responseDiv.className = 'response success';
        }
        else {
            document.getElementById("transaction_response").innerHTML = "Error:" + data.message;
        }
    })
    .catch(err => {
        document.getElementById("transaction_response").innerHTML = "Error: " + err.message;
        document.getElementById("transaction_response").className = 'response error';
    });
}

// Update Account
function updateAccount() {
    const accountId = document.getElementById("update_account_id").value;
    const name = document.getElementById("update_name").value;
    const email = document.getElementById("update_email").value;

    fetch(`${apiUrl}/accounts/${accountId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email})
    })
    .then(response => response.json())
    .then(data => {
        const responseDiv = document.getElementById("update_response");
        responseDiv.innerHTML = `Account updated: ${data.name}, Balance: ${data.email}`;
        responseDiv.className = 'response success';
    })
    .catch(err => {
        document.getElementById("update_response").innerHTML = "Error updating account: " + err.message;
        document.getElementById("update_response").className = 'response error';
    });
}

// Open the confirmation modal
function openConfirmationModal() {
    const accountId = document.getElementById('delete_account_id').value;

    // Check if the account ID is provided
    if (!accountId) {
        document.getElementById('delete_response').textContent = "Please enter an Account ID.";
        return;
    }

    // Show the modal
    document.getElementById('confirmationModal').style.display = "block";
}

// Close the confirmation modal
function closeConfirmationModal() {
    document.getElementById('confirmationModal').style.display = "none";
}

// Confirm the deletion
async function confirmDeletion() {
    const accountId = document.getElementById('delete_account_id').value;
    const deleteResponseElement = document.getElementById('delete_response');

    try {
        const response = await fetch(`${apiUrl}/accounts/${accountId}`, {
            method: 'DELETE'
        });

        if (response.ok) {  // Check if the status code is 2xx
            // Successfully deleted the account
            deleteResponseElement.textContent = "Account deleted successfully.";
        } else {
            // Account not found or other error
            const data = await response.json();  // Optionally, get error message from the response
            deleteResponseElement.textContent = data.message || "Account not found.";
        }
    } catch (error) {
        // Handle network or other errors
        deleteResponseElement.textContent = "An error occurred while deleting the account. " + error;
    }

    // Close the modal after confirmation
    closeConfirmationModal();
}


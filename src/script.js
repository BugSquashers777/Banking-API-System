// API URL
const apiUrl = "http://localhost:5000"; // Change to your API URL if needed

// Create Account
async function createAccount() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const balance = parseFloat(document.getElementById("initialBalance").value);

  if (!name || !email || balance < 0) {
    document.getElementById("create_response").innerHTML =
      "Invalid input: name and email are required, balance must be non-negative.";
    document.getElementById("create_response").className = "response error";
    return;
  }

  try {
    const response = await fetch(`${apiUrl}/accounts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, balance }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    const responseDiv = document.getElementById("create_response");
    responseDiv.innerHTML = `Account created successfully! ID: ${data.account_id}, Balance: ${data.balance}`;
    responseDiv.className = "response success";
  } catch (err) {
    document.getElementById("create_response").innerHTML =
      "Error creating account: " + err.message;
    document.getElementById("create_response").className = "response error";
  }
}

// Get Account Info
async function getAccountInfo() {
  const email = localStorage.getItem("email");

  try {
    const response = await fetch(`${apiUrl}/accounts/${email}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    const responseDiv = document.getElementById("account_info_response");
    responseDiv.innerHTML = `Name: ${data.name}<br>Email: ${data.email}<br>Balance: ${data.balance}`;
    responseDiv.className = "response success";
  } catch (err) {
    document.getElementById("account_info_response").innerHTML =
      "Account not found or error occurred: " + err.message;
    document.getElementById("account_info_response").className =
      "response error";
  }
}

// Process Transaction
async function processTransaction(action) {
  const accountId = document.getElementById("trans_account_id").value;
  const amount = parseFloat(document.getElementById("trans_amount").value);

  try {
    const response = await fetch(`${apiUrl}/transactions/${action}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ account_id: accountId, amount }),
    });
    const data = await response.json();

    if (data[1] === 200) {
      const responseDiv = document.getElementById("transaction_response");
      responseDiv.innerHTML = `${
        action.charAt(0).toUpperCase() + action.slice(1)
      } successful! New Balance: ${data[0].balance}`;
      responseDiv.className = "response success";
    } else {
      document.getElementById("transaction_response").innerHTML =
        "Error:" + data.message;
    }
  } catch (err) {
    document.getElementById("transaction_response").innerHTML =
      "Error: " + err.message;
    document.getElementById("transaction_response").className =
      "response error";
  }
}

// Update Account
async function updateAccount() {
  // Get elements
  const accountIdElement = document.getElementById("update_account_id");
  const nameElement = document.getElementById("update_name");
  const emailElement = document.getElementById("update_email");
  const responseDiv = document.getElementById("update_response");

  // Get values
  const accountId = accountIdElement.value;
  const name = nameElement.value;
  const email = emailElement.value;

  // Validate required fields
  if (!accountId || !name || !email) {
    responseDiv.innerHTML = "Please fill in all required fields";
    responseDiv.className = "response error";
    return;
  }

  try {
    const response = await fetch(
      `${apiUrl}/accounts/${localStorage.getItem("email")}`,
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email }),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    localStorage.setItem("email", data.email);

    const response_user = await fetch(`${apiUrl}/login/${email}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });
    responseDiv.innerHTML = `Account updated: ${data.name}, Email: ${data.email}`;
    responseDiv.className = "response success";
  } catch (err) {
    responseDiv.innerHTML = "Error updating account: " + err.message;
    responseDiv.className = "response error";
  }
}

async function userLogin() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch(
      `${apiUrl}/login?username=${username}&password=${password}`
    );

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("loggedIn", "true");
      localStorage.setItem("username", data.username);
      localStorage.removeItem("email");
      localStorage.setItem("email", data.email);
      window.location.href = "index.html";
    } else {
      const data = await response.json();
      document.getElementById("login_response").style.display = "block";
      document.getElementById("login_response").textContent =
        data.message || "Invalid credentials.";
    }
  } catch (error) {
    document.getElementById("login_response").textContent =
      "An error occurred while logging in. " + error;
  }
}

async function userRegister() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const email = document.getElementById("email").value;

  try {
    const response = await fetch(`${apiUrl}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
    });

    if (response.ok) {
      window.location.href = "login.html";
    }
  } catch (error) {
    document.getElementById("register_error").textContent =
      "An error occurred while logging in. " + error;
  }
}

function userLogout() {
  localStorage.removeItem("loggedIn");
  localStorage.removeItem("username");
  localStorage.removeItem("email");
  window.location.href = "login.html";
}

function confirmDeletion() {
  const result = confirm("Are you sure you want to delete your account?");
  if (result) {
    deleteAccount();
  } else {
    const deleteModal = bootstrap.Modal.getInstance(
      document.getElementById("deleteModal")
    );
    deleteModal.hide();
  }
}

async function deleteAccount() {
  const accountId = document.getElementById("delete_account_id").value;

  try {
    const response = await fetch(`${apiUrl}/accounts/${accountId}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const responseDiv = document.getElementById("delete_response");
    responseDiv.innerHTML = "Account deleted successfully!";
    responseDiv.className = "response success";

    // Log out user after successful deletion
    setTimeout(() => {
      userLogout();
    }, 2000);
  } catch (err) {
    document.getElementById("delete_response").innerHTML =
      "Error deleting account: " + err.message;
    document.getElementById("delete_response").className = "response error";
  }
}

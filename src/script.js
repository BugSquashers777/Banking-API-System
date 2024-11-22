// Global API configuration
const apiUrl = "http://127.0.0.1:5000";

// Global fetch configuration
const fetchConfig = {
  mode: "cors",
  credentials: "include",
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
    Origin: "http://127.0.0.1:5500",
  },
};
// Create Account
async function createAccount() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const balance = parseFloat(document.getElementById("initialBalance").value);
  const account_type = document.getElementById("accountType").value;

  if (!name || !email || balance < 0) {
    document.getElementById("create_response").innerHTML =
      "Invalid input: name and email are required, balance must be non-negative.";
    document.getElementById("create_response").className = "response error";
    return;
  }

  try {
    const response = await fetch(`${apiUrl}/accounts`, {
      method: "POST",
      ...fetchConfig,
      body: JSON.stringify({ name, email, balance, account_type }),
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
    responseDiv.innerHTML = `Name: ${data.name}<br>Email: ${
      data.email
    }<br>Balance: R${parseFloat(data.balance).toFixed(2)}`;
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
  const account_id = document.getElementById("trans_account_id").value;
  const amount = parseFloat(document.getElementById("trans_amount").value);
  const email = localStorage.getItem("email");
  const date = new Date().toISOString().split("T")[0];

  // Validate inputs
  if (!amount || amount <= 0) {
    document.getElementById("transaction_response").innerHTML =
      "Please enter a valid amount greater than 0";
    document.getElementById("transaction_response").className =
      "response error";
    return;
  }

  try {
    const response = await fetch(`${apiUrl}/transactions/${action}`, {
      method: "POST",
      ...fetchConfig,
      body: JSON.stringify({
        account_id: parseInt(account_id),
        amount: parseFloat(amount),
        email: email,
        date: date,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.message || `HTTP error! status: ${response.status}`
      );
    }

    const data = await response.json();
    const responseDiv = document.getElementById("transaction_response");
    responseDiv.innerHTML = `${
      action.charAt(0).toUpperCase() + action.slice(1)
    } successful! New Balance: ${data[0].balance}`;
    responseDiv.className = "response success";

    // Update available balance display
    document.getElementById("available_balance").value = data[0].balance;

    // Clear amount input for next transaction
    document.getElementById("trans_amount").value = "";
  } catch (err) {
    document.getElementById("transaction_response").innerHTML =
      "Error processing transaction: " + err.message;
    document.getElementById("transaction_response").className =
      "response error";
  }
}

// Update Account
async function updateAccount() {
  try {
    const email = document.getElementById("update_email").value;
    const name = document.getElementById("update_name").value;

    // Log the request details for debugging
    console.log("Updating account:", { email, name });

    const response = await fetch(`${apiUrl}/accounts/${email}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        name: name,
        email: email,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.message || `HTTP error! status: ${response.status}`
      );
    }

    const data = await response.json();
    document.getElementById("update_response").innerHTML =
      "Account updated successfully";
    document.getElementById("update_response").className = "response success";

    // Refresh account data
    await loadAccountData();
  } catch (err) {
    console.error("Update error:", err);
    document.getElementById("update_response").innerHTML =
      "Error updating account: " + err.message;
    document.getElementById("update_response").className = "response error";
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
      ...fetchConfig,
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
      ...fetchConfig,
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

async function getTransactionHistory() {
  try {
    const accountId = document.getElementById("trans_account_id").value;
    const responseDiv = document.getElementById("transactions_response");
    const tableBody = document.getElementById("transactions_list");

    if (!accountId) {
      throw new Error("Account ID not found");
    }

    const response = await fetch(
      `${apiUrl}/transactions/history/${localStorage.getItem("email")}`,
      {
        method: "GET",
        ...fetchConfig,
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Clear existing content
    tableBody.innerHTML = "";

    if (!data || data.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="3" class="text-center">No transactions found</td>
        </tr>
      `;
      return;
    }

    // Add each transaction to the table
    data.forEach((transaction) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${transaction.date}</td>
        <td>${
          transaction.action.charAt(0).toUpperCase() +
          transaction.action.slice(1)
        }</td>
        <td class="${
          transaction.action === "deposit" ? "text-success" : "text-danger"
        }">
          ${
            transaction.action === "deposit" ? "+" : "-"
          }R${transaction.amount.toFixed(2)}
        </td>
      `;
      tableBody.appendChild(row);
    });

    responseDiv.innerHTML = "";
    responseDiv.className = "response success";
  } catch (err) {
    console.error("Transaction error:", err);
    const responseDiv = document.getElementById("transactions_response");
    responseDiv.innerHTML = "Error fetching transactions: " + err.message;
    responseDiv.className = "response error";

    const tableBody = document.getElementById("transactions_list");
    tableBody.innerHTML = `
      <tr>
        <td colspan="3" class="text-center">Error loading transactions</td>
      </tr>
    `;
  }
}

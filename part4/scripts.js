/**
 * Listen form submit and send login data to backend
 * Sends login credential to the backend and handle the response
 * If success : stores the token in a cookie and redirect to home page
 * 
 * @param {string} email - User's email address
 * @param {string} password - User's password
 */

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      // Get field of login
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        // Send request API
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });

        if (response.ok) {
          const data = await response.json();

          // Stock JWT in cookie
          document.cookie = `token=${data.access_token}; path=/`;

          window.location.href = 'index.html';
        } else {
          // Handle error if invalid log
          const errorText = await response.text();
          alert('Login failed: ' + errorText);
        }
      } catch (error) {
        console.error('Erreur lors de la connexion :', error);
        alert('Erreur de connexion. Veuillez réessayer.');
      }
    });
  }
});
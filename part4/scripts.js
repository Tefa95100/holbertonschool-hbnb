
/**
 * Function to get a cookie by name
 * 
 * @param {string} name - Cookie's name
 */
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

/**
 * Check if user is authenticated and toggle login link visibility
 */
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    if (loginLink) loginLink.style.display = 'block';
  } else {
    if (loginLink) loginLink.style.display = 'none';
    fetchPlaces(token);
  }
}

/**
 * Fetch the list of places from the API
 */
async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
    } else {
      alert('Error loading places');
    }
  } catch (error) {
    console.error('API error:', error);
    alert('Unable to load places.');
  }
}

/**
 * Dynamically create and display place elements
 * 
 * @param {string} places - places name
 */
function displayPlaces(places) {
  const listContainer = document.getElementById('places-list');
  listContainer.innerHTML = '';

  places.forEach(place => {
    const article = document.createElement('article');
    article.className = 'place-card';
    article.setAttribute('data-price', place.price);
    article.innerHTML = `
      <h2>${place.name}</h2>
      <p>${place.description || ''}</p>
      <p>Price per night: ${place.price}€</p>
      <a href="place.html" class="details-button">View Details</a>
    `;
    listContainer.appendChild(article);
  });

  setupPriceFilter();
}

/**
 * Add event listener and handle price filter dropdown
 */
function setupPriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  if (!priceFilter) return;

  // Add options to dropdown if not already present
  if (!priceFilter.options.length) {
    ['10', '50', '100', 'All'].forEach(value => {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = value === 'All' ? 'All' : `≤ ${value}€`;
      priceFilter.appendChild(option);
    });
  }

  // Handle filter change
  priceFilter.addEventListener('change', (event) => {
    const selected = event.target.value;
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
      const price = parseInt(card.getAttribute('data-price'));

      if (selected === 'All' || price <= parseInt(selected)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

/**
 * Listen form submit and send login data to backend
 * Sends login credential to the backend and handle the response
 * If success : stores the token in a cookie and redirect to home page
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
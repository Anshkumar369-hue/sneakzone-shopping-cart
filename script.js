const registerTab = document.querySelector('#registerTab');
const loginTab = document.querySelector('#loginTab');
const registerForm = document.querySelector('#registerForm');
const loginForm = document.querySelector('#loginForm');
const signedIn = document.querySelector('#signedIn');
const message = document.querySelector('#message');
function showMessage(text, error = false) {
  message.textContent = text;
  message.className = error ? 'error' : 'success';
}
function switchTab(tab) {
  registerTab.classList.toggle('active', tab === 'register');
  loginTab.classList.toggle('active', tab === 'login');
  registerForm.hidden = tab !== 'register';
  loginForm.hidden = tab !== 'login';
  signedIn.hidden = true;
  showMessage('');
}
registerTab.addEventListener('click', () => switchTab('register'));
loginTab.addEventListener('click', () => switchTab('login'));
async function send(path, body) {
  const response = await fetch(path, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
  const data = await response.json();
  if (!response.ok) throw new Error(data.message || 'Something went wrong.');
  return data;
}
registerForm.addEventListener('submit', async event => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(registerForm));
  try {
    const result = await send('/api/register', data);
    registerForm.reset();
    switchTab('login');
    showMessage(result.message);
  } catch (error) { showMessage(error.message, true); }
});
loginForm.addEventListener('submit', async event => {
  event.preventDefault();
  try {
    const result = await send('/api/login', Object.fromEntries(new FormData(loginForm)));
    loginForm.reset();
    registerForm.hidden = true;
    loginForm.hidden = true;
    signedIn.hidden = false;
    document.querySelector('#welcome').textContent = `Hello, ${result.name}!`;
    showMessage(result.message);
  } catch (error) { showMessage(error.message, true); }
});
document.querySelector('#logout').addEventListener('click', async () => {
  try { await send('/api/logout', {}); switchTab('login'); showMessage('Logged out successfully.'); }
  catch (error) { showMessage(error.message, true); }
});
(async () => {
  try {
    const response = await fetch('/api/me');
    if (!response.ok) return;
    const user = await response.json();
    registerForm.hidden = true;
    loginForm.hidden = true;
    signedIn.hidden = false;
    document.querySelector('#welcome').textContent = `Hello, ${user.name}!`;
  } catch (_) { /* Server unavailable */ }
})();

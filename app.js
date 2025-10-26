
// JS logic for Gin Rummy gameplay and WebSockets
// Replace 'YOUR_DEPLOY_URL' with your Render/Vercel WebSocket URL, e.g., wss://myapp.onrender.com/ws
const ws = new WebSocket("wss://YOUR_DEPLOY_URL/ws");

ws.onopen = () => console.log("Connected to server");
ws.onmessage = (msg) => console.log("Message received:", msg.data);

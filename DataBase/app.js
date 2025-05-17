// Main Robot Logic (data push /read )
const { ref, set } = require("firebase/database");
const { database } = require("./firebaseConfig");

function sendTestAlert() {
  const alertRef = ref(database, 'alerts/testAlert');
  set(alertRef, {
    message: "Test alert from SECURO robot",
    timestamp: new Date().toISOString()
  })
  .then(() => console.log("✅ Alert sent to Firebase"))
  .catch(err => console.error("❌ Failed:", err));
}

sendTestAlert();


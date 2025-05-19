const admin = require('firebase-admin');
const serviceAccount = require('./serviceAccountKey.json');

// Initialize Firebase Admin SDK with service account
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://securo-database-default-rtdb.firebaseio.com' // Replace with your Firebase database URL
});

// Initialize Firestore
const db = admin.firestore(); // If using Firestore. If using Realtime Database, replace with admin.database()
module.exports = db;

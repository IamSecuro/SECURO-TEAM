const express = require('express');
const bodyParser = require('body-parser');
const admin = require('firebase-admin');
const serviceAccount = require('./serviceAccountKey.json');
const cors = require('cors');
const multer = require('multer');
const path = require('path');

// Initialize Express app
const app = express();
const port = 3000;

// Firebase initialization
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  storageBucket: 'securo-database.firebasestorage.app' // Add your Firebase storage bucket URL
});

const db = admin.firestore();
const bucket = admin.storage().bucket(); // Firebase Storage reference

// Use CORS for allowing cross-origin requests
app.use(cors());
// Increase the size limit to 200MB or adjust as needed
app.use(bodyParser.json({ limit: '100mb' })); // For JSON payload
app.use(bodyParser.urlencoded({ limit: '100mb', extended: true })); // For URL-encoded payload
app.use(bodyParser.json());

// Multer setup to handle file uploads in memory
const upload = multer({ storage: multer.memoryStorage() });

// Upload route to handle file upload to Firebase Storage
app.post('/upload', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded');
  }

  try {
    const fileName = `${Date.now()}_${req.file.originalname}`;
    const file = bucket.file(fileName);

    // Upload the file to Firebase Storage
    await file.save(req.file.buffer, {
      metadata: { contentType: req.file.mimetype },
    });

    // Make the file publicly accessible (optional)
    await file.makePublic();

    const fileUrl = `https://storage.googleapis.com/${bucket.name}/${fileName}`;
    return res.status(200).json({ fileUrl });
  } catch (error) {
    console.error('Error uploading file:', error);
    return res.status(500).send('Error uploading file');
  }
});

// Registration endpoint to store user data including the uploaded image URL
app.post('/register', async (req, res) => {
  try {
    console.log('Received registration request:', req.body);

    const { username, password, phoneNumber, country, address, photos } = req.body;

    if (!username || !password || !phoneNumber || !country || !address || !photos) {
      return res.status(400).json({ message: 'All fields are required!' });
    }

    // Save data to Firestore
    const userRef = db.collection('users').doc(username);
    await userRef.set({
      username,
      password,
      phoneNumber,
      country,
      address,
      photos
    });

    return res.status(200).json({ message: 'User registered successfully!' });
  } catch (err) {
    console.error('Error during registration:', err);
    return res.status(500).json({ message: 'Registration failed, please try again later.' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

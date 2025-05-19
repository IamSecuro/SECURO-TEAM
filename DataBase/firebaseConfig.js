// firebaseConfig.js

// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getDatabase, ref, set, push } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-database.js";
import { getStorage, ref as storageRef, uploadString, getDownloadURL } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-storage.js";
Q
// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBd_dgcQNudi4x8TIm1BmFV-DMXhG5fio4",
  authDomain: "securo-database.firebaseapp.com",
  databaseURL: "https://securo-database-default-rtdb.firebaseio.com",
  projectId: "securo-database",
  storageBucket: "securo-database.appspot.com",
  messagingSenderId: "298798946059",
  appId: "1:298798946059:web:dea01e2a93709d08dbf40e",
  measurementId: "G-VM9J6W4BNJ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const storage = getStorage(app);

// Export Firebase instances
export { app, database, storage, ref, set, push, storageRef, uploadString, getDownloadURL };

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBd_dgcQNudi4x8TIm1BmFV-DMXhG5fio4",
  authDomain: "securo-database.firebaseapp.com",
  databaseURL: "https://securo-database-default-rtdb.firebaseio.com",
  projectId: "securo-database",
  storageBucket: "securo-database.firebasestorage.app",
  messagingSenderId: "298798946059",
  appId: "1:298798946059:web:dea01e2a93709d08dbf40e",
  measurementId: "G-VM9J6W4BNJ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
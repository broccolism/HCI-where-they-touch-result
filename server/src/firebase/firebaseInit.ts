import firebase from "firebase";
import "firebase/firestore";
import firebaseConfig from "../config/firebaseConfig";

const firebaseApp = firebase.initializeApp(firebaseConfig);

export default firebaseApp.firestore();

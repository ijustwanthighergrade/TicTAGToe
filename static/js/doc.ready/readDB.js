// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyD97zcnmN1NA-cfki1DOxSp9wVrjexbPnA",
    authDomain: "tictagtoe-2edc4.firebaseapp.com",
    projectId: "tictagtoe-2edc4",
    storageBucket: "tictagtoe-2edc4.appspot.com",
    messagingSenderId: "222759135763",
    appId: "1:222759135763:web:db862c5fdb4dbd6c59ade6",
    measurementId: "G-PH3SG53GK9"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig)
const db = firebase.firestore()

db.collection('posts')
  .add({
    first: 'Dez',
    last: 'Chuang',
    gender: 'male'
  })
  .then(function(docRef) {
    console.log('Document written with ID: ', docRef.id)
  })
  .catch(function(error) {
    console.error('Error adding document: ', error)
})


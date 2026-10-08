const fs = require('fs');
fs.copyFileSync('www/location_data.js', 'location_data.js');
fs.copyFileSync('www/location_data.json', 'location_data.json');
fs.copyFileSync('www/location_data.js', 'android/app/src/main/assets/public/location_data.js');
fs.copyFileSync('www/location_data.json', 'android/app/src/main/assets/public/location_data.json');
console.log('Location files copied successfully');

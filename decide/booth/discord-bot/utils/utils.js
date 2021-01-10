const fs = require('fs')

const storeData = (userId, data) => {
    
    const path = 'users.json'

    if(!fs.existsSync(path)){
        fs.appendFileSync(path, '{}', function(err){
          if (err) throw err;
          console.log('Error creating file: '+ err)
        })
      }
    
    var read = fs.readFileSync(path)
    var file = JSON.parse(read)

    file[userId] = data
    fs.writeFileSync(path, JSON.stringify(file, null, 2)) 
}


const getDataFromUser = (userId) => { 
    const path = 'users.json'

    if(fs.existsSync(path)){
      var read = fs.readFileSync(path)
      var file = JSON.parse(read)
 
      return file[userId]      
    }else{
      return undefined
    }
}

const cleanData = (userId) => {
  const path = 'users.json'

  try{
    var read = fs.readFileSync(path)
    var file = JSON.parse(read)

    file[userId] = {}
    
    fs.writeFileSync(path, JSON.stringify(file, null, 2)) 
  }catch{
    console.log('Error en cleanData')
    return false
  }
}

exports.storeData = storeData
exports.getDataFromUser = getDataFromUser
exports.cleanData = cleanData

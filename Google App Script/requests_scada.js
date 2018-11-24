var spreadsheet = SpreadsheetApp.openById('1iOf4d2F_I6pzALuNP2FrWR6NQh68GeJDkWT_W8TqdTs');
var sheet = spreadsheet.getSheetByName('credentials');

function autenticacao(username, password) {
  sheet = spreadsheet.getSheetByName('credentials');
  
  // Tratativa do usuario
  var usuarioDecoded = Utilities.base64Decode(username);
  var usuario = Utilities.newBlob(usuarioDecoded).getDataAsString();
  
  // Tratativa da senha
  var senhaDecoded = Utilities.base64Decode(password);
  var senha = Utilities.newBlob(senhaDecoded).getDataAsString();
  
  // Realiza a verificacao
  for(var i = 2; i < sheet.getLastRow() + 1; i++) {
    if(usuario == sheet.getRange(i, 1).getValue() && senha == sheet.getRange(i, 2).getValue())
      return true;
  }
  return false;
}

function doPost(e) {
  var dados = JSON.parse(e.parameter.dados);
  var usuario = dados.credenciais[0].usuario;
  var senha = dados.credenciais[0].senha;
  
  if(autenticacao(usuario, senha)) {
    var name;
    var value;
    
    sheet = spreadsheet.getSheetByName('variables_info');
    for(var i = 2; i < sheet.getLastRow() + 1; i++) {
      name = dados.valores[i-2].name;
      value = dados.valores[i-2].last_value;
      
      if(name == 'KCT_MODE_PUMP1' || name == 'KCT_MODE_PUMP2' || name == 'KCT_START') {
        sheet.getRange(i, 11).setValue(value);
      }
    }
    
    return ContentService.createTextOutput(JSON.stringify({'resposta': 'permitido'})).setMimeType(ContentService.MimeType.JSON);
  } else {
    return ContentService.createTextOutput(JSON.stringify({'resposta': 'bloqueado'})).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  sheet = spreadsheet.getSheetByName('variables_info');
  var variables = [];
  
  for(var k = 2; k < sheet.getLastRow() + 1; k++) {
    variables.push({
      'id': spreadsheet.getSheetByName('variables_info').getRange(k, 1).getValue(),
      'name': spreadsheet.getSheetByName('variables_info').getRange(k, 2).getValue(),
      'last_value': spreadsheet.getSheetByName('variables_hist').getRange(2, k).getValue()
    });
  }
  
  return ContentService.createTextOutput(JSON.stringify(variables)).setMimeType(ContentService.MimeType.JSON);
}
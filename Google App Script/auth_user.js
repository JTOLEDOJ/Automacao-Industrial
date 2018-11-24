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
  var usuario = e.parameter.usuario;
  var senha = e.parameter.senha;
  
  if(autenticacao(usuario, senha)) {
    return ContentService.createTextOutput(JSON.stringify('Permitido')).setMimeType(ContentService.MimeType.JSON);
  } else {
    return ContentService.createTextOutput(JSON.stringify('Bloqueado')).setMimeType(ContentService.MimeType.JSON);
  }  
}
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
      
      if(name != 'KCT_MODE_PUMP1' && name != 'KCT_MODE_PUMP2' && name != 'KCT_START') {
        sheet.getRange(i, 11).setValue(value);
      }
      
      if((name == 'FBK_PUMP1_FAULT' || name == 'FBK_PUMP2_FAULT' || name == 'FBK_EMERGENCY') && value == 1) {
        var emailSheet = spreadsheet.getSheetByName('credentials');
        var emailQuotaRemaining = MailApp.getRemainingDailyQuota();
        var emailGroup = 'Administrators'
        
        for(var k = 2; k < emailSheet.getLastRow() + 1; k++) {
          if(emailSheet.getRange(k, 5).getValue() == emailGroup && emailQuotaRemaining > 0) {
            var emailUser = emailSheet.getRange(k, 1).getValue();
            var emailAddress = emailSheet.getRange(k, 3).getValue();
            var emailMessage = 'Caro ' + emailUser + ', o processo de sistema de limpeza de torre de resfriamento foi interrompido devido à variável ' + name;
            var emailSubject = 'Processo Interrompido';
            MailApp.sendEmail(emailAddress, emailSubject, emailMessage);
          }
        }
      }
    }
    
    sheet = spreadsheet.getSheetByName('variables_hist');
    sheet.insertRows(2);
    sheet.getRange(2, 1).setValue(Utilities.formatDate(new Date(), 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm:ss'));
    for(var j = 2; j < sheet.getLastColumn() + 1; j++) {
      value = dados.valores[j-2].last_value;
      sheet.getRange(2, j).setValue(value);
    }
    
    return ContentService.createTextOutput('Seus dados foram recebidos com sucesso!');
  }
  
  return ContentService.createTextOutput('Você não tem permissões para executar tal tarefa!');
}

function doGet() {
  sheet = spreadsheet.getSheetByName('variables_info');
  var variables = [];
  
  for(var i = 2; i < sheet.getLastRow() + 1; i++) {
    variables.push({
      'id': sheet.getRange(i, 1).getValue(),
      'name': sheet.getRange(i, 2).getValue(),
      'last_value': sheet.getRange(i, 11).getValue()
    });
  }
  
  return ContentService.createTextOutput(JSON.stringify(variables)).setMimeType(ContentService.MimeType.JSON);
}
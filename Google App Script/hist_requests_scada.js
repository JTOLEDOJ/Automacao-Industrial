var spreadsheet = SpreadsheetApp.openById('1iOf4d2F_I6pzALuNP2FrWR6NQh68GeJDkWT_W8TqdTs');
var sheet = spreadsheet.getSheetByName('variables_hist');

function doGet(e) {
  var variavel = e.parameter.variavel;
  for(var j = 2; j < sheet.getLastColumn() + 1; j++) {
    if(sheet.getRange(1, j).getValue() == variavel) {
      var quant_dados = sheet.getLastRow() - 1;
      
      var range_label = sheet.getRange(2, 1, quant_dados);
      var values_label = range_label.getValues().reverse();
      
      var range_data = sheet.getRange(2, j, quant_dados);
      var values_data = range_data.getValues().reverse();
      
      var hist_data = {
        'labels': values_label,
        'data': values_data
      };
      
      return ContentService.createTextOutput(JSON.stringify(hist_data)).setMimeType(ContentService.MimeType.JSON);
    }
  }
  
  return ContentService.createTextOutput('A variável ' + variavel + ' não faz parte do banco de dados!');
}
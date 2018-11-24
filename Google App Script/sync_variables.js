var spreadsheet = SpreadsheetApp.openById('1iOf4d2F_I6pzALuNP2FrWR6NQh68GeJDkWT_W8TqdTs');
var sheet = spreadsheet.getSheetByName('variables_info');

function doGet() {
  var variables = [];
  
  for(var i = 2; i < sheet.getLastRow() + 1; i++) {
    variables.push({
      'id': sheet.getRange(i, 1).getValue(),
      'name': sheet.getRange(i, 2).getValue(),
      'description': sheet.getRange(i, 3).getValue(),
      'tag': sheet.getRange(i, 4).getValue(),
      'type': sheet.getRange(i, 5).getValue(),
      'eng_unit': sheet.getRange(i, 6).getValue(),
      'l_limit': sheet.getRange(i, 7).getValue(),
      'h_limit': sheet.getRange(i, 8).getValue(),
      'll_limit': sheet.getRange(i, 9).getValue(),
      'hh_limit': sheet.getRange(i, 10).getValue(),
      'last_value': sheet.getRange(i, 11).getValue()
    });
  }
  
  return ContentService.createTextOutput(JSON.stringify(variables)).setMimeType(ContentService.MimeType.JSON);
}